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
@Table(name = "task_workspaces", indexes = {
    @Index(columnList = "task_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"task"})
@ToString(exclude = {"task"})
public class TaskWorkspace {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "task_id", unique = true, nullable = false)
    private AITask task;
    
    @Column(length = 500, nullable = false)
    private String workspacePath;
    
    @Column(columnDefinition = "TEXT")
    private String environment; // JSON encoded environment variables
    
    @Column(nullable = false)
    private Long diskUsageBytes;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
