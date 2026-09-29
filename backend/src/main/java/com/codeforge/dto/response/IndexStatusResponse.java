package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for repository indexing status
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class IndexStatusResponse {
    
    private String status;
    
    @JsonProperty("total_files")
    private Integer totalFiles;
    
    @JsonProperty("indexed_files")
    private Integer indexedFiles;
    
    @JsonProperty("total_chunks")
    private Integer totalChunks;
    
    private Double progress;
    
    @JsonProperty("last_indexed_at")
    private String lastIndexedAt;
    
    @JsonProperty("last_error")
    private String lastError;
}
