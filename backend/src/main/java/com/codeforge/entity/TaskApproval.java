package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

/**
 * Task approval entity for tracking approvals
 */
@Entity
@Table(name = "task_approvals", indexes = {
    @Index(columnList = "task_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"task"})
@ToString(exclude = {"task"})
public class TaskApproval {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "task_id", nullable = false)
    private AITask task;
    
    @Column(nullable = false)
    private Long approverUserId;
    
    @Column(length = 50)
    @Enumerated(EnumType.STRING)
    private ApprovalStatus status; // APPROVED, REJECTED
    
    @Column(columnDefinition = "TEXT")
    private String reason;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    public enum ApprovalStatus {
        APPROVED, REJECTED
    }
}
