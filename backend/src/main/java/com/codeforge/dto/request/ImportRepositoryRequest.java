package com.codeforge.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request to import a GitHub repository
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ImportRepositoryRequest {
    
    @NotBlank(message = "Repository owner is required")
    private String owner;
    
    @NotBlank(message = "Repository name is required")
    private String repo;
    
    @NotNull(message = "Project ID is required")
    private Long projectId;
}
