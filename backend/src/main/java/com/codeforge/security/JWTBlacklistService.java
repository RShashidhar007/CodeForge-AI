package com.codeforge.security;

import com.auth0.jwt.JWT;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.concurrent.TimeUnit;

@Service
@RequiredArgsConstructor
@Slf4j
public class JWTBlacklistService {

    private static final String BLACKLIST_PREFIX = "jwt:blacklist:";

    private final RedisTemplate<String, Object> redisTemplate;

    public void blacklistToken(String token) {
        try {
            Date expiresAt = JWT.decode(token).getExpiresAt();
            if (expiresAt == null) {
                log.warn("Token has no expiry, skipping blacklist");
                return;
            }
            long ttlMillis = expiresAt.getTime() - System.currentTimeMillis();
            if (ttlMillis <= 0) {
                log.debug("Token already expired, no need to blacklist");
                return;
            }
            String key = BLACKLIST_PREFIX + token;
            redisTemplate.opsForValue().set(key, "blacklisted", ttlMillis, TimeUnit.MILLISECONDS);
            log.info("Token blacklisted with TTL {}ms", ttlMillis);
        } catch (Exception e) {
            log.error("Error blacklisting token: {}", e.getMessage());
        }
    }

    public boolean isBlacklisted(String token) {
        try {
            String key = BLACKLIST_PREFIX + token;
            Boolean exists = redisTemplate.hasKey(key);
            return Boolean.TRUE.equals(exists);
        } catch (Exception e) {
            log.error("Error checking blacklist for token: {}", e.getMessage());
            return false;
        }
    }
}
