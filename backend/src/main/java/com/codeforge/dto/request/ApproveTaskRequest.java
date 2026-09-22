package com.codeforge.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request DTO for approving/rejecting a task
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ApproveTaskRequest {
    
    private boolean approved;
    private String reason;
}
