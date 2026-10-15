package com.codeforge.service.github;

import com.codeforge.config.AppProperties;
import com.codeforge.entity.GithubToken;
import com.codeforge.entity.User;
import com.codeforge.exception.GithubApiException;
import com.codeforge.exception.ResourceNotFoundException;
import com.codeforge.repository.GithubTokenRepository;
import com.codeforge.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;

/**
 * Service for handling GitHub OAuth authentication
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class GithubOAuthService {
    
    private final AppProperties appProperties;
    private final GithubTokenRepository githubTokenRepository;
    private final UserRepository userRepository;
    private final WebClient.Builder webClientBuilder;
    
    private static final String GITHUB_OAUTH_URL = "https://github.com/login/oauth/authorize";
    private static final String GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token";
    private static final String GITHUB_API_URL = "https://api.github.com";
    
    /**
     * Generate GitHub OAuth authorization URL
     */
    public String generateAuthorizationUrl(String state) {
        return String.format("%s?client_id=%s&redirect_uri=%s&scope=repo,read:user&state=%s",
            GITHUB_OAUTH_URL,
            appProperties.getGithub().getClientId(),
            appProperties.getGithub().getOauthCallbackUrl(),
            state);
    }
    
    /**
     * Exchange OAuth authorization code for access token
     */
    public String exchangeCodeForToken(String code) {
        try {
            Map<String, Object> response = webClientBuilder.build()
                .post()
                .uri(GITHUB_TOKEN_URL)
                .header("Accept", "application/json")
                .bodyValue(Map.of(
                    "client_id", appProperties.getGithub().getClientId(),
                    "client_secret", appProperties.getGithub().getClientSecret(),
                    "code", code
                ))
                .retrieve()
                .bodyToMono(Map.class)
                .block();
            
            if (response == null || !response.containsKey("access_token")) {
                throw new GithubApiException("Failed to exchange code for token");
            }
            
            String token = (String) response.get("access_token");
            log.info("Successfully exchanged GitHub OAuth code for token");
            return token;
            
        } catch (Exception e) {
            log.error("Failed to exchange GitHub OAuth code: {}", e.getMessage());
            throw new GithubApiException("Failed to exchange authorization code", e);
        }
    }
    
    /**
     * Fetch GitHub user profile using access token
     */
    public Map<String, Object> getUserProfile(String token) {
        try {
            Map<String, Object> profile = webClientBuilder.build()
                .get()
                .uri(GITHUB_API_URL + "/user")
                .header("Authorization", "Bearer " + token)
                .header("Accept", "application/json")
                .retrieve()
                .bodyToMono(Map.class)
                .block();
            
            if (profile != null && profile.containsKey("login")) {
                log.info("Fetched GitHub user profile for: {}", profile.get("login"));
            }
            return profile;
            
        } catch (Exception e) {
            log.error("Failed to fetch GitHub user profile: {}", e.getMessage());
            throw new GithubApiException("Failed to fetch user profile", e);
        }
    }
    
    /**
     * Save or update GitHub token for a user
     */
    @Transactional
    public GithubToken saveOrUpdateGithubToken(Long userId, String token, String username) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("User", "id", userId));
        
        GithubToken githubToken = githubTokenRepository
            .findByUserIdAndUsername(userId, username)
            .orElse(GithubToken.builder()
                .user(user)
                .username(username)
                .build());
        
        githubToken.setToken(token);
        GithubToken saved = githubTokenRepository.save(githubToken);
        
        log.info("Saved GitHub token for user {} and GitHub username {}", userId, username);
        return saved;
    }
    
    /**
     * Get GitHub token for a user
     */
    public GithubToken getGithubToken(Long userId) {
        return githubTokenRepository.findByUserId(userId).stream()
            .findFirst()
            .orElseThrow(() -> new ResourceNotFoundException("GitHub token not found for user " + userId));
    }
    
    /**
     * Delete GitHub token for a user
     */
    @Transactional
    public void deleteGithubToken(Long userId) {
        githubTokenRepository.findByUserId(userId).forEach(githubTokenRepository::delete);
        log.info("Deleted GitHub token(s) for user {}", userId);
    }
}
