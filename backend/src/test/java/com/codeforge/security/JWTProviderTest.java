package com.codeforge.security;

import com.codeforge.config.AppProperties;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for JWTProvider.
 * Uses a real AppProperties/JWTProvider instance — no mocks needed since JWTProvider
 * is a plain POJO around the auth0 JWT library. JWTBlacklistService is left null
 * intentionally; validateToken handles null gracefully (the @Lazy setter never fires).
 */
class JWTProviderTest {

    private JWTProvider jwtProvider;

    @BeforeEach
    void setUp() {
        AppProperties appProperties = new AppProperties();
        appProperties.getJwt().setSecret("this-is-a-very-long-secret-key-with-at-least-32-characters-for-hs256");
        appProperties.getJwt().setExpiration(86400);

        jwtProvider = new JWTProvider(appProperties);
        // JWTBlacklistService stays null — validateToken checks for null before calling it
    }

    @Test
    void generateToken_returnsNonBlankToken() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        assertNotNull(token);
        assertFalse(token.isBlank());
    }

    @Test
    void getUserId_returnsCorrectId() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        assertEquals(1L, jwtProvider.getUserId(token));
    }

    @Test
    void getEmail_returnsCorrectEmail() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        assertEquals("test@example.com", jwtProvider.getEmail(token));
    }

    @Test
    void getRole_returnsCorrectRole() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        assertEquals("CANDIDATE", jwtProvider.getRole(token));
    }

    @Test
    void validateToken_validToken_returnsTrue() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        assertTrue(jwtProvider.validateToken(token));
    }

    @Test
    void validateToken_invalidToken_returnsFalse() {
        assertFalse(jwtProvider.validateToken("this.is.not.a.valid.jwt"));
    }

    @Test
    void validateToken_tamperedToken_returnsFalse() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        // Corrupt the signature segment
        String tampered = token.substring(0, token.lastIndexOf('.') + 1) + "invalidsignature";
        assertFalse(jwtProvider.validateToken(tampered));
    }

    @Test
    void isTokenExpired_freshToken_returnsFalse() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        assertFalse(jwtProvider.isTokenExpired(token));
    }

    @Test
    void getExpirationDate_returnsNonNull() {
        String token = jwtProvider.generateToken(1L, "test@example.com", "CANDIDATE");
        assertNotNull(jwtProvider.getExpirationDateFromToken(token));
    }
}
