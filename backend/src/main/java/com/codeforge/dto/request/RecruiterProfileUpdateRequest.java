package com.codeforge.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request DTO for updating recruiter profile
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RecruiterProfileUpdateRequest {
    
    private String name;
    private String phone;
    private String position;
    private String bio;
}
