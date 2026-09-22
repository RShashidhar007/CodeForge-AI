package com.codeforge.repository;

import com.codeforge.entity.AITask;
import com.codeforge.entity.AITask.TaskStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for AITask entity
 */
@Repository
public interface AITaskRepository extends JpaRepository<AITask, Long> {
    Page<AITask> findByProjectId(Long projectId, Pageable pageable);
    
    List<AITask> findByProjectId(Long projectId);
    
    Page<AITask> findByProjectIdAndStatus(Long projectId, TaskStatus status, Pageable pageable);
}
