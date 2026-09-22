package com.codeforge.repository;

import com.codeforge.entity.AgentExecution;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for AgentExecution entity
 */
@Repository
public interface AgentExecutionRepository extends JpaRepository<AgentExecution, Long> {
    List<AgentExecution> findByTaskIdOrderBySequenceOrder(Long taskId);
}
