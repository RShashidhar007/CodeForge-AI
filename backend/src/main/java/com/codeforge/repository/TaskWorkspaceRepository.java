package com.codeforge.repository;

import com.codeforge.entity.TaskWorkspace;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * Repository for TaskWorkspace entity
 */
@Repository
public interface TaskWorkspaceRepository extends JpaRepository<TaskWorkspace, Long> {
    Optional<TaskWorkspace> findByTaskId(Long taskId);
}
