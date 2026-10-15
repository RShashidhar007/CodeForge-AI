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
    @Index(columnList = "code_document_id"),
    @Index(columnList = "language")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"codeDocument"})
@ToString(exclude = {"codeDocument"})
public class CodeChunk {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "code_document_id", nullable = false)
    private CodeDocument codeDocument;
    
    @Column(columnDefinition = "NVARCHAR(MAX)", nullable = false)
    private String content;
    
    @Column
    private Long startLine;
    
    @Column
    private Long endLine;
    
    @Column(length = 50)
    private String language;
    
    @Column(length = 500)
    private String symbolName;
    
    @Column(columnDefinition = "VARBINARY(MAX)")
    private byte[] embedding;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
}
