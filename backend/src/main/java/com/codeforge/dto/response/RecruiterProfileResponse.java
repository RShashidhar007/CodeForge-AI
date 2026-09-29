package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for recruiter profile
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RecruiterProfileResponse {
    
    @JsonProperty("user_id")
    private Long userId;
    
    private String name;
    private String email;
    private String phone;
    private String position;
    private String bio;
    
    @JsonProperty("company_id")
    private Long companyId;
    
    @JsonProperty("company_name")
    private String companyName;
}
