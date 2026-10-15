package com.codeforge.repository;

import com.codeforge.entity.CodeChunk;
import com.codeforge.entity.CodeDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for CodeChunk entity
 */
@Repository
public interface CodeChunkRepository extends JpaRepository<CodeChunk, Long> {
    List<CodeChunk> findByCodeDocumentId(Long documentId);
    
    List<CodeChunk> findByCodeDocument(CodeDocument codeDocument);
    
    @Query("SELECT c FROM CodeChunk c WHERE c.codeDocument.project.id = :projectId")
    List<CodeChunk> findByCodeDocumentProjectId(@Param("projectId") Long projectId);
}
