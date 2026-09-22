package com.codeforge.controller;

import com.codeforge.dto.request.CandidateProfileUpdateRequest;
import com.codeforge.dto.response.CandidateProfileResponse;
import com.codeforge.security.SecurityUser;
import com.codeforge.service.CandidateService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

/**
 * Candidate controller
 * Endpoints: GET /candidates/me, PUT /candidates/me
 */
@RestController
@RequestMapping("/candidates")
@RequiredArgsConstructor
public class CandidateController {
    
    private final CandidateService candidateService;
    
    /**
     * Get candidate profile
     * GET /candidates/me
     */
    @GetMapping("/me")
    public ResponseEntity<CandidateProfileResponse> getMyProfile(
            @AuthenticationPrincipal SecurityUser user) {
        CandidateProfileResponse response = candidateService.getMyProfile(user.getUserId());
        return ResponseEntity.ok(response);
    }
    
    /**
     * Update candidate profile
     * PUT /candidates/me
     */
    @PutMapping("/me")
    public ResponseEntity<CandidateProfileResponse> updateMyProfile(
            @AuthenticationPrincipal SecurityUser user,
            @Valid @RequestBody CandidateProfileUpdateRequest request) {
        CandidateProfileResponse response = candidateService.updateMyProfile(user.getUserId(), request);
        return ResponseEntity.ok(response);
    }
}
