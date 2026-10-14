package com.codeforge.controller;

import com.codeforge.dto.request.LoginRequest;
import com.codeforge.dto.request.RegisterCandidateRequest;
import com.codeforge.dto.request.RegisterRecruiterRequest;
import com.codeforge.dto.response.LoginResponse;
import com.codeforge.dto.response.UserResponse;
import com.codeforge.security.JWTBlacklistService;
import com.codeforge.security.JWTProvider;
import com.codeforge.service.AuthService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * Authentication controller
 * Endpoints: POST /auth/register/candidate, POST /auth/register/recruiter, POST /auth/login
 */
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {
    
    private final AuthService authService;
    private final JWTProvider jwtProvider;
    private final JWTBlacklistService jwtBlacklistService;
    
    /**
     * Register a new candidate
     * POST /auth/register/candidate
     */
    @PostMapping("/register/candidate")
    public ResponseEntity<UserResponse> registerCandidate(
            @Valid @RequestBody RegisterCandidateRequest request) {
        UserResponse response = authService.registerCandidate(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    /**
     * Register a new recruiter
     * POST /auth/register/recruiter
     */
    @PostMapping("/register/recruiter")
    public ResponseEntity<UserResponse> registerRecruiter(
            @Valid @RequestBody RegisterRecruiterRequest request) {
        UserResponse response = authService.registerRecruiter(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    /**
     * Login user
     * POST /auth/login
     */
    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(
            @Valid @RequestBody LoginRequest request) {
        LoginResponse response = authService.login(request);
        return ResponseEntity.ok(response);
    }

    /**
     * Logout user by blacklisting JWT token
     * POST /auth/logout
     */
    @PostMapping("/logout")
    public ResponseEntity<Map<String, String>> logout(HttpServletRequest request) {
        String token = jwtProvider.extractTokenFromRequest(request);
        if (token != null) {
            jwtBlacklistService.blacklistToken(token);
        }
        return ResponseEntity.ok(Map.of("message", "Logged out successfully"));
    }
}
