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
    @Index(columnList = "ai_task_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"aiTask", "approvedByUser"})
@ToString(exclude = {"aiTask", "approvedByUser"})
public class TaskApproval {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ai_task_id", nullable = false)
    private AITask aiTask;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "approved_by_user_id")
    private User approvedByUser;
    
    @Column(length = 50)
    private String approvalStatus;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String comments;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    public enum ApprovalStatus {
        APPROVED, REJECTED
    }
}
