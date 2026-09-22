package com.codeforge.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request DTO for AI chat endpoint
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatRequest {
    
    private String question;
    private Long conversationId;
    private Integer topK;
}
