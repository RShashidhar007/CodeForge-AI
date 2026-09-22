package com.codeforge.controller;

import com.codeforge.dto.request.ApproveTaskRequest;
import com.codeforge.dto.request.CreateTaskRequest;
import com.codeforge.dto.response.AITaskResponse;
import com.codeforge.dto.response.PageResponse;
import com.codeforge.security.SecurityUser;
import com.codeforge.service.TaskService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

/**
 * Task controller
 * Endpoints:
 * - POST /v1/projects/{projectId}/ai/tasks
 * - GET /v1/projects/{projectId}/ai/tasks
 * - GET /v1/projects/{projectId}/ai/tasks/{taskId}
 * - POST /v1/projects/{projectId}/ai/tasks/{taskId}/approve
 * - POST /v1/projects/{projectId}/ai/tasks/{taskId}/cancel
 */
@RestController
@RequestMapping("/v1/projects/{projectId}/ai/tasks")
@RequiredArgsConstructor
public class TaskController {
    
    private final TaskService taskService;
    
    /**
     * Create a new AI task
     * POST /v1/projects/{projectId}/ai/tasks
     */
    @PostMapping
    public ResponseEntity<AITaskResponse> createTask(
            @PathVariable Long projectId,
            @Valid @RequestBody CreateTaskRequest request,
            @AuthenticationPrincipal SecurityUser user) {
        AITaskResponse response = taskService.createTask(projectId, request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    /**
     * List tasks for a project
     * GET /v1/projects/{projectId}/ai/tasks?page=0&size=20
     */
    @GetMapping
    public ResponseEntity<PageResponse<AITaskResponse>> listTasks(
            @PathVariable Long projectId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @AuthenticationPrincipal SecurityUser user) {
        
        Pageable pageable = PageRequest.of(page, size);
        PageResponse<AITaskResponse> response = taskService.listTasks(projectId, pageable);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Get a specific task
     * GET /v1/projects/{projectId}/ai/tasks/{taskId}
     */
    @GetMapping("/{taskId}")
    public ResponseEntity<AITaskResponse> getTask(
            @PathVariable Long projectId,
            @PathVariable Long taskId,
            @AuthenticationPrincipal SecurityUser user) {
        AITaskResponse response = taskService.getTask(projectId, taskId);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Approve or reject a task
     * POST /v1/projects/{projectId}/ai/tasks/{taskId}/approve
     */
    @PostMapping("/{taskId}/approve")
    public ResponseEntity<AITaskResponse> approveTask(
            @PathVariable Long projectId,
            @PathVariable Long taskId,
            @Valid @RequestBody ApproveTaskRequest request,
            @AuthenticationPrincipal SecurityUser user) {
        AITaskResponse response = taskService.approveTask(projectId, taskId, user.getUserId(), request);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Cancel a task
     * POST /v1/projects/{projectId}/ai/tasks/{taskId}/cancel
     */
    @PostMapping("/{taskId}/cancel")
    public ResponseEntity<AITaskResponse> cancelTask(
            @PathVariable Long projectId,
            @PathVariable Long taskId,
            @AuthenticationPrincipal SecurityUser user) {
        AITaskResponse response = taskService.cancelTask(projectId, taskId);
        return ResponseEntity.ok(response);
    }
}
