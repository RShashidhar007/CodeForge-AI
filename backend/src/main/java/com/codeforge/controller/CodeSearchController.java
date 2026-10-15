package com.codeforge.controller;

import com.codeforge.dto.request.SemanticSearchRequest;
import com.codeforge.dto.response.SemanticSearchResponse;
import com.codeforge.entity.CodeChunk;
import com.codeforge.repository.CodeChunkRepository;
import com.codeforge.security.SecurityUser;
import com.codeforge.service.vector.VectorStoreService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Controller for semantic code search operations
 */
@RestController
@RequestMapping("/code/search")
@RequiredArgsConstructor
@Slf4j
public class CodeSearchController {
    
    private final VectorStoreService vectorStoreService;
    private final CodeChunkRepository codeChunkRepository;
    
    /**
     * Perform semantic search on code
     */
    @PostMapping
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<SemanticSearchResponse> search(
            @AuthenticationPrincipal SecurityUser currentUser,
            @Valid @RequestBody SemanticSearchRequest request) {
        
        log.info("Semantic search query: '{}' for project {}", request.getQuery(), request.getProjectId());
        
        // Perform vector search
        List<VectorStoreService.SearchResult> searchResults = vectorStoreService.search(
            request.getQuery(),
            request.getProjectId(),
            request.getLimit()
        );
        
        // Enrich results with actual code content
        List<SemanticSearchResponse.SearchResultItem> items = searchResults.stream()
            .map(result -> {
                CodeChunk chunk = codeChunkRepository.findById(result.getChunkId()).orElse(null);
                
                return SemanticSearchResponse.SearchResultItem.builder()
                    .chunkId(result.getChunkId())
                    .filePath(result.getFilePath())
                    .startLine(result.getStartLine())
                    .endLine(result.getEndLine())
                    .symbol(result.getSymbol())
                    .score(result.getScore())
                    .content(chunk != null ? chunk.getContent() : "")
                    .build();
            })
            .collect(Collectors.toList());
        
        SemanticSearchResponse response = SemanticSearchResponse.builder()
            .results(items)
            .totalResults(items.size())
            .build();
        
        return ResponseEntity.ok(response);
    }
}
