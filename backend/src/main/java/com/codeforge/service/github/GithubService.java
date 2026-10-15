package com.codeforge.service.github;

import com.codeforge.exception.GithubApiException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.kohsuke.github.*;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Service for GitHub API operations (repository listing, content fetching)
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class GithubService {
    
    /**
     * List repositories for the authenticated user
     */
    public List<Map<String, Object>> listRepositories(String accessToken) {
        try {
            GitHub github = new GitHubBuilder().withOAuthToken(accessToken).build();
            checkRateLimit(github);
            
            return github.getMyself().listRepositories().toList().stream()
                .map(repo -> {
                    try {
                        return Map.<String, Object>of(
                            "name", repo.getName(),
                            "fullName", repo.getFullName(),
                            "description", repo.getDescription() != null ? repo.getDescription() : "",
                            "private", repo.isPrivate(),
                            "url", repo.getHtmlUrl().toString(),
                            "language", repo.getLanguage() != null ? repo.getLanguage() : "Unknown",
                            "stars", repo.getStargazersCount(),
                            "updatedAt", repo.getUpdatedAt()
                        );
                    } catch (IOException e) {
                        log.warn("Failed to get details for repo: {}", repo.getName());
                        return null;
                    }
                })
                .filter(Objects::nonNull)
                .collect(Collectors.toList());
            
        } catch (IOException e) {
            log.error("Failed to list GitHub repositories: {}", e.getMessage());
            throw new GithubApiException("Failed to list repositories", e);
        }
    }
    
    /**
     * Fetch repository content (all files)
     */
    public Map<String, String> fetchRepositoryContent(String accessToken, String owner, String repo) {
        try {
            GitHub github = new GitHubBuilder().withOAuthToken(accessToken).build();
            checkRateLimit(github);
            
            GHRepository repository = github.getRepository(owner + "/" + repo);
            Map<String, String> files = new HashMap<>();
            
            // Fetch from root directory
            fetchDirectoryContents(repository, "", files);
            
            log.info("Fetched {} files from {}/{}", files.size(), owner, repo);
            return files;
            
        } catch (IOException e) {
            log.error("Failed to fetch repository content from {}/{}: {}", owner, repo, e.getMessage());
            throw new GithubApiException("Failed to fetch repository content", e);
        }
    }
    
    /**
     * Recursively fetch directory contents
     */
    private void fetchDirectoryContents(GHRepository repository, String path, Map<String, String> files) throws IOException {
        try {
            List<GHContent> contents = repository.getDirectoryContent(path);
            
            for (GHContent content : contents) {
                if (content.isFile()) {
                    try {
                        // Skip large files (>1MB)
                        if (content.getSize() > 1024 * 1024) {
                            log.debug("Skipping large file: {} ({}KB)", content.getPath(), content.getSize() / 1024);
                            continue;
                        }
                        
                        String fileContent = content.getContent();
                        if (fileContent != null) {
                            files.put(content.getPath(), fileContent);
                        }
                    } catch (IOException e) {
                        log.warn("Failed to fetch content for {}: {}", content.getPath(), e.getMessage());
                    }
                } else if (content.isDirectory()) {
                    // Skip common directories
                    String dirName = content.getName();
                    if (dirName.equals("node_modules") || dirName.equals(".git") || 
                        dirName.equals("vendor") || dirName.equals("target") ||
                        dirName.equals("build") || dirName.equals("dist")) {
                        log.debug("Skipping directory: {}", content.getPath());
                        continue;
                    }
                    
                    fetchDirectoryContents(repository, content.getPath(), files);
                }
            }
        } catch (IOException e) {
            log.warn("Failed to read directory {}: {}", path, e.getMessage());
        }
    }
    
    /**
     * Check GitHub API rate limit
     */
    private void checkRateLimit(GitHub github) throws IOException {
        GHRateLimit.Record rateLimit = github.getRateLimit().getCore();
        log.debug("GitHub API rate limit: {}/{} remaining", rateLimit.getRemaining(), rateLimit.getLimit());
        
        if (rateLimit.getRemaining() < 10) {
            throw new GithubApiException(
                String.format("GitHub API rate limit nearly exhausted: %d/%d remaining. Resets at: %s",
                    rateLimit.getRemaining(), 
                    rateLimit.getLimit(),
                    rateLimit.getResetDate()));
        }
    }
    
    /**
     * Get repository information
     */
    public Map<String, Object> getRepositoryInfo(String accessToken, String owner, String repo) {
        try {
            GitHub github = new GitHubBuilder().withOAuthToken(accessToken).build();
            GHRepository repository = github.getRepository(owner + "/" + repo);
            
            return Map.of(
                "name", repository.getName(),
                "fullName", repository.getFullName(),
                "description", repository.getDescription() != null ? repository.getDescription() : "",
                "private", repository.isPrivate(),
                "url", repository.getHtmlUrl().toString(),
                "language", repository.getLanguage() != null ? repository.getLanguage() : "Unknown",
                "stars", repository.getStargazersCount(),
                "forks", repository.getForksCount(),
                "defaultBranch", repository.getDefaultBranch()
            );
            
        } catch (IOException e) {
            log.error("Failed to get repository info for {}/{}: {}", owner, repo, e.getMessage());
            throw new GithubApiException("Failed to get repository information", e);
        }
    }
}
