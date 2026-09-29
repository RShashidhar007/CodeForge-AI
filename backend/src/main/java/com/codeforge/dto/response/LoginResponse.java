package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for login endpoint
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LoginResponse {
    
    private String token;
    
    @JsonProperty("token_type")
    private String tokenType;
    
    @JsonProperty("expires_in_seconds")
    private Integer expiresInSeconds;
    
    private UserResponse user;
}
