package com.codeforge.repository;

import com.codeforge.entity.AIMessage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repository for AIMessage entity
 */
@Repository
public interface AIMessageRepository extends JpaRepository<AIMessage, Long> {
    List<AIMessage> findByConversationId(Long conversationId);
    
    List<AIMessage> findByConversationIdOrderByCreatedAtAsc(Long conversationId);
}
