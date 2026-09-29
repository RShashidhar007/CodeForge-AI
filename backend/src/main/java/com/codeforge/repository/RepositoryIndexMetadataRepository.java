package com.codeforge.repository;

import com.codeforge.entity.RepositoryIndexMetadata;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Repository for RepositoryIndexMetadata entity
 */
@Repository
public interface RepositoryIndexMetadataRepository extends JpaRepository<RepositoryIndexMetadata, Long> {
    Optional<RepositoryIndexMetadata> findByProjectId(Long projectId);
}
