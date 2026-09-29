package com.codeforge.controller;

import com.codeforge.dto.request.LoginRequest;
import com.codeforge.dto.request.RegisterCandidateRequest;
import com.codeforge.dto.request.RegisterRecruiterRequest;
import com.codeforge.dto.response.LoginResponse;
import com.codeforge.dto.response.UserResponse;
import com.codeforge.service.AuthService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Authentication controller
 * Endpoints: POST /auth/register/candidate, POST /auth/register/recruiter, POST /auth/login
 */
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {
    
    private final AuthService authService;
    
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
}
