package com.codeforge.service;

import com.codeforge.dto.request.ApproveTaskRequest;
import com.codeforge.dto.request.CreateTaskRequest;
import com.codeforge.dto.response.AITaskResponse;
import com.codeforge.dto.response.PageResponse;
import com.codeforge.entity.AITask;
import com.codeforge.entity.AITask.TaskStatus;
import com.codeforge.entity.AITask.TaskType;
import com.codeforge.entity.Project;
import com.codeforge.entity.TaskApproval;
import com.codeforge.exception.ResourceNotFoundException;
import com.codeforge.repository.AITaskRepository;
import com.codeforge.repository.ProjectRepository;
import com.codeforge.repository.TaskApprovalRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * Service for AI task management
 */
@Service
@RequiredArgsConstructor
public class TaskService {
    
    private final AITaskRepository taskRepository;
    private final ProjectRepository projectRepository;
    private final TaskApprovalRepository approvalRepository;
    
    /**
     * Create a new AI task
     */
    @Transactional
    public AITaskResponse createTask(Long projectId, CreateTaskRequest request) {
        Project project = projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        AITask task = AITask.builder()
            .project(project)
            .title(request.getTitle())
            .description(request.getDescription())
            .taskType(TaskType.valueOf(request.getTaskType()))
            .status(TaskStatus.PENDING)
            .selectedFiles(request.getSelectedFiles() != null ? 
                String.join(",", request.getSelectedFiles()) : "")
            .build();
        
        task = taskRepository.save(task);
        
        return mapToAITaskResponse(task);
    }
    
    /**
     * List tasks for a project
     */
    public PageResponse<AITaskResponse> listTasks(Long projectId, Pageable pageable) {
        Project project = projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        Page<AITask> page = taskRepository.findByProjectId(projectId, pageable);
        
        return PageResponse.<AITaskResponse>builder()
            .content(page.getContent().stream()
                .map(this::mapToAITaskResponse)
                .toList())
            .page(page.getNumber())
            .size(page.getSize())
            .totalPages(page.getTotalPages())
            .totalElements(page.getTotalElements())
            .last(page.isLast())
            .build();
    }
    
    /**
     * Get a specific task
     */
    public AITaskResponse getTask(Long projectId, Long taskId) {
        Project project = projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        AITask task = taskRepository.findById(taskId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Task", "id", taskId));
        
        if (!task.getProject().getId().equals(projectId)) {
            throw new ResourceNotFoundException("Task does not belong to this project");
        }
        
        return mapToAITaskResponse(task);
    }
    
    /**
     * Approve a task (change status and record approval)
     */
    @Transactional
    public AITaskResponse approveTask(Long projectId, Long taskId, Long approverId, ApproveTaskRequest request) {
        AITask task = taskRepository.findById(taskId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Task", "id", taskId));
        
        if (!task.getProject().getId().equals(projectId)) {
            throw new ResourceNotFoundException("Task does not belong to this project");
        }
        
        if (request.isApproved()) {
            task.setStatus(TaskStatus.COMPLETED);
            
            // Record approval
            TaskApproval approval = TaskApproval.builder()
                .task(task)
                .approverUserId(approverId)
                .status(TaskApproval.ApprovalStatus.APPROVED)
                .reason(request.getReason())
                .build();
            approvalRepository.save(approval);
        } else {
            task.setStatus(TaskStatus.FAILED);
            
            // Record rejection
            TaskApproval approval = TaskApproval.builder()
                .task(task)
                .approverUserId(approverId)
                .status(TaskApproval.ApprovalStatus.REJECTED)
                .reason(request.getReason())
                .build();
            approvalRepository.save(approval);
        }
        
        task = taskRepository.save(task);
        
        return mapToAITaskResponse(task);
    }
    
    /**
     * Cancel a task
     */
    @Transactional
    public AITaskResponse cancelTask(Long projectId, Long taskId) {
        AITask task = taskRepository.findById(taskId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Task", "id", taskId));
        
        if (!task.getProject().getId().equals(projectId)) {
            throw new ResourceNotFoundException("Task does not belong to this project");
        }
        
        task.setStatus(TaskStatus.CANCELLED);
        task = taskRepository.save(task);
        
        return mapToAITaskResponse(task);
    }
    
    private AITaskResponse mapToAITaskResponse(AITask task) {
        return AITaskResponse.builder()
            .id(task.getId())
            .projectId(task.getProject().getId())
            .title(task.getTitle())
            .description(task.getDescription())
            .status(task.getStatus().name())
            .taskType(task.getTaskType().name())
            .selectedFiles(task.getSelectedFiles())
            .result(task.getResult())
            .createdAt(task.getCreatedAt())
            .updatedAt(task.getUpdatedAt())
            .build();
    }
}
