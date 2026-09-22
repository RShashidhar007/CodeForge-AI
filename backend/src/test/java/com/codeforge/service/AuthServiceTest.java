package com.codeforge.service;

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

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

/**
 * Unit tests for AuthService
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
    private JWTProvider jwtProvider;
    
    @Mock
    private PasswordEncoder passwordEncoder;
    
    @InjectMocks
    private AuthService authService;
    
    private RegisterCandidateRequest registerRequest;
    private LoginRequest loginRequest;
    
    @BeforeEach
    void setUp() {
        registerRequest = new RegisterCandidateRequest("John Doe", "john@example.com", "password123");
        loginRequest = new LoginRequest("john@example.com", "password123");
    }
    
    @Test
    void testRegisterCandidateSuccess() {
        // Arrange
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        
        User user = User.builder()
            .id(1L)
            .name("John Doe")
            .email("john@example.com")
            .passwordHash("hashed_password")
            .role(User.UserRole.CANDIDATE)
            .enabled(true)
            .build();
        
        when(userRepository.save(any(User.class))).thenReturn(user);
        when(candidateRepository.save(any(Candidate.class))).thenReturn(new Candidate());
        
        // Act
        UserResponse response = authService.registerCandidate(registerRequest);
        
        // Assert
        assertNotNull(response);
        assertEquals("John Doe", response.getName());
        assertEquals("john@example.com", response.getEmail());
        assertEquals("CANDIDATE", response.getRole());
    }
    
    @Test
    void testRegisterCandidateDuplicate() {
        // Arrange
        when(userRepository.existsByEmail(anyString())).thenReturn(true);
        
        // Act & Assert
        assertThrows(DuplicateResourceException.class, () -> authService.registerCandidate(registerRequest));
    }
    
    @Test
    void testLoginSuccess() {
        // Arrange
        User user = User.builder()
            .id(1L)
            .name("John Doe")
            .email("john@example.com")
            .passwordHash("hashed_password")
            .role(User.UserRole.CANDIDATE)
            .enabled(true)
            .build();
        
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(user));
        when(passwordEncoder.matches(anyString(), anyString())).thenReturn(true);
        when(jwtProvider.generateToken(1L, "john@example.com", "CANDIDATE")).thenReturn("jwt_token");
        
        // Act
        LoginResponse response = authService.login(loginRequest);
        
        // Assert
        assertNotNull(response);
        assertEquals("jwt_token", response.getToken());
        assertEquals("Bearer", response.getTokenType());
        assertEquals("John Doe", response.getUser().getName());
    }
    
    @Test
    void testLoginInvalidCredentials() {
        // Arrange
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.empty());
        
        // Act & Assert
        assertThrows(BadCredentialsException.class, () -> authService.login(loginRequest));
    }
    
    @Test
    void testLoginDisabledUser() {
        // Arrange
        User user = User.builder()
            .id(1L)
            .email("john@example.com")
            .enabled(false)
            .build();
        
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(user));
        
        // Act & Assert
        assertThrows(BadCredentialsException.class, () -> authService.login(loginRequest));
    }
}
