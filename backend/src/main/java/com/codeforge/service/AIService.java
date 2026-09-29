package com.codeforge.service;

import com.codeforge.dto.request.ChatRequest;
import com.codeforge.dto.request.CodeAnalysisRequest;
import com.codeforge.dto.response.ChatResponse;
import com.codeforge.dto.response.CodeAnalysisResponse;
import com.codeforge.dto.response.IndexStatusResponse;
import com.codeforge.entity.AIConversation;
import com.codeforge.entity.AIMessage;
import com.codeforge.entity.CodeChunk;
import com.codeforge.entity.Project;
import com.codeforge.entity.RepositoryIndexMetadata;
import com.codeforge.exception.ResourceNotFoundException;
import com.codeforge.repository.AIConversationRepository;
import com.codeforge.repository.AIMessageRepository;
import com.codeforge.repository.CodeChunkRepository;
import com.codeforge.repository.ProjectRepository;
import com.codeforge.repository.RepositoryIndexMetadataRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

/**
 * Service for AI/RAG operations
 * Handles chat, code analysis, and semantic search
 */
@Service
@RequiredArgsConstructor
public class AIService {
    
    private final ProjectRepository projectRepository;
    private final AIConversationRepository conversationRepository;
    private final AIMessageRepository messageRepository;
    private final CodeChunkRepository codeChunkRepository;
    private final RepositoryIndexMetadataRepository indexMetadataRepository;
    
    /**
     * Chat with AI about project code
     */
    @Transactional
    public ChatResponse chat(Long projectId, ChatRequest request) {
        Project project = projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        // Get or create conversation
        AIConversation conversation;
        if (request.getConversationId() != null) {
            conversation = conversationRepository.findById(request.getConversationId())
                .orElseThrow(() -> ResourceNotFoundException.notFound("Conversation", "id", request.getConversationId()));
        } else {
            conversation = AIConversation.builder()
                .project(project)
                .title("Chat")
                .build();
            conversation = conversationRepository.save(conversation);
        }
        
        // Save user message
        AIMessage userMessage = AIMessage.builder()
            .conversation(conversation)
            .content(request.getQuestion())
            .role(AIMessage.MessageRole.USER)
            .build();
        messageRepository.save(userMessage);
        
        // Semantic search for relevant code chunks
        List<CodeChunk> relevantChunks = codeChunkRepository.findByDocumentProjectId(projectId);
        
        // Build context from relevant chunks
        StringBuilder context = new StringBuilder();
        for (CodeChunk chunk : relevantChunks) {
            context.append("File: ").append(chunk.getDocument().getFilePath())
                .append("\n")
                .append("Lines ").append(chunk.getStartLine()).append("-").append(chunk.getEndLine())
                .append("\n")
                .append(chunk.getContent())
                .append("\n\n");
        }
        
        // For now, return mock response
        // TODO: Integrate with LLM provider
        String answer = "This is a mock response to: " + request.getQuestion();
        
        // Save assistant message
        AIMessage assistantMessage = AIMessage.builder()
            .conversation(conversation)
            .content(answer)
            .role(AIMessage.MessageRole.ASSISTANT)
            .build();
        messageRepository.save(assistantMessage);
        
        // Build response
        List<ChatResponse.SourceReference> sources = new ArrayList<>();
        for (CodeChunk chunk : relevantChunks.stream().limit(5).toList()) {
            sources.add(ChatResponse.SourceReference.builder()
                .file(chunk.getDocument().getFilePath())
                .startLine(chunk.getStartLine())
                .endLine(chunk.getEndLine())
                .symbol(chunk.getSymbol())
                .build());
        }
        
        return ChatResponse.builder()
            .conversationId(conversation.getId())
            .answer(answer)
            .sources(sources)
            .chunksRetrieved(relevantChunks.size())
            .build();
    }
    
    /**
     * Get conversation history
     */
    public ChatResponse getConversationHistory(Long projectId, Long conversationId) {
        Project project = projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        AIConversation conversation = conversationRepository.findById(conversationId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Conversation", "id", conversationId));
        
        List<AIMessage> messages = messageRepository.findByConversationIdOrderByCreatedAtAsc(conversationId);
        
        // Return last assistant message as answer
        String lastAnswer = messages.stream()
            .filter(m -> m.getRole() == AIMessage.MessageRole.ASSISTANT)
            .map(AIMessage::getContent)
            .reduce((first, second) -> second)
            .orElse("");
        
        return ChatResponse.builder()
            .conversationId(conversation.getId())
            .answer(lastAnswer)
            .sources(new ArrayList<>())
            .chunksRetrieved(0)
            .build();
    }
    
    /**
     * Explain code
     */
    public CodeAnalysisResponse explainCode(Long projectId, CodeAnalysisRequest request) {
        projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        // TODO: Integrate with LLM provider
        String explanation = "Mock explanation for code from " + request.getFilepath() + 
                           " lines " + request.getStartLine() + "-" + request.getEndLine();
        
        return CodeAnalysisResponse.builder()
            .explanation(explanation)
            .sources(new ArrayList<>())
            .build();
    }
    
    /**
     * Detect bugs in code
     */
    public CodeAnalysisResponse detectBugs(Long projectId, CodeAnalysisRequest request) {
        projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        // TODO: Integrate with LLM provider
        String analysis = "Mock bug detection for code from " + request.getFilepath();
        
        return CodeAnalysisResponse.builder()
            .analysis(analysis)
            .sources(new ArrayList<>())
            .build();
    }
    
    /**
     * Improve code
     */
    public CodeAnalysisResponse improveCode(Long projectId, CodeAnalysisRequest request) {
        projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        // TODO: Integrate with LLM provider
        String suggestions = "Mock suggestions for improving code from " + request.getFilepath();
        
        return CodeAnalysisResponse.builder()
            .suggestions(suggestions)
            .sources(new ArrayList<>())
            .build();
    }
    
    /**
     * Generate tests
     */
    public CodeAnalysisResponse generateTests(Long projectId, CodeAnalysisRequest request) {
        projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        // TODO: Integrate with LLM provider
        String tests = "Mock tests generated for code from " + request.getFilepath();
        
        return CodeAnalysisResponse.builder()
            .tests(tests)
            .testFramework(request.getTestFramework() != null ? request.getTestFramework() : "jest")
            .sources(new ArrayList<>())
            .build();
    }
    
    /**
     * Get repository indexing status
     */
    public IndexStatusResponse getIndexStatus(Long projectId) {
        Project project = projectRepository.findById(projectId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
        
        RepositoryIndexMetadata metadata = indexMetadataRepository.findByProjectId(projectId)
            .orElseGet(() -> RepositoryIndexMetadata.builder()
                .project(project)
                .totalFiles(0)
                .indexedFiles(0)
                .totalChunks(0)
                .progress(0.0)
                .build());
        
        return IndexStatusResponse.builder()
            .status(metadata.getProgress() >= 1.0 ? "completed" : "processing")
            .totalFiles(metadata.getTotalFiles())
            .indexedFiles(metadata.getIndexedFiles())
            .totalChunks(metadata.getTotalChunks())
            .progress(metadata.getProgress())
            .lastIndexedAt(metadata.getLastIndexedAt() != null ? metadata.getLastIndexedAt().toString() : null)
            .lastError(metadata.getLastError())
            .build();
    }
}
