package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * Repository index metadata for tracking RAG indexing status
 */
@Entity
@Table(name = "repository_index_metadata", indexes = {
    @Index(columnList = "project_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"project"})
@ToString(exclude = {"project"})
public class RepositoryIndexMetadata {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", unique = true, nullable = false)
    private Project project;
    
    @Column(nullable = false)
    private Integer totalFiles;
    
    @Column(nullable = false)
    private Integer indexedFiles;
    
    @Column(nullable = false)
    private Integer totalChunks;
    
    @Column(nullable = false)
    private Double progress; // 0.0 to 1.0
    
    @Column(columnDefinition = "TEXT")
    private String lastError;
    
    @Column
    private LocalDateTime lastIndexedAt;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
