package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

/**
 * AI task entity for multi-agent task execution
 */
@Entity
@Table(name = "ai_tasks", indexes = {
    @Index(columnList = "project_id"),
    @Index(columnList = "status")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"project", "user", "executions", "patches", "testResults", "approval"})
@ToString(exclude = {"project", "user", "executions", "patches", "testResults", "approval"})
public class AITask {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id")
    private Project project;
    
    @Column(length = 100, nullable = false)
    private String taskType;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String inputData;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String outputData;
    
    @Column(length = 50, nullable = false)
    private String status; // PENDING, RUNNING, COMPLETED, FAILED
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String errorMessage;
    
    @Column
    private LocalDateTime executionStartTime;

    @Column
    private LocalDateTime executionEndTime;

    @Column(length = 255)
    private String executedByAgentId;
    
    @OneToMany(mappedBy = "task", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<AgentExecution> executions = new HashSet<>();
    
    @OneToMany(mappedBy = "aiTask", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<TaskPatch> patches = new HashSet<>();
    
    @OneToMany(mappedBy = "aiTask", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<TaskTestResult> testResults = new HashSet<>();
    
    @OneToOne(mappedBy = "aiTask", cascade = CascadeType.ALL, orphanRemoval = true)
    private TaskApproval approval;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    public enum TaskStatus {
        PENDING, RUNNING, COMPLETED, FAILED
    }
    
    public enum TaskType {
        CODE_ANALYSIS, REFACTORING, BUG_FIX, TEST_GENERATION
    }
}
