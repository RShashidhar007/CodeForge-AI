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
    @Index(columnList = "ai_task_id"),
    @Index(columnList = "agent_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"aiTask"})
@ToString(exclude = {"aiTask"})
public class AgentExecution {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ai_task_id")
    private AITask aiTask;
    
    @Column(length = 255)
    private String agentId;
    
    @Column(length = 50)
    private String status;
    
    @Column
    private LocalDateTime startTime;
    
    @Column
    private LocalDateTime endTime;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String resultSummary;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    public enum ExecutionStatus {
        PENDING, RUNNING, SUCCESS, FAILED
    }
}
