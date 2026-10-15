package com.codeforge.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Response containing semantic search results
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SemanticSearchResponse {
    private List<SearchResultItem> results;
    private int totalResults;
    
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SearchResultItem {
        private Long chunkId;
        private String filePath;
        private int startLine;
        private int endLine;
        private String symbol;
        private float score;
        private String content;
    }
}
