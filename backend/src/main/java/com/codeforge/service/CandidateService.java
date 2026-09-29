package com.codeforge.service;

import com.codeforge.dto.request.CandidateProfileUpdateRequest;
import com.codeforge.dto.response.CandidateProfileResponse;
import com.codeforge.entity.Candidate;
import com.codeforge.entity.User;
import com.codeforge.exception.ResourceNotFoundException;
import com.codeforge.repository.CandidateRepository;
import com.codeforge.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Collections;
import java.util.Set;

/**
 * Service for candidate profile management
 */
@Service
@RequiredArgsConstructor
public class CandidateService {
    
    private final CandidateRepository candidateRepository;
    private final UserRepository userRepository;
    
    /**
     * Get candidate profile for authenticated user
     */
    public CandidateProfileResponse getMyProfile(Long userId) {
        Candidate candidate = candidateRepository.findById(userId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Candidate", "id", userId));
        
        return mapToCandidateProfileResponse(candidate);
    }
    
    /**
     * Update candidate profile
     */
    @Transactional
    public CandidateProfileResponse updateMyProfile(Long userId, CandidateProfileUpdateRequest request) {
        Candidate candidate = candidateRepository.findById(userId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Candidate", "id", userId));
        
        User user = candidate.getUser();
        
        if (request.getName() != null) {
            user.setName(request.getName());
        }
        
        if (request.getPhone() != null) {
            candidate.setPhone(request.getPhone());
        }
        
        if (request.getLocation() != null) {
            candidate.setLocation(request.getLocation());
        }
        
        if (request.getBio() != null) {
            candidate.setBio(request.getBio());
        }
        
        if (request.getGithubUrl() != null) {
            candidate.setGithubUrl(request.getGithubUrl());
        }
        
        if (request.getLinkedinUrl() != null) {
            candidate.setLinkedinUrl(request.getLinkedinUrl());
        }
        
        // Skills management disabled for now - will be implemented via raw queries
        
        userRepository.save(user);
        candidate = candidateRepository.save(candidate);
        
        return mapToCandidateProfileResponse(candidate);
    }
    
    private CandidateProfileResponse mapToCandidateProfileResponse(Candidate candidate) {
        // Skills will be populated from candidate_skills table via raw queries in future
        Set<String> skillNames = Collections.emptySet();
        
        return CandidateProfileResponse.builder()
            .userId(candidate.getId())
            .name(candidate.getUser().getName())
            .email(candidate.getUser().getEmail())
            .phone(candidate.getPhone())
            .location(candidate.getLocation())
            .bio(candidate.getBio())
            .githubUrl(candidate.getGithubUrl())
            .linkedinUrl(candidate.getLinkedinUrl())
            .skills(skillNames)
            .build();
    }
}
