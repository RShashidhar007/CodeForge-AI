package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Response DTO for code analysis endpoints
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CodeAnalysisResponse {
    
    private String analysis;
    private String explanation;
    private String suggestions;
    private String tests;
    
    @JsonProperty("test_framework")
    private String testFramework;
    
    private List<SourceReference> sources;
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SourceReference {
        private String file;
        
        @JsonProperty("start_line")
        private Integer startLine;
        
        @JsonProperty("end_line")
        private Integer endLine;
    }
}
