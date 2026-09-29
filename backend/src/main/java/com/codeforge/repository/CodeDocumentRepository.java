package com.codeforge.repository;

import com.codeforge.entity.CodeDocument;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository for CodeDocument entity
 */
@Repository
public interface CodeDocumentRepository extends JpaRepository<CodeDocument, Long> {
    List<CodeDocument> findByProjectId(Long projectId);
    
    Optional<CodeDocument> findByProjectIdAndFilePath(Long projectId, String filePath);
}
