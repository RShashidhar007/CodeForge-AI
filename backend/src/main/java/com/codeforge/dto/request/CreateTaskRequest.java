package com.codeforge.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Set;

/**
 * Request DTO for creating an AI task
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateTaskRequest {
    
    private String title;
    private String description;
    private String taskType; // CODE_ANALYSIS, REFACTORING, BUG_FIX, TEST_GENERATION
    private Set<String> selectedFiles;
}
