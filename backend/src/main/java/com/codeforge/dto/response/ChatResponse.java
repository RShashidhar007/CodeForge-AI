package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Response DTO for AI chat endpoint
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ChatResponse {
    
    @JsonProperty("conversation_id")
    private Long conversationId;
    
    private String answer;
    private List<SourceReference> sources;
    
    @JsonProperty("chunks_retrieved")
    private Integer chunksRetrieved;
    
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
        
        private String symbol;
    }
}
