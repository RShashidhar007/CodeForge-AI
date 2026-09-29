package com.codeforge.service;

import com.codeforge.dto.request.RecruiterProfileUpdateRequest;
import com.codeforge.dto.response.RecruiterProfileResponse;
import com.codeforge.entity.Recruiter;
import com.codeforge.entity.User;
import com.codeforge.exception.ResourceNotFoundException;
import com.codeforge.repository.RecruiterRepository;
import com.codeforge.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Service for recruiter profile management
 */
@Service
@RequiredArgsConstructor
public class RecruiterService {
    
    private final RecruiterRepository recruiterRepository;
    private final UserRepository userRepository;
    
    /**
     * Get recruiter profile for authenticated user
     */
    public RecruiterProfileResponse getMyProfile(Long userId) {
        Recruiter recruiter = recruiterRepository.findById(userId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Recruiter", "id", userId));
        
        return mapToRecruiterProfileResponse(recruiter);
    }
    
    /**
     * Update recruiter profile
     */
    @Transactional
    public RecruiterProfileResponse updateMyProfile(Long userId, RecruiterProfileUpdateRequest request) {
        Recruiter recruiter = recruiterRepository.findById(userId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Recruiter", "id", userId));
        
        User user = recruiter.getUser();
        
        if (request.getName() != null) {
            user.setName(request.getName());
        }
        
        if (request.getPhone() != null) {
            recruiter.setPhone(request.getPhone());
        }
        
        if (request.getPosition() != null) {
            recruiter.setPosition(request.getPosition());
        }
        
        if (request.getBio() != null) {
            recruiter.setBio(request.getBio());
        }
        
        userRepository.save(user);
        recruiter = recruiterRepository.save(recruiter);
        
        return mapToRecruiterProfileResponse(recruiter);
    }
    
    private RecruiterProfileResponse mapToRecruiterProfileResponse(Recruiter recruiter) {
        String companyName = recruiter.getCompany() != null ? recruiter.getCompany().getName() : null;
        Long companyId = recruiter.getCompany() != null ? recruiter.getCompany().getId() : null;
        
        return RecruiterProfileResponse.builder()
            .userId(recruiter.getId())
            .name(recruiter.getUser().getName())
            .email(recruiter.getUser().getEmail())
            .phone(recruiter.getPhone())
            .position(recruiter.getPosition())
            .bio(recruiter.getBio())
            .companyId(companyId)
            .companyName(companyName)
            .build();
    }
}
