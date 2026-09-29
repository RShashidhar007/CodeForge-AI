package com.codeforge.repository;

import com.codeforge.entity.TaskPatch;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for TaskPatch entity
 */
@Repository
public interface TaskPatchRepository extends JpaRepository<TaskPatch, Long> {
    List<TaskPatch> findByTaskId(Long taskId);
}
