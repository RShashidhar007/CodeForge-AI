package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * Task workspace entity for task execution environment
 */
@Entity
@Table(name = "task_workspaces")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"aiTask"})
@ToString(exclude = {"aiTask"})
public class TaskWorkspace {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ai_task_id", nullable = false, unique = true)
    private AITask aiTask;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String workspacePath;
    
    @Column
    private Integer cloneDepth;
    
    @Column(length = 255)
    private String branchName;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
