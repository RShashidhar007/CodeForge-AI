package com.codeforge.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request for GitHub OAuth callback
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class GithubOAuthCallbackRequest {
    
    @NotBlank(message = "Authorization code is required")
    private String code;
    
    private String state;
}
