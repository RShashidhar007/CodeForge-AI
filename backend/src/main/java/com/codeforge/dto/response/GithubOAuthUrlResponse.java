package com.codeforge.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response containing GitHub OAuth authorization URL
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class GithubOAuthUrlResponse {
    private String authorizationUrl;
    private String state;
}
