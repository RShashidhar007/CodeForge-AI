package com.codeforge.security;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTVerificationException;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.codeforge.config.AppProperties;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT Token Provider for creating and validating JWT tokens.
 * Uses HS256 algorithm with configurable secret and expiration.
 */
@Component
@RequiredArgsConstructor
public class JWTProvider {
    
    private final AppProperties appProperties;
    
    private Algorithm getAlgorithm() {
        byte[] keyBytes = appProperties.getJwt().getSecret().getBytes(StandardCharsets.UTF_8);
        return Algorithm.HMAC256(keyBytes);
    }
    
    /**
     * Generate JWT token for a user
     */
    public String generateToken(Long userId, String email, String role) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + appProperties.getJwt().getExpiration() * 1000L);
        
        return JWT.create()
            .withSubject(String.valueOf(userId))
            .withClaim("email", email)
            .withClaim("role", role)
            .withIssuedAt(now)
            .withExpiresAt(expiryDate)
            .sign(getAlgorithm());
    }
    
    /**
     * Get user ID from token
     */
    public Long getUserId(String token) {
        try {
            DecodedJWT jwt = JWT.require(getAlgorithm()).build().verify(token);
            return Long.valueOf(jwt.getSubject());
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Get email from token
     */
    public String getEmail(String token) {
        try {
            DecodedJWT jwt = JWT.require(getAlgorithm()).build().verify(token);
            return jwt.getClaim("email").asString();
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Get role from token
     */
    public String getRole(String token) {
        try {
            DecodedJWT jwt = JWT.require(getAlgorithm()).build().verify(token);
            return jwt.getClaim("role").asString();
        } catch (Exception e) {
            return null;
        }
    }
    
    /**
     * Check if token is expired
     */
    public Boolean isTokenExpired(String token) {
        try {
            DecodedJWT jwt = JWT.require(getAlgorithm()).build().verify(token);
            return jwt.getExpiresAt().before(new Date());
        } catch (Exception e) {
            return true;
        }
    }
    
    /**
     * Get expiration date from token
     */
    public Date getExpirationDateFromToken(String token) {
        try {
            DecodedJWT jwt = JWT.decode(token);
            return jwt.getExpiresAt();
        } catch (Exception e) {
            return new Date(0);
        }
    }
    
    /**
     * Validate token
     */
    public Boolean validateToken(String token) {
        try {
            JWT.require(getAlgorithm()).build().verify(token);
            return !isTokenExpired(token);
        } catch (JWTVerificationException e) {
            return false;
        }
    }
}

