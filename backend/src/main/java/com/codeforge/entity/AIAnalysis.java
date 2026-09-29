package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * AI analysis entity for code analysis results
 */
@Entity
@Table(name = "ai_analyses", indexes = {
    @Index(columnList = "project_id"),
    @Index(columnList = "analysis_type")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"project"})
@ToString(exclude = {"project"})
public class AIAnalysis {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;
    
    @Column(length = 100, nullable = false)
    @Enumerated(EnumType.STRING)
    private AnalysisType analysisType; // EXPLAIN, BUGS, IMPROVE, TESTS
    
    @Column(length = 500)
    private String filePath;
    
    @Column(nullable = false)
    private Integer startLine;
    
    @Column(nullable = false)
    private Integer endLine;
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String result;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
    
    public enum AnalysisType {
        EXPLAIN, BUGS, IMPROVE, TESTS
    }
}
