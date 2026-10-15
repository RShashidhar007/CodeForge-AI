package com.codeforge.repository;

import com.codeforge.entity.TaskWorkspace;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface TaskWorkspaceRepository extends JpaRepository<TaskWorkspace, Long> {
    Optional<TaskWorkspace> findByAiTaskId(Long aiTaskId);
}
