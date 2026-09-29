package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * Code chunk entity for RAG (Retrieval-Augmented Generation)
 * Stores embeddings as JSON for semantic search
 */
@Entity
@Table(name = "code_chunks", indexes = {
    @Index(columnList = "document_id"),
    @Index(columnList = "start_line")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"document"})
@ToString(exclude = {"document"})
public class CodeChunk {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "document_id", nullable = false)
    private CodeDocument document;
    
    @Column(nullable = false)
    private Integer startLine;
    
    @Column(nullable = false)
    private Integer endLine;
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String content;
    
    @Column(columnDefinition = "TEXT")
    private String symbol;
    
    @Column(columnDefinition = "TEXT")
    private String embedding; // Stored as JSON array
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
