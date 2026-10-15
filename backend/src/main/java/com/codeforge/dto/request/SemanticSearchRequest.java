package com.codeforge.dto.request;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request for semantic code search
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SemanticSearchRequest {
    
    @NotBlank(message = "Query is required")
    private String query;
    
    @NotNull(message = "Project ID is required")
    private Long projectId;
    
    @Min(value = 1, message = "Limit must be at least 1")
    @lombok.Builder.Default
    private int limit = 10;
}
