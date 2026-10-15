package com.codeforge.service;

import com.codeforge.config.AppProperties;
import com.codeforge.dto.request.LoginRequest;
import com.codeforge.dto.request.RegisterCandidateRequest;
import com.codeforge.dto.response.LoginResponse;
import com.codeforge.dto.response.UserResponse;
import com.codeforge.entity.Candidate;
import com.codeforge.entity.User;
import com.codeforge.exception.BadCredentialsException;
import com.codeforge.exception.DuplicateResourceException;
import com.codeforge.repository.CandidateRepository;
import com.codeforge.repository.RecruiterRepository;
import com.codeforge.repository.UserRepository;
import com.codeforge.security.JWTProvider;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.util.ReflectionTestUtils;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

/**
 * Unit tests for AuthService.
 * JWTProvider is constructed as a real instance (@Spy) to avoid JDK 27
 * Mockito inline-mock incompatibility when mocking non-interface classes.
 */
@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private CandidateRepository candidateRepository;

    @Mock
    private RecruiterRepository recruiterRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    // Real JWTProvider — avoids JDK 27 Mockito inline-mock failure on @Mock/@Spy of concrete classes.
    // Injected manually into AuthService via reflection in setUp().
    private JWTProvider jwtProvider;

    @InjectMocks
    private AuthService authService;

    private RegisterCandidateRequest registerRequest;
    private LoginRequest loginRequest;

    @BeforeEach
    void setUp() {
        jwtProvider = buildJwtProvider();
        // Inject the real JWTProvider into the @InjectMocks-created AuthService
        ReflectionTestUtils.setField(authService, "jwtProvider", jwtProvider);

        registerRequest = new RegisterCandidateRequest("John Doe", "john@example.com", "password123");
        loginRequest = new LoginRequest("john@example.com", "password123");
    }

    // ── helpers ────────────────────────────────────────────────────────────────

    private static JWTProvider buildJwtProvider() {
        AppProperties props = new AppProperties();
        props.getJwt().setSecret("test-secret-key-at-least-32-characters-long-for-tests");
        props.getJwt().setExpiration(86400);
        return new JWTProvider(props);
    }

    // ── registerCandidate ──────────────────────────────────────────────────────

    @Test
    void registerCandidate_success_returnsUserResponse() {
        when(userRepository.existsByEmail(anyString())).thenReturn(false);

        User saved = User.builder()
                .id(1L).name("John Doe").email("john@example.com")
                .passwordHash("hashed").role(User.UserRole.CANDIDATE).enabled(true)
                .build();

        when(userRepository.save(any(User.class))).thenReturn(saved);
        when(candidateRepository.save(any(Candidate.class))).thenReturn(new Candidate());

        UserResponse response = authService.registerCandidate(registerRequest);

        assertNotNull(response);
        assertEquals("John Doe", response.getName());
        assertEquals("john@example.com", response.getEmail());
        assertEquals("CANDIDATE", response.getRole());
    }

    @Test
    void registerCandidate_duplicateEmail_throwsDuplicateResourceException() {
        when(userRepository.existsByEmail(anyString())).thenReturn(true);
        assertThrows(DuplicateResourceException.class,
                () -> authService.registerCandidate(registerRequest));
    }

    // ── login ──────────────────────────────────────────────────────────────────

    @Test
    void login_success_returnsLoginResponseWithToken() {
        User user = User.builder()
                .id(1L).name("John Doe").email("john@example.com")
                .passwordHash("hashed").role(User.UserRole.CANDIDATE).enabled(true)
                .build();

        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(user));
        when(passwordEncoder.matches(anyString(), anyString())).thenReturn(true);

        LoginResponse response = authService.login(loginRequest);

        assertNotNull(response);
        assertNotNull(response.getToken());
        assertFalse(response.getToken().isBlank());
        assertEquals("Bearer", response.getTokenType());
        assertEquals("John Doe", response.getUser().getName());
    }

    @Test
    void login_unknownEmail_throwsBadCredentialsException() {
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.empty());
        assertThrows(BadCredentialsException.class, () -> authService.login(loginRequest));
    }

    @Test
    void login_wrongPassword_throwsBadCredentialsException() {
        User user = User.builder()
                .id(1L).email("john@example.com")
                .passwordHash("hashed").role(User.UserRole.CANDIDATE).enabled(true)
                .build();

        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(user));
        when(passwordEncoder.matches(anyString(), anyString())).thenReturn(false);

        assertThrows(BadCredentialsException.class, () -> authService.login(loginRequest));
    }

    @Test
    void login_disabledUser_throwsBadCredentialsException() {
        User user = User.builder()
                .id(1L).email("john@example.com")
                .passwordHash("hashed").role(User.UserRole.CANDIDATE).enabled(false)
                .build();

        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(user));

        assertThrows(BadCredentialsException.class, () -> authService.login(loginRequest));
    }
}
