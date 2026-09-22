package com.codeforge.repository;

import com.codeforge.entity.TaskTestResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for TaskTestResult entity
 */
@Repository
public interface TaskTestResultRepository extends JpaRepository<TaskTestResult, Long> {
    List<TaskTestResult> findByTaskId(Long taskId);
}
