package com.codeforge.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
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
    
    @NotBlank(message = "Question is required")
    @Size(max = 5000, message = "Question must be at most 5000 characters")
    private String question;
    private Long conversationId;
    private Integer topK;
}
