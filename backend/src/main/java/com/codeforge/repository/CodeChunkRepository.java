package com.codeforge.repository;

import com.codeforge.entity.CodeChunk;
import com.codeforge.entity.CodeDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for CodeChunk entity
 */
@Repository
public interface CodeChunkRepository extends JpaRepository<CodeChunk, Long> {
    List<CodeChunk> findByDocumentId(Long documentId);
    
    List<CodeChunk> findByDocument(CodeDocument document);
    
    List<CodeChunk> findByDocumentProjectId(Long projectId);
}
