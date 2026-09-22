package com.codeforge.dto.request;

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
    
    private String code;
    private String filepath;
    private Integer startLine;
    private Integer endLine;
    private String language;
    private String testFramework; // For test generation
}
