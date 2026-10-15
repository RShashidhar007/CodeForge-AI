package com.codeforge.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SemanticSearchResult {
    private Long chunkId;
    private String filePath;
    private Integer startLine;
    private Integer endLine;
    private String content;
    private Double score;
}
