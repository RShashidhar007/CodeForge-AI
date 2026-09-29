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
@EqualsAndHashCode(exclude = {"project", "executions", "patches"})
@ToString(exclude = {"project", "executions", "patches"})
public class AITask {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;
    
    @Column(length = 255, nullable = false)
    private String title;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    @Column(length = 100, nullable = false)
    @Enumerated(EnumType.STRING)
    private TaskStatus status; // PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    
    @Column(length = 50)
    @Enumerated(EnumType.STRING)
    private TaskType taskType; // CODE_ANALYSIS, REFACTORING, BUG_FIX, TEST_GENERATION
    
    @Column(columnDefinition = "TEXT")
    private String selectedFiles; // JSON array of file paths
    
    @Column(columnDefinition = "TEXT")
    private String result; // Task execution result
    
    @OneToMany(mappedBy = "task", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<AgentExecution> executions = new HashSet<>();
    
    @OneToMany(mappedBy = "task", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<TaskPatch> patches = new HashSet<>();
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    public enum TaskStatus {
        PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    }
    
    public enum TaskType {
        CODE_ANALYSIS, REFACTORING, BUG_FIX, TEST_GENERATION
    }
}
