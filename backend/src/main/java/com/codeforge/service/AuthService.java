package com.codeforge.service;

import com.codeforge.dto.request.LoginRequest;
import com.codeforge.dto.request.RegisterCandidateRequest;
import com.codeforge.dto.request.RegisterRecruiterRequest;
import com.codeforge.dto.response.LoginResponse;
import com.codeforge.dto.response.UserResponse;
import com.codeforge.entity.Candidate;
import com.codeforge.entity.Recruiter;
import com.codeforge.entity.User;
import com.codeforge.exception.BadCredentialsException;
import com.codeforge.exception.DuplicateResourceException;
import com.codeforge.repository.CandidateRepository;
import com.codeforge.repository.RecruiterRepository;
import com.codeforge.repository.UserRepository;
import com.codeforge.security.JWTProvider;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Authentication service for user registration and login
 */
@Service
@RequiredArgsConstructor
public class AuthService {
    
    private final UserRepository userRepository;
    private final CandidateRepository candidateRepository;
    private final RecruiterRepository recruiterRepository;
    private final JWTProvider jwtProvider;
    private final PasswordEncoder passwordEncoder;
    
    /**
     * Register a new candidate
     */
    @Transactional
    public UserResponse registerCandidate(RegisterCandidateRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw DuplicateResourceException.alreadyExists("User", "email", request.getEmail());
        }
        
        User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .passwordHash(passwordEncoder.encode(request.getPassword()))
            .role(User.UserRole.CANDIDATE)
            .enabled(true)
            .build();
        
        user = userRepository.save(user);
        
        // Create candidate profile
        Candidate candidate = Candidate.builder()
            .id(user.getId())
            .user(user)
            .build();
        candidateRepository.save(candidate);
        
        return mapToUserResponse(user);
    }
    
    /**
     * Register a new recruiter
     */
    @Transactional
    public UserResponse registerRecruiter(RegisterRecruiterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw DuplicateResourceException.alreadyExists("User", "email", request.getEmail());
        }
        
        User user = User.builder()
            .name(request.getName())
            .email(request.getEmail())
            .passwordHash(passwordEncoder.encode(request.getPassword()))
            .role(User.UserRole.RECRUITER)
            .enabled(true)
            .build();
        
        user = userRepository.save(user);
        
        // Create recruiter profile
        Recruiter recruiter = Recruiter.builder()
            .id(user.getId())
            .user(user)
            .phone(request.getPhone())
            .position(request.getPosition())
            .build();
        recruiterRepository.save(recruiter);
        
        return mapToUserResponse(user);
    }
    
    /**
     * Login user and return JWT token
     */
    public LoginResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
            .orElseThrow(() -> new BadCredentialsException("Invalid email or password"));
        
        if (!user.getEnabled()) {
            throw new BadCredentialsException("User account is disabled");
        }
        
        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new BadCredentialsException("Invalid email or password");
        }
        
        String token = jwtProvider.generateToken(user.getId(), user.getEmail(), user.getRole().name());
        
        return LoginResponse.builder()
            .token(token)
            .tokenType("Bearer")
            .expiresInSeconds(86400) // 24 hours
            .user(mapToUserResponse(user))
            .build();
    }
    
    private UserResponse mapToUserResponse(User user) {
        return UserResponse.builder()
            .id(user.getId())
            .name(user.getName())
            .email(user.getEmail())
            .role(user.getRole().name())
            .enabled(user.getEnabled())
            .build();
    }
}
