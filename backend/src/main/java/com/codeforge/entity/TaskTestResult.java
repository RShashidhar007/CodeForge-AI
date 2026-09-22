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
    @Index(columnList = "task_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"task"})
@ToString(exclude = {"task"})
public class TaskTestResult {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "task_id", nullable = false)
    private AITask task;
    
    @Column(length = 50)
    @Enumerated(EnumType.STRING)
    private TestStatus status; // PASSED, FAILED
    
    @Column(nullable = false)
    private Integer testsRun;
    
    @Column(nullable = false)
    private Integer testsPassed;
    
    @Column(nullable = false)
    private Integer testsFailed;
    
    @Column(columnDefinition = "TEXT")
    private String output;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    public enum TestStatus {
        PASSED, FAILED
    }
}
