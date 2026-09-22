package com.codeforge.security;

import com.codeforge.config.AppProperties;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

/**
 * Unit tests for JWTProvider
 */
@ExtendWith(MockitoExtension.class)
class JWTProviderTest {
    
    @Mock
    private AppProperties appProperties;
    
    @Mock
    private AppProperties.Jwt jwtProperties;
    
    private JWTProvider jwtProvider;
    
    @BeforeEach
    void setUp() {
        when(appProperties.getJwt()).thenReturn(jwtProperties);
        when(jwtProperties.getSecret()).thenReturn("this-is-a-very-long-secret-key-with-at-least-32-characters-for-hs256");
        when(jwtProperties.getExpiration()).thenReturn(86400); // 24 hours
        
        jwtProvider = new JWTProvider(appProperties);
    }
    
    @Test
    void testGenerateToken() {
        // Act
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        
        // Assert
        assertNotNull(token);
        assertFalse(token.isEmpty());
    }
    
    @Test
    void testGetUserIdFromToken() {
        // Arrange
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        
        // Act
        Long userId = jwtProvider.getUserId(token);
        
        // Assert
        assertEquals(1L, userId);
    }
    
    @Test
    void testGetEmailFromToken() {
        // Arrange
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        
        // Act
        String email = jwtProvider.getEmail(token);
        
        // Assert
        assertEquals("test@example.com", email);
    }
    
    @Test
    void testGetRoleFromToken() {
        // Arrange
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        
        // Act
        String role = jwtProvider.getRole(token);
        
        // Assert
        assertEquals("CANDIDATE", role);
    }
    
    @Test
    void testValidateToken() {
        // Arrange
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        
        // Act
        Boolean isValid = jwtProvider.validateToken(token);
        
        // Assert
        assertTrue(isValid);
    }
    
    @Test
    void testValidateInvalidToken() {
        // Act
        Boolean isValid = jwtProvider.validateToken("invalid_token");
        
        // Assert
        assertFalse(isValid);
    }
}
