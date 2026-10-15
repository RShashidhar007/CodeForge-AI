# Phase 3 Implementation Plan: GitHub OAuth Integration & Qdrant Vector Database RAG

## Overview
Phase 3 adds GitHub OAuth integration for repository access and Qdrant vector database for semantic code search (RAG). This builds on top of Phase 1 (core platform) and Phase 2 (rate limiting) to enable AI-powered code analysis over imported GitHub repositories.

## Build & Test Commands
- **Build**: `cd backend && mvn clean compile` (from d:\projects\CodeForge-AI-main)
- **Test**: `cd backend && mvn test`
- **Run**: `cd backend && mvn spring-boot:run`

## Implementation Steps

- [ ] 1. **Add Maven dependencies for Qdrant client and GitHub API**
      
      Add `io.qdrant:client:1.7.4` and `org.kohsuke:github-api:1.321` to pom.xml dependencies section.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\pom.xml
      
      **Details**:
      ```xml
      <!-- Qdrant Vector Database Client -->
      <dependency>
          <groupId>io.qdrant</groupId>
          <artifactId>client</artifactId>
          <version>1.7.4</version>
      </dependency>
      
      <!-- GitHub API Client -->
      <dependency>
          <groupId>org.kohsuke</groupId>
          <artifactId>github-api</artifactId>
          <version>1.321</version>
      </dependency>
      ```
      
      **Verify**: `cd backend && mvn dependency:resolve` — dependencies download without errors

- [ ] 2. **Update AppProperties.java to add GitHub and Qdrant configuration**
      
      Add two new nested static classes: `GitHub` (clientId, clientSecret, oauthCallbackUrl) and `Qdrant` (host default "localhost", port default 6334, apiKey optional, collectionName default "code_embeddings"). Initialize them in AppProperties similar to existing Jwt, Cors, Admin, Ai fields.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\config\AppProperties.java
      
      **Details**:
      ```java
      private final Github github = new Github();
      private final Qdrant qdrant = new Qdrant();
      
      @Data
      public static class Github {
          private String clientId;
          private String clientSecret;
          private String oauthCallbackUrl;
      }
      
      @Data
      public static class Qdrant {
          private String host = "localhost";
          private int port = 6334;
          private String apiKey;
          private String collectionName = "code_embeddings";
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 3. **Update application.properties with GitHub and Qdrant property mappings**
      
      Add property mappings for GitHub OAuth (app.github.client-id, app.github.client-secret, app.github.oauth-callback-url) and Qdrant (app.qdrant.host, app.qdrant.port, app.qdrant.api-key, app.qdrant.collection-name) with environment variable substitutions.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\resources\application.properties
      
      **Details**:
      Add section after AI configuration:
      ```properties
      # ===========================
      # GitHub OAuth Configuration
      # ===========================
      app.github.client-id=${GITHUB_CLIENT_ID:}
      app.github.client-secret=${GITHUB_CLIENT_SECRET:}
      app.github.oauth-callback-url=${GITHUB_OAUTH_CALLBACK_URL:http://localhost:5173/github/callback}
      
      # ===========================
      # Qdrant Vector Database Configuration
      # ===========================
      app.qdrant.host=${QDRANT_HOST:localhost}
      app.qdrant.port=${QDRANT_PORT:6334}
      app.qdrant.api-key=${QDRANT_API_KEY:}
      app.qdrant.collection-name=${QDRANT_COLLECTION_NAME:code_embeddings}
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 4. **Create .env.example file for environment variables**
      
      Create .env.example at project root (d:\projects\CodeForge-AI-main\.env.example) documenting all environment variables including new GitHub and Qdrant variables. Base on existing application.properties defaults.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\.env.example
      
      **Details**:
      ```bash
      # Database
      DB_HOST=localhost
      DB_PORT=1433
      DB_NAME=recruitment_platform
      DB_USERNAME=sa
      DB_PASSWORD=Admin@123456
      
      # Redis
      REDIS_HOST=localhost
      REDIS_PORT=6379
      
      # JWT
      JWT_SECRET=your-secret-key-must-be-at-least-32-characters-long-change-in-production
      JWT_EXPIRATION_SECONDS=86400
      
      # CORS
      CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
      
      # Admin Bootstrap
      ADMIN_EMAIL=admin@example.com
      ADMIN_PASSWORD=Admin123!
      ADMIN_NAME=Platform Admin
      
      # AI/LLM
      LLM_PROVIDER=mock
      LLM_MODEL=gpt-4-turbo
      LLM_API_KEY=sk-test-key
      EMBEDDING_PROVIDER=mock
      EMBEDDING_MODEL=text-embedding-3-small
      EMBEDDING_API_KEY=sk-test-key
      
      # GitHub OAuth
      GITHUB_CLIENT_ID=
      GITHUB_CLIENT_SECRET=
      GITHUB_OAUTH_CALLBACK_URL=http://localhost:5173/github/callback
      
      # Qdrant Vector Database
      QDRANT_HOST=localhost
      QDRANT_PORT=6334
      QDRANT_API_KEY=
      QDRANT_COLLECTION_NAME=code_embeddings
      ```
      
      **Verify**: File exists and is readable

- [ ] 5. **Create QdrantConfig.java configuration class**
      
      Create @Configuration class that provides a @Bean for QdrantClient. Connect using QdrantGrpcClient.newBuilder(host, port, false).build() for no-API-key or .withApiKey(apiKey) if apiKey is present. Initialize collection on startup using CollectionsGrpc or QdrantClient.createCollectionAsync() with VectorParams (dimension 1536 to match embedding). Handle connection failures gracefully: log warning and return null bean if Qdrant unavailable (graceful degradation).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\config\QdrantConfig.java
      
      **Details**:
      ```java
      package com.codeforge.config;
      
      import io.qdrant.client.QdrantClient;
      import io.qdrant.client.QdrantGrpcClient;
      import io.qdrant.client.grpc.Collections.VectorParams;
      import io.qdrant.client.grpc.Collections.Distance;
      import lombok.RequiredArgsConstructor;
      import lombok.extern.slf4j.Slf4j;
      import org.springframework.context.annotation.Bean;
      import org.springframework.context.annotation.Configuration;
      
      @Configuration
      @RequiredArgsConstructor
      @Slf4j
      public class QdrantConfig {
          private final AppProperties appProperties;
          
          @Bean
          public QdrantClient qdrantClient() {
              try {
                  QdrantGrpcClient.Builder builder = QdrantGrpcClient.newBuilder(
                      appProperties.getQdrant().getHost(),
                      appProperties.getQdrant().getPort(),
                      false
                  );
                  
                  if (appProperties.getQdrant().getApiKey() != null 
                      && !appProperties.getQdrant().getApiKey().isEmpty()) {
                      builder.withApiKey(appProperties.getQdrant().getApiKey());
                  }
                  
                  QdrantClient client = new QdrantClient(builder.build());
                  
                  // Initialize collection if it doesn't exist
                  String collectionName = appProperties.getQdrant().getCollectionName();
                  initializeCollection(client, collectionName);
                  
                  log.info("Qdrant client initialized successfully: {}:{}", 
                      appProperties.getQdrant().getHost(), 
                      appProperties.getQdrant().getPort());
                  return client;
                  
              } catch (Exception e) {
                  log.warn("Failed to connect to Qdrant at {}:{}. Vector search will be unavailable. Error: {}", 
                      appProperties.getQdrant().getHost(),
                      appProperties.getQdrant().getPort(),
                      e.getMessage());
                  return null;
              }
          }
          
          private void initializeCollection(QdrantClient client, String collectionName) {
              try {
                  // Check if collection exists, create if not
                  VectorParams vectorParams = VectorParams.newBuilder()
                      .setSize(1536)  // text-embedding-3-small dimension
                      .setDistance(Distance.Cosine)
                      .build();
                  
                  client.createCollectionAsync(collectionName, vectorParams).get();
                  log.info("Qdrant collection '{}' initialized", collectionName);
                  
              } catch (Exception e) {
                  // Collection may already exist, which is fine
                  log.debug("Collection initialization: {}", e.getMessage());
              }
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 6. **Create custom exception classes for Phase 3**
      
      Create three new exception classes in exception package: GithubApiException (for GitHub API failures), VectorStoreException (for Qdrant failures), RepositoryImportException (for import orchestration failures). All extend RuntimeException and follow the pattern of existing exceptions (BadCredentialsException, ResourceNotFoundException).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\exception\GithubApiException.java
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\exception\VectorStoreException.java
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\exception\RepositoryImportException.java
      
      **Details**:
      ```java
      // GithubApiException.java
      package com.codeforge.exception;
      
      public class GithubApiException extends RuntimeException {
          public GithubApiException(String message) {
              super(message);
          }
          
          public GithubApiException(String message, Throwable cause) {
              super(message, cause);
          }
      }
      
      // VectorStoreException.java
      package com.codeforge.exception;
      
      public class VectorStoreException extends RuntimeException {
          public VectorStoreException(String message) {
              super(message);
          }
          
          public VectorStoreException(String message, Throwable cause) {
              super(message, cause);
          }
      }
      
      // RepositoryImportException.java
      package com.codeforge.exception;
      
      public class RepositoryImportException extends RuntimeException {
          public RepositoryImportException(String message) {
              super(message);
          }
          
          public RepositoryImportException(String message, Throwable cause) {
              super(message, cause);
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 7. **Update GlobalExceptionHandler to handle new exceptions**
      
      Add @ExceptionHandler methods for GithubApiException (502 Bad Gateway), VectorStoreException (503 Service Unavailable), and RepositoryImportException (500 Internal Server Error). Follow existing pattern in GlobalExceptionHandler.java.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\exception\GlobalExceptionHandler.java
      
      **Details**:
      Add before handleGlobalException():
      ```java
      @ExceptionHandler(GithubApiException.class)
      public ResponseEntity<ErrorResponse> handleGithubApiException(
              GithubApiException ex,
              WebRequest request) {
          
          ErrorResponse error = ErrorResponse.of(
              HttpStatus.BAD_GATEWAY.value(),
              "Bad Gateway",
              "GitHub API error: " + ex.getMessage(),
              request.getDescription(false).replace("uri=", "")
          );
          
          return ResponseEntity.status(HttpStatus.BAD_GATEWAY).body(error);
      }
      
      @ExceptionHandler(VectorStoreException.class)
      public ResponseEntity<ErrorResponse> handleVectorStoreException(
              VectorStoreException ex,
              WebRequest request) {
          
          ErrorResponse error = ErrorResponse.of(
              HttpStatus.SERVICE_UNAVAILABLE.value(),
              "Service Unavailable",
              "Vector store error: " + ex.getMessage(),
              request.getDescription(false).replace("uri=", "")
          );
          
          return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
      }
      
      @ExceptionHandler(RepositoryImportException.class)
      public ResponseEntity<ErrorResponse> handleRepositoryImportException(
              RepositoryImportException ex,
              WebRequest request) {
          
          ErrorResponse error = ErrorResponse.of(
              HttpStatus.INTERNAL_SERVER_ERROR.value(),
              "Internal Server Error",
              "Repository import failed: " + ex.getMessage(),
              request.getDescription(false).replace("uri=", "")
          );
          
          return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 8. **Create GithubOAuthService for GitHub OAuth flow**
      
      Create service in service/github package with methods: generateAuthorizationUrl() (returns GitHub OAuth URL with client_id and redirect_uri), exchangeCodeForToken(code, state) (exchanges authorization code for access token using GitHub OAuth token endpoint), getUserProfile(token) (fetches GitHub user profile), saveOrUpdateGithubToken(userId, token, username) (uses GithubTokenRepository to save/update token for user). Use WebClient (spring-boot-starter-webflux already in pom.xml) for HTTP calls. Mask tokens in logs.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\github\GithubOAuthService.java
      
      **Details**:
      ```java
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
          
          public String generateAuthorizationUrl(String state) {
              return String.format("%s?client_id=%s&redirect_uri=%s&scope=repo,read:user&state=%s",
                  GITHUB_OAUTH_URL,
                  appProperties.getGithub().getClientId(),
                  appProperties.getGithub().getOauthCallbackUrl(),
                  state);
          }
          
          public String exchangeCodeForToken(String code) {
              try {
                  Map<String, String> response = webClientBuilder.build()
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
                  log.info("Successfully exchanged GitHub OAuth code for token (masked)");
                  return token;
                  
              } catch (Exception e) {
                  log.error("Failed to exchange GitHub OAuth code: {}", e.getMessage());
                  throw new GithubApiException("Failed to exchange authorization code", e);
              }
          }
          
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
                  
                  log.info("Fetched GitHub user profile for: {}", profile.get("login"));
                  return profile;
                  
              } catch (Exception e) {
                  log.error("Failed to fetch GitHub user profile: {}", e.getMessage());
                  throw new GithubApiException("Failed to fetch user profile", e);
              }
          }
          
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
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 9. **Create GithubService for GitHub API operations**
      
      Create service in service/github package with methods: listRepositories(accessToken) (fetches user's repos using GitHub class from org.kohsuke:github-api), fetchRepositoryContent(accessToken, owner, repo, path) (recursively fetches file tree), downloadRepositoryZip(accessToken, owner, repo) (downloads ZIP archive). Use GitHub class as entry point: `new GitHubBuilder().withOAuthToken(accessToken).build()`. Handle rate limiting (check rate limit headers, throw GithubApiException if exhausted).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\github\GithubService.java
      
      **Details**:
      ```java
      package com.codeforge.service.github;
      
      import com.codeforge.exception.GithubApiException;
      import lombok.RequiredArgsConstructor;
      import lombok.extern.slf4j.Slf4j;
      import org.kohsuke.github.*;
      import org.springframework.stereotype.Service;
      
      import java.io.IOException;
      import java.util.*;
      import java.util.stream.Collectors;
      
      @Service
      @RequiredArgsConstructor
      @Slf4j
      public class GithubService {
          
          public List<Map<String, Object>> listRepositories(String accessToken) {
              try {
                  GitHub github = new GitHubBuilder().withOAuthToken(accessToken).build();
                  checkRateLimit(github);
                  
                  return github.getMyself().listRepositories().toList().stream()
                      .map(repo -> Map.<String, Object>of(
                          "name", repo.getName(),
                          "fullName", repo.getFullName(),
                          "description", repo.getDescription() != null ? repo.getDescription() : "",
                          "private", repo.isPrivate(),
                          "url", repo.getHtmlUrl().toString(),
                          "language", repo.getLanguage() != null ? repo.getLanguage() : "Unknown",
                          "stars", repo.getStargazersCount()
                      ))
                      .collect(Collectors.toList());
                  
              } catch (IOException e) {
                  log.error("Failed to list GitHub repositories: {}", e.getMessage());
                  throw new GithubApiException("Failed to list repositories", e);
              }
          }
          
          public Map<String, String> fetchRepositoryContent(String accessToken, String owner, String repo) {
              try {
                  GitHub github = new GitHubBuilder().withOAuthToken(accessToken).build();
                  checkRateLimit(github);
                  
                  GHRepository repository = github.getRepository(owner + "/" + repo);
                  Map<String, String> files = new HashMap<>();
                  
                  fetchDirectoryContents(repository, "", files);
                  
                  log.info("Fetched {} files from {}/{}", files.size(), owner, repo);
                  return files;
                  
              } catch (IOException e) {
                  log.error("Failed to fetch repository content from {}/{}: {}", owner, repo, e.getMessage());
                  throw new GithubApiException("Failed to fetch repository content", e);
              }
          }
          
          private void fetchDirectoryContents(GHRepository repository, String path, Map<String, String> files) throws IOException {
              List<GHContent> contents = repository.getDirectoryContent(path);
              
              for (GHContent content : contents) {
                  if (content.isFile()) {
                      try {
                          String fileContent = content.getContent();
                          files.put(content.getPath(), fileContent);
                      } catch (IOException e) {
                          log.warn("Failed to fetch content for {}: {}", content.getPath(), e.getMessage());
                      }
                  } else if (content.isDirectory()) {
                      fetchDirectoryContents(repository, content.getPath(), files);
                  }
              }
          }
          
          private void checkRateLimit(GitHub github) throws IOException {
              GHRateLimit rateLimit = github.getRateLimit().getCore();
              if (rateLimit.getRemaining() < 10) {
                  throw new GithubApiException(
                      String.format("GitHub API rate limit nearly exhausted: %d/%d remaining",
                          rateLimit.getRemaining(), rateLimit.getLimit()));
              }
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 10. **Create CodeProcessingService for code file processing**
      
      Create service in service/code package with methods: processRepository(owner, repo, files) (processes all files in repo), chunkFile(filePath, content) (splits file into logical chunks by function/class boundaries, aim for 100-300 lines per chunk), filterRelevantFiles(files) (filters out binary files, node_modules, .git, build artifacts - keep .java, .js, .ts, .py, .go, .rs, .cpp, .c, .h, .md, .yml, .yaml, .json, .xml), createCodeDocumentAndChunks(project, filePath, content, language) (creates CodeDocument and CodeChunk entities, detects language from extension). Use CodeDocumentRepository and CodeChunkRepository.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\code\CodeProcessingService.java
      
      **Details**:
      ```java
      package com.codeforge.service.code;
      
      import com.codeforge.entity.CodeChunk;
      import com.codeforge.entity.CodeDocument;
      import com.codeforge.entity.Project;
      import com.codeforge.repository.CodeChunkRepository;
      import com.codeforge.repository.CodeDocumentRepository;
      import lombok.RequiredArgsConstructor;
      import lombok.extern.slf4j.Slf4j;
      import org.springframework.stereotype.Service;
      import org.springframework.transaction.annotation.Transactional;
      
      import java.util.*;
      import java.util.regex.Pattern;
      
      @Service
      @RequiredArgsConstructor
      @Slf4j
      public class CodeProcessingService {
          
          private final CodeDocumentRepository codeDocumentRepository;
          private final CodeChunkRepository codeChunkRepository;
          
          private static final Set<String> RELEVANT_EXTENSIONS = Set.of(
              "java", "js", "ts", "jsx", "tsx", "py", "go", "rs", "cpp", "c", "h", "hpp",
              "md", "yml", "yaml", "json", "xml", "sql", "sh", "bash", "rb", "php", "cs"
          );
          
          private static final Pattern BINARY_PATTERN = Pattern.compile("\\.(png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|pdf|zip|tar|gz|exe|dll|so|dylib)$");
          
          public Map<String, String> filterRelevantFiles(Map<String, String> files) {
              Map<String, String> filtered = new HashMap<>();
              
              for (Map.Entry<String, String> entry : files.entrySet()) {
                  String path = entry.getKey();
                  
                  // Skip binary files
                  if (BINARY_PATTERN.matcher(path.toLowerCase()).find()) {
                      continue;
                  }
                  
                  // Skip common ignored directories
                  if (path.contains("node_modules/") || path.contains(".git/") || 
                      path.contains("build/") || path.contains("dist/") ||
                      path.contains("target/") || path.contains(".idea/") ||
                      path.contains("venv/") || path.contains("__pycache__/")) {
                      continue;
                  }
                  
                  // Check if extension is relevant
                  String extension = getFileExtension(path);
                  if (RELEVANT_EXTENSIONS.contains(extension)) {
                      filtered.put(path, entry.getValue());
                  }
              }
              
              log.info("Filtered {} relevant files from {} total", filtered.size(), files.size());
              return filtered;
          }
          
          @Transactional
          public CodeDocument createCodeDocumentAndChunks(Project project, String filePath, String content, String language) {
              // Create document
              CodeDocument document = CodeDocument.builder()
                  .project(project)
                  .filePath(filePath)
                  .fullContent(content)
                  .language(language)
                  .build();
              document = codeDocumentRepository.save(document);
              
              // Create chunks
              List<CodeChunk> chunks = chunkFile(document, content);
              codeChunkRepository.saveAll(chunks);
              
              log.debug("Created document {} with {} chunks", filePath, chunks.size());
              return document;
          }
          
          public List<CodeChunk> chunkFile(CodeDocument document, String content) {
              List<CodeChunk> chunks = new ArrayList<>();
              String[] lines = content.split("\n");
              
              int chunkSize = 200; // Target lines per chunk
              int startLine = 0;
              
              while (startLine < lines.length) {
                  int endLine = Math.min(startLine + chunkSize, lines.length);
                  
                  StringBuilder chunkContent = new StringBuilder();
                  for (int i = startLine; i < endLine; i++) {
                      chunkContent.append(lines[i]).append("\n");
                  }
                  
                  CodeChunk chunk = CodeChunk.builder()
                      .document(document)
                      .startLine(startLine + 1) // 1-indexed
                      .endLine(endLine)
                      .content(chunkContent.toString())
                      .symbol(extractSymbol(chunkContent.toString(), document.getLanguage()))
                      .build();
                  
                  chunks.add(chunk);
                  startLine = endLine;
              }
              
              return chunks;
          }
          
          private String extractSymbol(String content, String language) {
              // Simple heuristic: extract first function/class name
              if ("java".equals(language)) {
                  if (content.contains("class ")) {
                      return extractPattern(content, "class\\s+(\\w+)");
                  } else if (content.contains("public ") || content.contains("private ")) {
                      return extractPattern(content, "(public|private|protected)\\s+\\w+\\s+(\\w+)\\s*\\(");
                  }
              }
              return null;
          }
          
          private String extractPattern(String content, String regex) {
              var matcher = Pattern.compile(regex).matcher(content);
              if (matcher.find()) {
                  return matcher.group(matcher.groupCount());
              }
              return null;
          }
          
          public String detectLanguage(String filePath) {
              String extension = getFileExtension(filePath);
              return switch (extension) {
                  case "java" -> "java";
                  case "js", "jsx" -> "javascript";
                  case "ts", "tsx" -> "typescript";
                  case "py" -> "python";
                  case "go" -> "go";
                  case "rs" -> "rust";
                  case "cpp", "cc", "cxx" -> "cpp";
                  case "c" -> "c";
                  case "cs" -> "csharp";
                  case "rb" -> "ruby";
                  case "php" -> "php";
                  default -> "text";
              };
          }
          
          private String getFileExtension(String path) {
              int lastDot = path.lastIndexOf('.');
              if (lastDot > 0 && lastDot < path.length() - 1) {
                  return path.substring(lastDot + 1).toLowerCase();
              }
              return "";
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 11. **Create VectorStoreService for Qdrant operations**
      
      Create service in service/vector package with methods: storeChunkEmbedding(chunkId, embedding, metadata) (stores embedding in Qdrant with payload containing chunkId, projectId, filePath), searchSimilar(queryEmbedding, limit, projectId) (searches Qdrant for similar vectors, filters by projectId in payload), deleteByProjectId(projectId) (deletes all vectors for a project), batchStore(chunks) (stores multiple embeddings efficiently). Use QdrantClient bean (may be null if Qdrant unavailable). Methods should check if client is null and throw VectorStoreException with helpful message. Use Points API for upsert/search/delete.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\vector\VectorStoreService.java
      
      **Details**:
      ```java
      package com.codeforge.service.vector;
      
      import com.codeforge.config.AppProperties;
      import com.codeforge.entity.CodeChunk;
      import com.codeforge.exception.VectorStoreException;
      import io.qdrant.client.QdrantClient;
      import io.qdrant.client.grpc.Points.*;
      import lombok.RequiredArgsConstructor;
      import lombok.extern.slf4j.Slf4j;
      import org.springframework.stereotype.Service;
      
      import java.util.*;
      import java.util.concurrent.ExecutionException;
      
      @Service
      @RequiredArgsConstructor
      @Slf4j
      public class VectorStoreService {
          
          private final QdrantClient qdrantClient;
          private final AppProperties appProperties;
          
          public void storeChunkEmbedding(Long chunkId, float[] embedding, Map<String, Object> metadata) {
              if (qdrantClient == null) {
                  throw new VectorStoreException("Qdrant client not available");
              }
              
              try {
                  String collectionName = appProperties.getQdrant().getCollectionName();
                  
                  // Build payload
                  Map<String, Value> payload = new HashMap<>();
                  payload.put("chunk_id", Value.newBuilder().setIntegerValue(chunkId).build());
                  
                  for (Map.Entry<String, Object> entry : metadata.entrySet()) {
                      if (entry.getValue() instanceof String) {
                          payload.put(entry.getKey(), Value.newBuilder().setStringValue((String) entry.getValue()).build());
                      } else if (entry.getValue() instanceof Long) {
                          payload.put(entry.getKey(), Value.newBuilder().setIntegerValue((Long) entry.getValue()).build());
                      }
                  }
                  
                  // Build point
                  PointStruct point = PointStruct.newBuilder()
                      .setId(PointId.newBuilder().setNum(chunkId).build())
                      .setVectors(Vectors.newBuilder().setVector(Vector.newBuilder().addAllData(toList(embedding)).build()).build())
                      .putAllPayload(payload)
                      .build();
                  
                  qdrantClient.upsertAsync(collectionName, List.of(point)).get();
                  log.debug("Stored embedding for chunk {}", chunkId);
                  
              } catch (InterruptedException | ExecutionException e) {
                  log.error("Failed to store embedding for chunk {}: {}", chunkId, e.getMessage());
                  throw new VectorStoreException("Failed to store embedding", e);
              }
          }
          
          public List<Long> searchSimilar(float[] queryEmbedding, int limit, Long projectId) {
              if (qdrantClient == null) {
                  log.warn("Qdrant client not available, returning empty search results");
                  return Collections.emptyList();
              }
              
              try {
                  String collectionName = appProperties.getQdrant().getCollectionName();
                  
                  // Build filter for projectId
                  Filter filter = null;
                  if (projectId != null) {
                      filter = Filter.newBuilder()
                          .addMust(Condition.newBuilder()
                              .setField(FieldCondition.newBuilder()
                                  .setKey("project_id")
                                  .setMatch(Match.newBuilder().setInteger(projectId).build())
                                  .build())
                              .build())
                          .build();
                  }
                  
                  SearchPoints searchRequest = SearchPoints.newBuilder()
                      .setCollectionName(collectionName)
                      .addAllVector(toList(queryEmbedding))
                      .setLimit(limit)
                      .setFilter(filter)
                      .setWithPayload(WithPayloadSelector.newBuilder().setEnable(true).build())
                      .build();
                  
                  List<ScoredPoint> results = qdrantClient.searchAsync(searchRequest).get();
                  
                  List<Long> chunkIds = results.stream()
                      .map(point -> point.getPayloadOrThrow("chunk_id").getIntegerValue())
                      .toList();
                  
                  log.debug("Found {} similar chunks for project {}", chunkIds.size(), projectId);
                  return chunkIds;
                  
              } catch (InterruptedException | ExecutionException e) {
                  log.error("Failed to search similar chunks: {}", e.getMessage());
                  throw new VectorStoreException("Failed to search similar chunks", e);
              }
          }
          
          public void deleteByProjectId(Long projectId) {
              if (qdrantClient == null) {
                  throw new VectorStoreException("Qdrant client not available");
              }
              
              try {
                  String collectionName = appProperties.getQdrant().getCollectionName();
                  
                  Filter filter = Filter.newBuilder()
                      .addMust(Condition.newBuilder()
                          .setField(FieldCondition.newBuilder()
                              .setKey("project_id")
                              .setMatch(Match.newBuilder().setInteger(projectId).build())
                              .build())
                          .build())
                      .build();
                  
                  qdrantClient.deleteAsync(collectionName, filter).get();
                  log.info("Deleted all vectors for project {}", projectId);
                  
              } catch (InterruptedException | ExecutionException e) {
                  log.error("Failed to delete vectors for project {}: {}", projectId, e.getMessage());
                  throw new VectorStoreException("Failed to delete vectors", e);
              }
          }
          
          public void batchStore(List<CodeChunk> chunks, Map<Long, float[]> embeddings) {
              if (qdrantClient == null) {
                  throw new VectorStoreException("Qdrant client not available");
              }
              
              try {
                  String collectionName = appProperties.getQdrant().getCollectionName();
                  List<PointStruct> points = new ArrayList<>();
                  
                  for (CodeChunk chunk : chunks) {
                      float[] embedding = embeddings.get(chunk.getId());
                      if (embedding == null) continue;
                      
                      Map<String, Value> payload = new HashMap<>();
                      payload.put("chunk_id", Value.newBuilder().setIntegerValue(chunk.getId()).build());
                      payload.put("project_id", Value.newBuilder().setIntegerValue(chunk.getDocument().getProject().getId()).build());
                      payload.put("file_path", Value.newBuilder().setStringValue(chunk.getDocument().getFilePath()).build());
                      
                      PointStruct point = PointStruct.newBuilder()
                          .setId(PointId.newBuilder().setNum(chunk.getId()).build())
                          .setVectors(Vectors.newBuilder().setVector(Vector.newBuilder().addAllData(toList(embedding)).build()).build())
                          .putAllPayload(payload)
                          .build();
                      
                      points.add(point);
                  }
                  
                  qdrantClient.upsertAsync(collectionName, points).get();
                  log.info("Batch stored {} embeddings", points.size());
                  
              } catch (InterruptedException | ExecutionException e) {
                  log.error("Failed to batch store embeddings: {}", e.getMessage());
                  throw new VectorStoreException("Failed to batch store embeddings", e);
              }
          }
          
          private List<Float> toList(float[] array) {
              List<Float> list = new ArrayList<>(array.length);
              for (float f : array) {
                  list.add(f);
              }
              return list;
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 12. **Create RepositoryImportService for async import orchestration**
      
      Create service with @Async method importRepository(projectId, owner, repo, accessToken) that orchestrates: fetch from GitHub (GithubService), process files (CodeProcessingService), generate embeddings (LLMProvider.getEmbedding), store in Qdrant (VectorStoreService). Track import status in-memory (ConcurrentHashMap<String, ImportStatus>) with importId (UUID), status (QUEUED, PROCESSING, COMPLETED, FAILED), progress (0.0-1.0), error message. Update Project entity with importStatus and importId columns (see migration step). Use ProjectRepository to update status.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\RepositoryImportService.java
      
      **Details**:
      ```java
      package com.codeforge.service;
      
      import com.codeforge.entity.CodeChunk;
      import com.codeforge.entity.CodeDocument;
      import com.codeforge.entity.Project;
      import com.codeforge.exception.RepositoryImportException;
      import com.codeforge.exception.ResourceNotFoundException;
      import com.codeforge.repository.ProjectRepository;
      import com.codeforge.service.ai.LLMProvider;
      import com.codeforge.service.code.CodeProcessingService;
      import com.codeforge.service.github.GithubService;
      import com.codeforge.service.vector.VectorStoreService;
      import lombok.Builder;
      import lombok.Data;
      import lombok.RequiredArgsConstructor;
      import lombok.extern.slf4j.Slf4j;
      import org.springframework.scheduling.annotation.Async;
      import org.springframework.stereotype.Service;
      
      import java.time.LocalDateTime;
      import java.util.*;
      import java.util.concurrent.ConcurrentHashMap;
      
      @Service
      @RequiredArgsConstructor
      @Slf4j
      public class RepositoryImportService {
          
          private final ProjectRepository projectRepository;
          private final GithubService githubService;
          private final CodeProcessingService codeProcessingService;
          private final LLMProvider llmProvider;
          private final VectorStoreService vectorStoreService;
          
          private final Map<String, ImportStatus> importStatusMap = new ConcurrentHashMap<>();
          
          @Async
          public void importRepository(Long projectId, String owner, String repo, String accessToken) {
              String importId = UUID.randomUUID().toString();
              
              ImportStatus status = ImportStatus.builder()
                  .importId(importId)
                  .projectId(projectId)
                  .status("PROCESSING")
                  .progress(0.0)
                  .startedAt(LocalDateTime.now())
                  .build();
              
              importStatusMap.put(importId, status);
              
              try {
                  Project project = projectRepository.findById(projectId)
                      .orElseThrow(() -> ResourceNotFoundException.notFound("Project", "id", projectId));
                  
                  // Update project with import status
                  project.setRepositoryUrl(String.format("https://github.com/%s/%s", owner, repo));
                  projectRepository.save(project);
                  
                  // Step 1: Fetch repository content (20% progress)
                  log.info("Fetching repository content from {}/{}", owner, repo);
                  Map<String, String> allFiles = githubService.fetchRepositoryContent(accessToken, owner, repo);
                  status.setProgress(0.2);
                  
                  // Step 2: Filter relevant files (30% progress)
                  Map<String, String> relevantFiles = codeProcessingService.filterRelevantFiles(allFiles);
                  status.setProgress(0.3);
                  
                  // Step 3: Process files and create documents/chunks (50% progress)
                  log.info("Processing {} relevant files", relevantFiles.size());
                  List<CodeDocument> documents = new ArrayList<>();
                  for (Map.Entry<String, String> entry : relevantFiles.entrySet()) {
                      String filePath = entry.getKey();
                      String content = entry.getValue();
                      String language = codeProcessingService.detectLanguage(filePath);
                      
                      CodeDocument doc = codeProcessingService.createCodeDocumentAndChunks(project, filePath, content, language);
                      documents.add(doc);
                  }
                  status.setProgress(0.5);
                  
                  // Step 4: Generate embeddings (80% progress)
                  log.info("Generating embeddings for {} documents", documents.size());
                  Map<Long, float[]> embeddingsMap = new HashMap<>();
                  List<CodeChunk> allChunks = new ArrayList<>();
                  
                  for (CodeDocument doc : documents) {
                      for (CodeChunk chunk : doc.getChunks()) {
                          allChunks.add(chunk);
                          float[] embedding = llmProvider.getEmbedding(chunk.getContent());
                          embeddingsMap.put(chunk.getId(), embedding);
                      }
                  }
                  status.setProgress(0.8);
                  
                  // Step 5: Store in Qdrant (100% progress)
                  log.info("Storing {} embeddings in Qdrant", allChunks.size());
                  vectorStoreService.batchStore(allChunks, embeddingsMap);
                  status.setProgress(1.0);
                  
                  status.setStatus("COMPLETED");
                  status.setCompletedAt(LocalDateTime.now());
                  status.setTotalFiles(documents.size());
                  status.setTotalChunks(allChunks.size());
                  
                  log.info("Import completed for project {} - {} files, {} chunks", projectId, documents.size(), allChunks.size());
                  
              } catch (Exception e) {
                  log.error("Import failed for project {}: {}", projectId, e.getMessage(), e);
                  status.setStatus("FAILED");
                  status.setError(e.getMessage());
                  status.setCompletedAt(LocalDateTime.now());
              }
          }
          
          public ImportStatus getImportStatus(String importId) {
              ImportStatus status = importStatusMap.get(importId);
              if (status == null) {
                  throw ResourceNotFoundException.notFound("Import", "importId", importId);
              }
              return status;
          }
          
          @Data
          @Builder
          public static class ImportStatus {
              private String importId;
              private Long projectId;
              private String status; // QUEUED, PROCESSING, COMPLETED, FAILED
              private Double progress; // 0.0 - 1.0
              private String error;
              private Integer totalFiles;
              private Integer totalChunks;
              private LocalDateTime startedAt;
              private LocalDateTime completedAt;
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 13. **Update AIService to add RAG enhancement**
      
      Modify chat() method in AIService: before calling llmProvider.chat(), check if VectorStoreService is available (inject it, check if qdrantClient bean exists). If available, get embedding of the question using llmProvider.getEmbedding(), call vectorStoreService.searchSimilar() with the embedding and projectId, fetch the actual CodeChunk entities by IDs from CodeChunkRepository, build context from retrieved chunks (replace current logic that fetches all chunks). This enables semantic search instead of returning all chunks.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\AIService.java
      
      **Details**:
      Add VectorStoreService as constructor parameter. Modify chat() method:
      ```java
      // Replace existing chunk retrieval logic with:
      List<CodeChunk> relevantChunks;
      try {
          // Use semantic search if Qdrant available
          float[] queryEmbedding = llmProvider.getEmbedding(request.getQuestion());
          List<Long> chunkIds = vectorStoreService.searchSimilar(queryEmbedding, 10, projectId);
          relevantChunks = codeChunkRepository.findAllById(chunkIds);
          log.info("Retrieved {} relevant chunks via semantic search", relevantChunks.size());
      } catch (Exception e) {
          // Fall back to fetching all chunks if Qdrant unavailable
          log.warn("Semantic search unavailable, falling back to all chunks: {}", e.getMessage());
          relevantChunks = codeChunkRepository.findByDocumentProjectId(projectId);
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 14. **Create DTO classes for GitHub and import operations**
      
      Create DTOs in dto/request and dto/response packages: GithubOAuthCallbackRequest (code, state), GithubRepositoryResponse (name, fullName, description, private, url, language, stars), ImportRepositoryRequest (owner, repo, projectId), ImportStatusResponse (importId, status, progress, error, totalFiles, totalChunks, startedAt, completedAt), SemanticSearchRequest (query, projectId, limit), SemanticSearchResponse (chunks with file, startLine, endLine, content, score).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\request\GithubOAuthCallbackRequest.java
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\request\ImportRepositoryRequest.java
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\request\SemanticSearchRequest.java
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\GithubRepositoryResponse.java
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\ImportStatusResponse.java
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\SemanticSearchResponse.java
      
      **Details**:
      ```java
      // GithubOAuthCallbackRequest.java
      package com.codeforge.dto.request;
      import jakarta.validation.constraints.NotBlank;
      import lombok.Data;
      
      @Data
      public class GithubOAuthCallbackRequest {
          @NotBlank
          private String code;
          private String state;
      }
      
      // ImportRepositoryRequest.java
      package com.codeforge.dto.request;
      import jakarta.validation.constraints.NotBlank;
      import jakarta.validation.constraints.NotNull;
      import lombok.Data;
      
      @Data
      public class ImportRepositoryRequest {
          @NotBlank
          private String owner;
          @NotBlank
          private String repo;
          @NotNull
          private Long projectId;
      }
      
      // SemanticSearchRequest.java
      package com.codeforge.dto.request;
      import jakarta.validation.constraints.NotBlank;
      import lombok.Data;
      
      @Data
      public class SemanticSearchRequest {
          @NotBlank
          private String query;
          private Long projectId;
          private Integer limit = 10;
      }
      
      // GithubRepositoryResponse.java
      package com.codeforge.dto.response;
      import lombok.Builder;
      import lombok.Data;
      
      @Data
      @Builder
      public class GithubRepositoryResponse {
          private String name;
          private String fullName;
          private String description;
          private Boolean isPrivate;
          private String url;
          private String language;
          private Integer stars;
      }
      
      // ImportStatusResponse.java
      package com.codeforge.dto.response;
      import lombok.Builder;
      import lombok.Data;
      import java.time.LocalDateTime;
      
      @Data
      @Builder
      public class ImportStatusResponse {
          private String importId;
          private Long projectId;
          private String status;
          private Double progress;
          private String error;
          private Integer totalFiles;
          private Integer totalChunks;
          private LocalDateTime startedAt;
          private LocalDateTime completedAt;
      }
      
      // SemanticSearchResponse.java
      package com.codeforge.dto.response;
      import lombok.Builder;
      import lombok.Data;
      import java.util.List;
      
      @Data
      @Builder
      public class SemanticSearchResponse {
          private List<ChunkResult> results;
          
          @Data
          @Builder
          public static class ChunkResult {
              private Long chunkId;
              private String file;
              private Integer startLine;
              private Integer endLine;
              private String content;
              private Double score;
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 15. **Create GithubController for GitHub OAuth and repository operations**
      
      Create REST controller with endpoints: GET /api/github/oauth/authorize (generates OAuth URL), POST /api/github/oauth/callback (handles callback with code), GET /api/github/repositories (lists user's repos), POST /api/github/import (starts import), GET /api/github/import/{importId}/status (checks import status), DELETE /api/github/tokens (deletes user's GitHub token). Inject GithubOAuthService, GithubService, RepositoryImportService. Use @AuthenticationPrincipal for current user. Return appropriate DTOs.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\controller\GithubController.java
      
      **Details**:
      ```java
      package com.codeforge.controller;
      
      import com.codeforge.dto.request.GithubOAuthCallbackRequest;
      import com.codeforge.dto.request.ImportRepositoryRequest;
      import com.codeforge.dto.response.ImportStatusResponse;
      import com.codeforge.entity.GithubToken;
      import com.codeforge.entity.User;
      import com.codeforge.exception.ResourceNotFoundException;
      import com.codeforge.repository.GithubTokenRepository;
      import com.codeforge.service.RepositoryImportService;
      import com.codeforge.service.github.GithubOAuthService;
      import com.codeforge.service.github.GithubService;
      import jakarta.validation.Valid;
      import lombok.RequiredArgsConstructor;
      import org.springframework.http.ResponseEntity;
      import org.springframework.security.core.annotation.AuthenticationPrincipal;
      import org.springframework.security.core.userdetails.UserDetails;
      import org.springframework.web.bind.annotation.*;
      
      import java.util.List;
      import java.util.Map;
      import java.util.UUID;
      
      @RestController
      @RequestMapping("/github")
      @RequiredArgsConstructor
      public class GithubController {
          
          private final GithubOAuthService githubOAuthService;
          private final GithubService githubService;
          private final RepositoryImportService repositoryImportService;
          private final GithubTokenRepository githubTokenRepository;
          
          @GetMapping("/oauth/authorize")
          public ResponseEntity<Map<String, String>> getAuthorizationUrl() {
              String state = UUID.randomUUID().toString();
              String url = githubOAuthService.generateAuthorizationUrl(state);
              return ResponseEntity.ok(Map.of("url", url, "state", state));
          }
          
          @PostMapping("/oauth/callback")
          public ResponseEntity<Map<String, String>> handleCallback(
                  @Valid @RequestBody GithubOAuthCallbackRequest request,
                  @AuthenticationPrincipal UserDetails userDetails) {
              
              // Exchange code for token
              String accessToken = githubOAuthService.exchangeCodeForToken(request.getCode());
              
              // Get user profile
              Map<String, Object> profile = githubOAuthService.getUserProfile(accessToken);
              String username = (String) profile.get("login");
              
              // Save token
              User user = (User) userDetails;
              githubOAuthService.saveOrUpdateGithubToken(user.getId(), accessToken, username);
              
              return ResponseEntity.ok(Map.of("status", "success", "username", username));
          }
          
          @GetMapping("/repositories")
          public ResponseEntity<List<Map<String, Object>>> listRepositories(
                  @AuthenticationPrincipal UserDetails userDetails) {
              
              User user = (User) userDetails;
              GithubToken token = githubTokenRepository.findByUserId(user.getId()).stream()
                  .findFirst()
                  .orElseThrow(() -> ResourceNotFoundException.notFound("GithubToken", "userId", user.getId()));
              
              List<Map<String, Object>> repos = githubService.listRepositories(token.getToken());
              return ResponseEntity.ok(repos);
          }
          
          @PostMapping("/import")
          public ResponseEntity<Map<String, String>> importRepository(
                  @Valid @RequestBody ImportRepositoryRequest request,
                  @AuthenticationPrincipal UserDetails userDetails) {
              
              User user = (User) userDetails;
              GithubToken token = githubTokenRepository.findByUserId(user.getId()).stream()
                  .findFirst()
                  .orElseThrow(() -> ResourceNotFoundException.notFound("GithubToken", "userId", user.getId()));
              
              String importId = UUID.randomUUID().toString();
              repositoryImportService.importRepository(request.getProjectId(), request.getOwner(), 
                  request.getRepo(), token.getToken());
              
              return ResponseEntity.ok(Map.of("importId", importId, "status", "PROCESSING"));
          }
          
          @GetMapping("/import/{importId}/status")
          public ResponseEntity<ImportStatusResponse> getImportStatus(@PathVariable String importId) {
              RepositoryImportService.ImportStatus status = repositoryImportService.getImportStatus(importId);
              
              ImportStatusResponse response = ImportStatusResponse.builder()
                  .importId(status.getImportId())
                  .projectId(status.getProjectId())
                  .status(status.getStatus())
                  .progress(status.getProgress())
                  .error(status.getError())
                  .totalFiles(status.getTotalFiles())
                  .totalChunks(status.getTotalChunks())
                  .startedAt(status.getStartedAt())
                  .completedAt(status.getCompletedAt())
                  .build();
              
              return ResponseEntity.ok(response);
          }
          
          @DeleteMapping("/tokens")
          public ResponseEntity<Map<String, String>> deleteToken(
                  @AuthenticationPrincipal UserDetails userDetails) {
              
              User user = (User) userDetails;
              List<GithubToken> tokens = githubTokenRepository.findByUserId(user.getId());
              githubTokenRepository.deleteAll(tokens);
              
              return ResponseEntity.ok(Map.of("status", "success"));
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 16. **Create CodeSearchController for semantic search endpoint**
      
      Create REST controller with POST /api/code/search endpoint. Accepts SemanticSearchRequest, uses VectorStoreService to search, fetches CodeChunk entities, returns SemanticSearchResponse. This provides a standalone semantic search endpoint separate from the chat flow.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\controller\CodeSearchController.java
      
      **Details**:
      ```java
      package com.codeforge.controller;
      
      import com.codeforge.dto.request.SemanticSearchRequest;
      import com.codeforge.dto.response.SemanticSearchResponse;
      import com.codeforge.entity.CodeChunk;
      import com.codeforge.repository.CodeChunkRepository;
      import com.codeforge.service.ai.LLMProvider;
      import com.codeforge.service.vector.VectorStoreService;
      import jakarta.validation.Valid;
      import lombok.RequiredArgsConstructor;
      import org.springframework.http.ResponseEntity;
      import org.springframework.web.bind.annotation.*;
      
      import java.util.List;
      import java.util.stream.Collectors;
      
      @RestController
      @RequestMapping("/code")
      @RequiredArgsConstructor
      public class CodeSearchController {
          
          private final VectorStoreService vectorStoreService;
          private final LLMProvider llmProvider;
          private final CodeChunkRepository codeChunkRepository;
          
          @PostMapping("/search")
          public ResponseEntity<SemanticSearchResponse> semanticSearch(
                  @Valid @RequestBody SemanticSearchRequest request) {
              
              // Get query embedding
              float[] queryEmbedding = llmProvider.getEmbedding(request.getQuery());
              
              // Search similar chunks
              List<Long> chunkIds = vectorStoreService.searchSimilar(
                  queryEmbedding, 
                  request.getLimit() != null ? request.getLimit() : 10,
                  request.getProjectId()
              );
              
              // Fetch chunks
              List<CodeChunk> chunks = codeChunkRepository.findAllById(chunkIds);
              
              // Build response
              List<SemanticSearchResponse.ChunkResult> results = chunks.stream()
                  .map(chunk -> SemanticSearchResponse.ChunkResult.builder()
                      .chunkId(chunk.getId())
                      .file(chunk.getDocument().getFilePath())
                      .startLine(chunk.getStartLine())
                      .endLine(chunk.getEndLine())
                      .content(chunk.getContent())
                      .score(1.0) // Placeholder, Qdrant returns scores but we simplified
                      .build())
                  .collect(Collectors.toList());
              
              SemanticSearchResponse response = SemanticSearchResponse.builder()
                  .results(results)
                  .build();
              
              return ResponseEntity.ok(response);
          }
      }
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 17. **Update SecurityConfig to permit GitHub OAuth callback endpoint**
      
      Add POST /github/oauth/callback to permitAll() list in SecurityConfig.java authorizeHttpRequests configuration. This allows unauthenticated users to complete OAuth flow (they authenticate with GitHub, not our backend, at this point).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\config\SecurityConfig.java
      
      **Details**:
      Modify authorizeHttpRequests() to add:
      ```java
      .requestMatchers(HttpMethod.POST, "/github/oauth/callback").permitAll()
      ```
      Add after existing public endpoints (register, login).
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 18. **Create Flyway migration V3 for Phase 3 schema changes**
      
      Create V3__Add_github_import_fields.sql in db/migration directory. Add columns to projects table: import_status VARCHAR(50) (values: PENDING, PROCESSING, COMPLETED, FAILED), import_id VARCHAR(100) for tracking async imports. Add vector_id VARCHAR(100) to code_chunks table for Qdrant point ID tracking. Use SQL Server syntax (ALTER TABLE, NVARCHAR, NULL defaults).
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\resources\db\migration\V3__Add_github_import_fields.sql
      
      **Details**:
      ```sql
      -- ================================================================
      -- CodeForge AI - Phase 3 Schema Changes (Flyway V3)
      -- ================================================================
      -- Add GitHub import tracking to projects table
      -- Add vector store tracking to code_chunks table
      -- Database: Microsoft SQL Server 2022
      -- ================================================================
      
      -- Add import tracking fields to projects table
      ALTER TABLE projects ADD import_status VARCHAR(50) NULL;
      ALTER TABLE projects ADD import_id VARCHAR(100) NULL;
      
      -- Add vector store ID to code_chunks table for Qdrant point tracking
      ALTER TABLE code_chunks ADD vector_id VARCHAR(100) NULL;
      
      -- Add index for import status queries
      CREATE INDEX idx_projects_import_status ON projects(import_status);
      CREATE INDEX idx_projects_import_id ON projects(import_id);
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors. Migration will run on next startup.

- [ ] 19. **Update Project entity to add import tracking fields**
      
      Add two fields to Project entity: importStatus (String, can be null), importId (String, can be null). Add Lombok annotations as needed. These track the async import process initiated via GitHub controller.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\entity\Project.java
      
      **Details**:
      Add after repositoryUrl field:
      ```java
      @Column(length = 50)
      private String importStatus;
      
      @Column(length = 100)
      private String importId;
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 20. **Update CodeChunk entity to add vector store ID field**
      
      Add vectorId field (String, can be null) to CodeChunk entity. This tracks the Qdrant point ID for each chunk.
      
      **Files**: 
      - d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\entity\CodeChunk.java
      
      **Details**:
      Add after embedding field:
      ```java
      @Column(length = 100)
      private String vectorId;
      ```
      
      **Verify**: `cd backend && mvn clean compile` — compiles without errors

- [ ] 21. **Final compilation and verification**
      
      Run full Maven compile to verify all Phase 3 code compiles without errors. Then run unit tests to ensure existing functionality not broken. Finally, attempt to start the application to verify Spring context loads (may fail to connect to Qdrant/GitHub but should not fail on configuration/wiring errors).
      
      **Files**: All Phase 3 files
      
      **Details**:
      ```bash
      cd backend
      mvn clean compile
      mvn test
      mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=test"
      ```
      Check logs for:
      - QdrantConfig initialization (should log warning if Qdrant unavailable but continue)
      - All beans created successfully
      - No circular dependency errors
      - Flyway migration V3 applied successfully
      
      **Verify**: Application starts, logs show "Started CodeForgeApplication", Flyway reports V3 migration applied, QdrantConfig logs connection status

## Notes

- **Graceful Degradation**: Qdrant connection failures at startup are logged as warnings but do not prevent application startup. VectorStoreService methods check for null client and throw VectorStoreException with helpful message.
  
- **Security**: Never log GitHub access tokens (mask as "***" in logs). GithubOAuthService already does this.

- **Async Processing**: RepositoryImportService uses @Async (already enabled via @EnableAsync in CodeForgeApplication). Import status tracked in-memory with ConcurrentHashMap. For production, consider persisting status to database or Redis.

- **Existing Data Model**: GithubToken entity already exists with correct schema. Project, CodeDocument, CodeChunk entities exist. No need to recreate them.

- **Testing Strategy**: Phase 3 can be tested with Qdrant unavailable (graceful degradation). GitHub OAuth requires actual GitHub OAuth app credentials (set GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET). For local testing without real GitHub/Qdrant, mock implementations can be used.

- **Migration Safety**: V3 migration only adds columns (no data modification). Safe to run on existing database with V1 and V2 already applied.

## Success Criteria

Phase 3 is complete when:
1. All code compiles without errors (`mvn clean compile` succeeds)
2. All existing tests pass (`mvn test` succeeds)
3. Application starts successfully with Flyway V3 migration applied
4. GitHub OAuth flow can be initiated (authorization URL generated)
5. Qdrant connection gracefully degrades if unavailable (logs warning, continues)
6. AIService chat() method uses semantic search when Qdrant available
7. All new endpoints return appropriate responses (can be tested with mocks)
