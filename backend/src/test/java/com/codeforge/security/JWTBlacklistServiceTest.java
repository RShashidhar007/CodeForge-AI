package com.codeforge.security;

import com.codeforge.config.AppProperties;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.data.redis.core.RedisOperations;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.test.util.ReflectionTestUtils;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for JWTBlacklistService.
 *
 * Avoids Mockito entirely (JDK 27 inline-mock incompatibility with Spring Redis classes).
 * Instead, a JDK proxy implements {@link ValueOperations} backed by a plain HashMap, and
 * a minimal anonymous {@link RedisTemplate} subclass delegates hasKey() to the same map.
 */
class JWTBlacklistServiceTest {

    private Map<String, Object> store;
    private JWTBlacklistService blacklistService;
    private JWTProvider jwtProvider;

    private static final String BLACKLIST_PREFIX = "jwt:blacklist:";

    @SuppressWarnings("unchecked")
    @BeforeEach
    void setUp() {
        store = new HashMap<>();

        // ValueOperations proxy — only set(key, value, ttl, unit) and get(key) are called by the service
        ValueOperations<String, Object> valueOpsProxy = (ValueOperations<String, Object>)
                Proxy.newProxyInstance(
                        getClass().getClassLoader(),
                        new Class[]{ValueOperations.class},
                        (proxy, method, args) -> {
                            if ("set".equals(method.getName()) && args.length == 4) {
                                store.put((String) args[0], args[1]);
                                return null;
                            }
                            if ("get".equals(method.getName()) && args.length == 1) {
                                return store.get(args[0]);
                            }
                            return null;
                        });

        // RedisTemplate subclass — hasKey() delegates to the map; opsForValue() returns the proxy
        RedisTemplate<String, Object> template = new RedisTemplate<>() {
            @Override
            public Boolean hasKey(String key) {
                return store.containsKey(key);
            }

            @Override
            public ValueOperations<String, Object> opsForValue() {
                return valueOpsProxy;
            }
        };

        blacklistService = new JWTBlacklistService(template);

        AppProperties props = new AppProperties();
        props.getJwt().setSecret("test-secret-key-at-least-32-characters-long-here");
        props.getJwt().setExpiration(3600);
        jwtProvider = new JWTProvider(props);
    }

    @Test
    void blacklistToken_validToken_storesKeyInStore() {
        String token = jwtProvider.generateToken(1L, "user@test.com", "CANDIDATE");
        blacklistService.blacklistToken(token);
        assertTrue(store.containsKey(BLACKLIST_PREFIX + token));
    }

    @Test
    void isBlacklisted_afterBlacklist_returnsTrue() {
        String token = jwtProvider.generateToken(1L, "user@test.com", "CANDIDATE");
        blacklistService.blacklistToken(token);
        assertTrue(blacklistService.isBlacklisted(token));
    }

    @Test
    void isBlacklisted_freshToken_returnsFalse() {
        String token = jwtProvider.generateToken(2L, "other@test.com", "RECRUITER");
        assertFalse(blacklistService.isBlacklisted(token));
    }

    @Test
    void blacklistToken_invalidToken_doesNotThrow() {
        assertDoesNotThrow(() -> blacklistService.blacklistToken("not.a.valid.jwt"));
    }

    @Test
    void blacklistToken_emptyString_doesNotThrow() {
        assertDoesNotThrow(() -> blacklistService.blacklistToken(""));
    }

    @Test
    void isBlacklisted_unknownToken_returnsFalse() {
        assertFalse(blacklistService.isBlacklisted("unknown.token.value"));
    }
}
