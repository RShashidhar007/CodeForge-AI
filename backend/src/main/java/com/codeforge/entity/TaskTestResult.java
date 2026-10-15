package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

/**
 * Task test result entity for storing test execution results
 */
@Entity
@Table(name = "task_test_results", indexes = {
    @Index(columnList = "ai_task_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"aiTask"})
@ToString(exclude = {"aiTask"})
public class TaskTestResult {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ai_task_id", nullable = false)
    private AITask aiTask;
    
    @Column(length = 500)
    private String testName;
    
    @Column(length = 50)
    private String status; // PASSED, FAILED, etc.
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String output;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
}
