package com.codeforge.repository;

import com.codeforge.entity.TaskApproval;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for TaskApproval entity
 */
@Repository
public interface TaskApprovalRepository extends JpaRepository<TaskApproval, Long> {
    List<TaskApproval> findByTaskId(Long taskId);
}
