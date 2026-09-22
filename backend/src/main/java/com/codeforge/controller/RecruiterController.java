package com.codeforge.controller;

import com.codeforge.dto.request.RecruiterProfileUpdateRequest;
import com.codeforge.dto.response.RecruiterProfileResponse;
import com.codeforge.security.SecurityUser;
import com.codeforge.service.RecruiterService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

/**
 * Recruiter controller
 * Endpoints: GET /recruiters/me, PUT /recruiters/me
 */
@RestController
@RequestMapping("/recruiters")
@RequiredArgsConstructor
public class RecruiterController {
    
    private final RecruiterService recruiterService;
    
    /**
     * Get recruiter profile
     * GET /recruiters/me
     */
    @GetMapping("/me")
    public ResponseEntity<RecruiterProfileResponse> getMyProfile(
            @AuthenticationPrincipal SecurityUser user) {
        RecruiterProfileResponse response = recruiterService.getMyProfile(user.getUserId());
        return ResponseEntity.ok(response);
    }
    
    /**
     * Update recruiter profile
     * PUT /recruiters/me
     */
    @PutMapping("/me")
    public ResponseEntity<RecruiterProfileResponse> updateMyProfile(
            @AuthenticationPrincipal SecurityUser user,
            @Valid @RequestBody RecruiterProfileUpdateRequest request) {
        RecruiterProfileResponse response = recruiterService.updateMyProfile(user.getUserId(), request);
        return ResponseEntity.ok(response);
    }
}
