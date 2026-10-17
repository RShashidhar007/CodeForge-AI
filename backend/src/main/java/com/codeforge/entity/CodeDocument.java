package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

/**
 * Code document entity for indexed source code
 */
@Entity
@Table(name = "code_documents", indexes = {
    @Index(columnList = "project_id"),
    @Index(columnList = "file_path")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"project", "file", "chunks"})
@ToString(exclude = {"project", "file", "chunks"})
public class CodeDocument {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "file_id")
    private File file;
    
    @Column(nullable = false, columnDefinition = "NVARCHAR(255)")
    private String filePath;
    
    @Column(nullable = false, length = 255)
    private String fileName;
    
    @Column(length = 50)
    private String language;
    
    @Column(columnDefinition = "NVARCHAR(MAX)")
    private String content;
    
    @Column(length = 64)
    private String contentHash;
    
    @Column
    private LocalDateTime indexedAt;
    
    @OneToMany(mappedBy = "codeDocument", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<CodeChunk> chunks = new HashSet<>();
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
