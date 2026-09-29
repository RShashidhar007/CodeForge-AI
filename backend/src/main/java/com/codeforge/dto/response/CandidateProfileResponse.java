package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Set;

/**
 * Response DTO for candidate profile
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CandidateProfileResponse {
    
    @JsonProperty("user_id")
    private Long userId;
    
    private String name;
    private String email;
    private String phone;
    private String location;
    private String bio;
    
    @JsonProperty("github_url")
    private String githubUrl;
    
    @JsonProperty("linkedin_url")
    private String linkedinUrl;
    
    private Set<String> skills;
}
