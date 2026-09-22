package com.codeforge.controller;

import com.codeforge.dto.request.ChatRequest;
import com.codeforge.dto.request.CodeAnalysisRequest;
import com.codeforge.dto.response.ChatResponse;
import com.codeforge.dto.response.CodeAnalysisResponse;
import com.codeforge.dto.response.IndexStatusResponse;
import com.codeforge.service.AIService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

/**
 * AI controller
 * Endpoints:
 * - POST /v1/projects/{projectId}/ai/chat
 * - POST /v1/projects/{projectId}/ai/explain
 * - POST /v1/projects/{projectId}/ai/bugs
 * - POST /v1/projects/{projectId}/ai/improve
 * - POST /v1/projects/{projectId}/ai/tests
 * - GET /v1/projects/{projectId}/ai/status
 * - GET /v1/projects/{projectId}/ai/conversations/{conversationId}/history
 */
@RestController
@RequestMapping("/v1/projects/{projectId}/ai")
@RequiredArgsConstructor
public class AIController {
    
    private final AIService aiService;
    
    /**
     * Chat with AI about project code
     * POST /v1/projects/{projectId}/ai/chat
     */
    @PostMapping("/chat")
    public ResponseEntity<ChatResponse> chat(
            @PathVariable Long projectId,
            @Valid @RequestBody ChatRequest request,
            @AuthenticationPrincipal UserDetails user) {
        ChatResponse response = aiService.chat(projectId, request);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Explain code
     * POST /v1/projects/{projectId}/ai/explain
     */
    @PostMapping("/explain")
    public ResponseEntity<CodeAnalysisResponse> explainCode(
            @PathVariable Long projectId,
            @Valid @RequestBody CodeAnalysisRequest request,
            @AuthenticationPrincipal UserDetails user) {
        CodeAnalysisResponse response = aiService.explainCode(projectId, request);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Detect bugs in code
     * POST /v1/projects/{projectId}/ai/bugs
     */
    @PostMapping("/bugs")
    public ResponseEntity<CodeAnalysisResponse> detectBugs(
            @PathVariable Long projectId,
            @Valid @RequestBody CodeAnalysisRequest request,
            @AuthenticationPrincipal UserDetails user) {
        CodeAnalysisResponse response = aiService.detectBugs(projectId, request);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Improve code
     * POST /v1/projects/{projectId}/ai/improve
     */
    @PostMapping("/improve")
    public ResponseEntity<CodeAnalysisResponse> improveCode(
            @PathVariable Long projectId,
            @Valid @RequestBody CodeAnalysisRequest request,
            @AuthenticationPrincipal UserDetails user) {
        CodeAnalysisResponse response = aiService.improveCode(projectId, request);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Generate tests
     * POST /v1/projects/{projectId}/ai/tests
     */
    @PostMapping("/tests")
    public ResponseEntity<CodeAnalysisResponse> generateTests(
            @PathVariable Long projectId,
            @Valid @RequestBody CodeAnalysisRequest request,
            @AuthenticationPrincipal UserDetails user) {
        CodeAnalysisResponse response = aiService.generateTests(projectId, request);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Get repository indexing status
     * GET /v1/projects/{projectId}/ai/status
     */
    @GetMapping("/status")
    public ResponseEntity<IndexStatusResponse> getIndexStatus(
            @PathVariable Long projectId,
            @AuthenticationPrincipal UserDetails user) {
        IndexStatusResponse response = aiService.getIndexStatus(projectId);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Get conversation history
     * GET /v1/projects/{projectId}/ai/conversations/{conversationId}/history
     */
    @GetMapping("/conversations/{conversationId}/history")
    public ResponseEntity<ChatResponse> getConversationHistory(
            @PathVariable Long projectId,
            @PathVariable Long conversationId,
            @AuthenticationPrincipal UserDetails user) {
        ChatResponse response = aiService.getConversationHistory(projectId, conversationId);
        return ResponseEntity.ok(response);
    }
}
