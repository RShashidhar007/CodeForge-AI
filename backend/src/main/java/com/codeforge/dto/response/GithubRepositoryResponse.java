package com.codeforge.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * Response containing GitHub repository information
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class GithubRepositoryResponse {
    private String name;
    private String fullName;
    private String description;
    private boolean isPrivate;
    private String url;
    private String language;
    private int stars;
    private Object updatedAt; // Can be Date or LocalDateTime
}
