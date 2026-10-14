package com.codeforge.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Base request DTO for code analysis endpoints (explain, bugs, improve, tests)
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CodeAnalysisRequest {
    
    @NotBlank(message = "Code is required")
    @Size(max = 50000, message = "Code must be at most 50000 characters")
    private String code;
    private String filepath;
    private Integer startLine;
    private Integer endLine;
    private String language;
    private String testFramework; // For test generation
}
