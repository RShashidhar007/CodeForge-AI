package com.codeforge.controller;

import com.codeforge.dto.request.GithubOAuthCallbackRequest;
import com.codeforge.dto.request.ImportRepositoryRequest;
import com.codeforge.dto.response.GithubOAuthUrlResponse;
import com.codeforge.dto.response.GithubRepositoryResponse;
import com.codeforge.dto.response.ImportStatusResponse;
import com.codeforge.entity.GithubToken;
import com.codeforge.security.SecurityUser;
import com.codeforge.service.github.GithubOAuthService;
import com.codeforge.service.github.GithubService;
import com.codeforge.service.github.RepositoryImportService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Controller for GitHub integration operations
 */
@RestController
@RequestMapping("/github")
@RequiredArgsConstructor
@Slf4j
public class GithubController {
    
    private final GithubOAuthService githubOAuthService;
    private final GithubService githubService;
    private final RepositoryImportService repositoryImportService;
    
    /**
     * Get GitHub OAuth authorization URL
     */
    @GetMapping("/oauth/authorize")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<GithubOAuthUrlResponse> getAuthorizationUrl(@AuthenticationPrincipal SecurityUser currentUser) {
        String state = UUID.randomUUID().toString();
        String authUrl = githubOAuthService.generateAuthorizationUrl(state);
        
        return ResponseEntity.ok(GithubOAuthUrlResponse.builder()
            .authorizationUrl(authUrl)
            .state(state)
            .build());
    }
    
    /**
     * Handle GitHub OAuth callback
     */
    @PostMapping("/oauth/callback")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Map<String, String>> handleOAuthCallback(
            @AuthenticationPrincipal SecurityUser currentUser,
            @Valid @RequestBody GithubOAuthCallbackRequest request) {
        
        // Exchange code for token
        String accessToken = githubOAuthService.exchangeCodeForToken(request.getCode());
        
        // Get GitHub user profile
        Map<String, Object> profile = githubOAuthService.getUserProfile(accessToken);
        String githubUsername = (String) profile.get("login");
        
        // Save token
        githubOAuthService.saveOrUpdateGithubToken(currentUser.getUserId(), accessToken, githubUsername);
        
        log.info("User {} linked GitHub account: {}", currentUser.getUserId(), githubUsername);
        
        return ResponseEntity.ok(Map.of(
            "message", "GitHub account linked successfully",
            "username", githubUsername
        ));
    }
    
    /**
     * List user's GitHub repositories
     */
    @GetMapping("/repositories")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<List<GithubRepositoryResponse>> listRepositories(@AuthenticationPrincipal SecurityUser currentUser) {
        GithubToken token = githubOAuthService.getGithubToken(currentUser.getUserId());
        
        List<Map<String, Object>> repos = githubService.listRepositories(token.getToken());
        
        List<GithubRepositoryResponse> response = repos.stream()
            .map(repo -> GithubRepositoryResponse.builder()
                .name((String) repo.get("name"))
                .fullName((String) repo.get("fullName"))
                .description((String) repo.get("description"))
                .isPrivate((Boolean) repo.get("private"))
                .url((String) repo.get("url"))
                .language((String) repo.get("language"))
                .stars((Integer) repo.get("stars"))
                .updatedAt(repo.get("updatedAt"))
                .build())
            .collect(Collectors.toList());
        
        return ResponseEntity.ok(response);
    }
    
    /**
     * Import a GitHub repository
     */
    @PostMapping("/import")
    @PreAuthorize("hasAnyRole('RECRUITER', 'ADMIN')")
    public ResponseEntity<Map<String, String>> importRepository(
            @AuthenticationPrincipal SecurityUser currentUser,
            @Valid @RequestBody ImportRepositoryRequest request) {
        
        GithubToken token = githubOAuthService.getGithubToken(currentUser.getUserId());
        
        // Start async import
        repositoryImportService.importRepositoryAsync(
            request.getProjectId(),
            token.getToken(),
            request.getOwner(),
            request.getRepo()
        );
        
        log.info("Started import of {}/{} for project {}", 
            request.getOwner(), request.getRepo(), request.getProjectId());
        
        return ResponseEntity.accepted().body(Map.of(
            "message", "Repository import started",
            "projectId", request.getProjectId().toString()
        ));
    }
    
    /**
     * Get import status
     */
    @GetMapping("/import/{projectId}/status")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<ImportStatusResponse> getImportStatus(@PathVariable Long projectId) {
        RepositoryImportService.ImportStatus status = repositoryImportService.getImportStatus(projectId);
        
        if (status == null) {
            return ResponseEntity.notFound().build();
        }
        
        // Calculate progress percentage
        int progress = 0;
        if (status.getRelevantFiles() > 0) {
            progress = (int) ((status.getProcessedFiles() * 100.0) / status.getRelevantFiles());
        }
        
        ImportStatusResponse response = ImportStatusResponse.builder()
            .projectId(status.getProjectId())
            .status(status.getStatus())
            .currentStep(status.getCurrentStep())
            .totalFiles(status.getTotalFiles())
            .relevantFiles(status.getRelevantFiles())
            .processedFiles(status.getProcessedFiles())
            .totalChunks(status.getTotalChunks())
            .embeddedChunks(status.getEmbeddedChunks())
            .error(status.getError())
            .startTime(status.getStartTime())
            .endTime(status.getEndTime())
            .progressPercentage(progress)
            .build();
        
        return ResponseEntity.ok(response);
    }
    
    /**
     * Delete GitHub token (unlink account)
     */
    @DeleteMapping("/tokens")
    @PreAuthorize("isAuthenticated()")
    public ResponseEntity<Map<String, String>> deleteGithubToken(@AuthenticationPrincipal SecurityUser currentUser) {
        githubOAuthService.deleteGithubToken(currentUser.getUserId());
        
        log.info("User {} unlinked GitHub account", currentUser.getUserId());
        
        return ResponseEntity.ok(Map.of("message", "GitHub account unlinked successfully"));
    }
}
