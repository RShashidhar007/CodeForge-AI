package com.codeforge.controller;

import com.codeforge.config.AppProperties;
import com.codeforge.dto.request.LoginRequest;
import com.codeforge.dto.request.RegisterCandidateRequest;
import com.codeforge.dto.request.RegisterRecruiterRequest;
import com.codeforge.dto.response.LoginResponse;
import com.codeforge.dto.response.UserResponse;
import com.codeforge.exception.GlobalExceptionHandler;
import com.codeforge.security.JWTBlacklistService;
import com.codeforge.security.JWTProvider;
import com.codeforge.service.AuthService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ValueOperations;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.Map;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Standalone MockMvc tests for AuthController.
 *
 * Uses no Spring context to avoid the JDK 27 / Byte Buddy incompatibility.
 * Dependencies are real instances or subclass fakes — no Mockito involved.
 */
class AuthControllerTest {

    private MockMvc mockMvc;
    private ObjectMapper objectMapper;

    /** Fake AuthService — subclass override, zero Mockito/Byte Buddy. */
    private static class FakeAuthService extends AuthService {
        UserResponse registerResponse;
        LoginResponse loginResponse;

        FakeAuthService() {
            // Pass nulls — Lombok constructor needs all 5 final fields; they are
            // never accessed because we override all methods the controller calls.
            super(null, null, null, null, null);
        }

        @Override
        public UserResponse registerCandidate(RegisterCandidateRequest r) { return registerResponse; }

        @Override
        public UserResponse registerRecruiter(RegisterRecruiterRequest r) { return registerResponse; }

        @Override
        public LoginResponse login(LoginRequest r) { return loginResponse; }
    }

    private FakeAuthService fakeAuthService;

    @BeforeEach
    @SuppressWarnings("unchecked")
    void setUp() {
        objectMapper = new ObjectMapper();
        fakeAuthService = new FakeAuthService();

        // Real JWTProvider
        AppProperties props = new AppProperties();
        props.getJwt().setSecret("test-secret-at-least-32-characters-long");
        props.getJwt().setExpiration(3600);
        JWTProvider jwtProvider = new JWTProvider(props);

        // JDK-proxy ValueOperations (no concrete class subclassing)
        Map<String, Object> redisStore = new HashMap<>();
        ValueOperations<String, Object> valueOps = (ValueOperations<String, Object>)
                Proxy.newProxyInstance(
                        getClass().getClassLoader(),
                        new Class[]{ValueOperations.class},
                        (p, method, args) -> {
                            if ("set".equals(method.getName()) && args != null && args.length == 4) {
                                redisStore.put((String) args[0], args[1]);
                            }
                            return null;
                        });

        RedisTemplate<String, Object> redisTemplate = new RedisTemplate<>() {
            @Override public Boolean hasKey(String k) { return redisStore.containsKey(k); }
            @Override public ValueOperations<String, Object> opsForValue() { return valueOps; }
        };

        JWTBlacklistService blacklistService = new JWTBlacklistService(redisTemplate);
        jwtProvider.setJwtBlacklistService(blacklistService);

        AuthController controller = new AuthController(fakeAuthService, jwtProvider, blacklistService);
        mockMvc = MockMvcBuilders
                .standaloneSetup(controller)
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();
    }

    @Test
    void registerCandidate_success_returns201() throws Exception {
        fakeAuthService.registerResponse = UserResponse.builder()
                .id(1L).name("John Doe").email("john@example.com")
                .role("CANDIDATE").enabled(true).build();

        mockMvc.perform(post("/auth/register/candidate")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new RegisterCandidateRequest("John Doe", "john@example.com", "password123"))))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("John Doe"))
                .andExpect(jsonPath("$.email").value("john@example.com"))
                .andExpect(jsonPath("$.role").value("CANDIDATE"));
    }

    @Test
    void login_success_returns200WithToken() throws Exception {
        UserResponse user = UserResponse.builder()
                .id(1L).name("John Doe").email("john@example.com")
                .role("CANDIDATE").enabled(true).build();

        fakeAuthService.loginResponse = LoginResponse.builder()
                .token("jwt_token").tokenType("Bearer")
                .expiresInSeconds(86400).user(user).build();

        mockMvc.perform(post("/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new LoginRequest("john@example.com", "password123"))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").value("jwt_token"))
                .andExpect(jsonPath("$.token_type").value("Bearer"))
                .andExpect(jsonPath("$.user.email").value("john@example.com"));
    }

    @Test
    void login_blankCredentials_returns400() throws Exception {
        mockMvc.perform(post("/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new LoginRequest("", ""))))
                .andExpect(status().isBadRequest());
    }

    @Test
    void logout_returns200() throws Exception {
        mockMvc.perform(post("/auth/logout")
                        .header("Authorization", "Bearer some.valid.token"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.message").value("Logged out successfully"));
    }
}
