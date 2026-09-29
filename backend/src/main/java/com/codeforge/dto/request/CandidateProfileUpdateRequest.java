package com.codeforge.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Set;

/**
 * Request DTO for updating candidate profile
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CandidateProfileUpdateRequest {
    
    private String name;
    private String phone;
    private String location;
    private String bio;
    private String githubUrl;
    private String linkedinUrl;
    private Set<String> skills;
}
