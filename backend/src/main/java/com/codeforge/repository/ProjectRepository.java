package com.codeforge.repository;

import com.codeforge.entity.Project;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for Project entity
 */
@Repository
public interface ProjectRepository extends JpaRepository<Project, Long> {
    Page<Project> findByCompanyId(Long companyId, Pageable pageable);
    
    List<Project> findByCompanyId(Long companyId);
}
