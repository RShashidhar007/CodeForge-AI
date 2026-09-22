package com.codeforge.repository;

import com.codeforge.entity.File;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for File entity
 */
@Repository
public interface FileRepository extends JpaRepository<File, Long> {
    List<File> findByProjectId(Long projectId);
}
