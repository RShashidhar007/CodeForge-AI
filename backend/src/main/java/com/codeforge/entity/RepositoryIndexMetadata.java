package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * Repository index metadata entity for tracking indexing progress
 */
@Entity
@Table(name = "repository_index_metadata")
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
    @JoinColumn(name = "project_id", nullable = false, unique = true)
    private Project project;
    
    @Column
    private Long totalFiles;
    
    @Column
    private Long indexedFiles;
    
    @Column
    private Long totalChunks;
    
    @Column
    private LocalDateTime lastIndexedAt;
    
    @Column(length = 50)
    private String status;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
