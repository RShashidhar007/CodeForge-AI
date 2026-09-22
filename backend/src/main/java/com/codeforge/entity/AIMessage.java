package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

/**
 * AI message entity for conversation history
 */
@Entity
@Table(name = "ai_messages", indexes = {
    @Index(columnList = "conversation_id")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"conversation"})
@ToString(exclude = {"conversation"})
public class AIMessage {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "conversation_id", nullable = false)
    private AIConversation conversation;
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String content;
    
    @Column(length = 10, nullable = false)
    @Enumerated(EnumType.STRING)
    private MessageRole role; // USER, ASSISTANT
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    public enum MessageRole {
        USER, ASSISTANT
    }
}
