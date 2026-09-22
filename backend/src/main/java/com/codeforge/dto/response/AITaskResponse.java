package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * Response DTO for AI task
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AITaskResponse {
    
    private Long id;
    
    @JsonProperty("project_id")
    private Long projectId;
    
    private String title;
    private String description;
    private String status;
    
    @JsonProperty("task_type")
    private String taskType;
    
    @JsonProperty("selected_files")
    private String selectedFiles;
    
    private String result;
    
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonProperty("updated_at")
    private LocalDateTime updatedAt;
}
