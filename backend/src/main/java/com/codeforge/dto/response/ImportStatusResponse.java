package com.codeforge.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * Response containing repository import status
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ImportStatusResponse {
    private Long projectId;
    private String status;
    private String currentStep;
    private int totalFiles;
    private int relevantFiles;
    private int processedFiles;
    private int totalChunks;
    private int embeddedChunks;
    private String error;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private Integer progressPercentage;
}
