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
    @Index(columnList = "code_document_id"),
    @Index(columnList = "analysis_type")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"codeDocument", "performedByUser"})
@ToString(exclude = {"codeDocument", "performedByUser"})
public class AIAnalysis {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "code_document_id")
    private CodeDocument codeDocument;
    
    @Column(length = 100)
    private String analysisType;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String analysisResult;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String summary;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "performed_by_user_id")
    private User performedByUser;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    public enum AnalysisType {
        EXPLAIN, BUGS, IMPROVE, TESTS
    }
}
