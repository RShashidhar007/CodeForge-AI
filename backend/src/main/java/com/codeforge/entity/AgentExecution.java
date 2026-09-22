package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * Agent execution entity for tracking multi-agent workflow steps
 */
@Entity
@Table(name = "agent_executions", indexes = {
    @Index(columnList = "task_id"),
    @Index(columnList = "agent_name")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"task"})
@ToString(exclude = {"task"})
public class AgentExecution {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "task_id", nullable = false)
    private AITask task;
    
    @Column(length = 100, nullable = false)
    private String agentName;
    
    @Column(columnDefinition = "TEXT")
    private String input;
    
    @Column(columnDefinition = "TEXT")
    private String output;
    
    @Column(length = 50)
    @Enumerated(EnumType.STRING)
    private ExecutionStatus status; // PENDING, RUNNING, SUCCESS, FAILED
    
    @Column(columnDefinition = "TEXT")
    private String errorMessage;
    
    @Column
    private Integer sequenceOrder;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    public enum ExecutionStatus {
        PENDING, RUNNING, SUCCESS, FAILED
    }
}
