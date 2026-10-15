# Phase 2 Implementation Plan: Production-Ready Backend

This plan transforms the CodeForge AI backend from mock responses to a production-ready system with real LLM integration, async agent execution, rate limiting, input validation, and JWT token revocation.

## Key Architecture Decisions

**LLM Provider Strategy**: Use Spring's `@ConditionalOnProperty` to enable provider-specific beans (OpenAIProvider vs MockLLMProvider) based on `app.ai.llm.provider`. This allows seamless switching between mock and real implementations without code changes.

**Agent Execution Model**: Poll-based scheduler (5-second fixed delay) that queries `PENDING` tasks, executes them via LLMProvider, and updates status. No complex queue infrastructure needed — the database is the queue.

**Rate Limiting**: Use Bucket4j with in-memory token buckets (100 req/min per client IP) applied via servlet filter. Redis-backed buckets are future enhancement; in-memory is sufficient for current scale.

**JWT Blacklist**: Redis-backed set with TTL matching token expiry. On logout, token goes into `jwt:blacklist:{token}` with TTL = remaining token lifetime. `validateToken()` checks blacklist before proceeding.

**Database Schema Evolution**: Add three columns to `ai_tasks` table via Flyway migration V2. Hibernate's `ddl-auto=update` won't create these cleanly, so Flyway is mandatory for this phase.

---

## Implementation Steps

- [ ] 1. **Create LLMProvider interface and implementations**
      
      Define `LLMProvider` interface with methods: `chat(prompt, context)`, `explainCode(code, language)`, `detectBugs(code, language)`, `improveCode(code, language)`, `generateTests(code, language, testFramework)`, `getEmbedding(text)`.
      
      Create `OpenAIProvider` using `WebClient` (already in pom.xml via spring-boot-starter-webflux) to call OpenAI API. Guard with `@ConditionalOnProperty(name="app.ai.llm.provider", havingValue="openai")`. Inject `AppProperties.Ai.Llm` for apiKey, model, maxTokens, temperature. Use POST to `https://api.openai.com/v1/chat/completions` for chat-based methods, and POST to `https://api.openai.com/v1/embeddings` for `getEmbedding()`. Return `Mono<String>` or `Mono<List<Double>>` and block synchronously in each method (async at scheduler level, not provider level).
      
      Create `MockLLMProvider` with stub responses like "Mock explanation for {language} code: {first 50 chars}". Guard with `@ConditionalOnProperty(name="app.ai.llm.provider", havingValue="mock", matchIfMissing=true)`. This is the default when provider property is unset.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\ai\LLMProvider.java` (new interface)
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\ai\OpenAIProvider.java` (new class)
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\ai\MockLLMProvider.java` (new class)
      
      Verify: `mvn clean compile` succeeds, no bean creation errors on startup with `app.ai.llm.provider=mock` (default) and with `app.ai.llm.provider=openai` (requires valid API key or will fail at runtime call, not startup).

- [ ] 2. **Update AIService to use LLMProvider**
      
      Inject `LLMProvider` into `AIService`. Replace all "Mock response" strings in `chat()`, `explainCode()`, `detectBugs()`, `improveCode()`, `generateTests()` with calls to the corresponding `LLMProvider` methods.
      
      For `chat()`: pass `request.getQuestion()` as prompt and the built `context` string as context to `llmProvider.chat(prompt, context)`.
      
      For `explainCode()`: pass `request.getCode()` and `request.getLanguage()` to `llmProvider.explainCode(code, language)`.
      
      For `detectBugs()`: pass `request.getCode()` and `request.getLanguage()` to `llmProvider.detectBugs(code, language)`.
      
      For `improveCode()`: pass `request.getCode()` and `request.getLanguage()` to `llmProvider.improveCode(code, language)`.
      
      For `generateTests()`: pass `request.getCode()`, `request.getLanguage()`, and `request.getTestFramework()` to `llmProvider.generateTests(code, language, testFramework)`.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\AIService.java` (modify)
      
      Verify: `mvn test` runs all existing tests successfully. No integration tests exist yet for OpenAI, but mock tests should pass.

- [ ] 3. **Add database columns to AITask entity and create Flyway migration V2**
      
      Add three fields to `AITask` entity (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\entity\AITask.java`):
      - `executionStartTime` (LocalDateTime, nullable, no default)
      - `executionEndTime` (LocalDateTime, nullable, no default)
      - `errorMessage` (String, `@Column(columnDefinition = "TEXT")`, nullable)
      
      Create Flyway migration `V2__Add_AITask_execution_fields.sql` in `d:\projects\CodeForge-AI-main\backend\src\main\resources\db\migration\`:
      
      ```sql
      -- Add execution tracking fields to ai_tasks table
      ALTER TABLE ai_tasks ADD execution_start_time DATETIME2 NULL;
      ALTER TABLE ai_tasks ADD execution_end_time DATETIME2 NULL;
      ALTER TABLE ai_tasks ADD error_message NVARCHAR(MAX) NULL;
      ```
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\entity\AITask.java` (modify: add 3 fields)
      - `d:\projects\CodeForge-AI-main\backend\src\main\resources\db\migration\V2__Add_AITask_execution_fields.sql` (new)
      
      Verify: `mvn clean compile` succeeds. Start the application with a clean database (or with Flyway baseline) and confirm migration V2 applies without error. Check `flyway_schema_history` table for V2 entry.

- [ ] 4. **Add findByStatus() method to AITaskRepository**
      
      Add method signature: `List<AITask> findByStatus(TaskStatus status);` to `AITaskRepository` interface (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\AITaskRepository.java`). Spring Data JPA will auto-implement this query method.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\AITaskRepository.java` (modify: add 1 method signature)
      
      Verify: `mvn clean compile` succeeds. No runtime errors when calling `aiTaskRepository.findByStatus(TaskStatus.PENDING)`.

- [ ] 5. **Create AgentExecutor service with @Scheduled task polling**
      
      Create `AgentExecutor` service at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\agent\AgentExecutor.java`. Inject `AITaskRepository`, `AgentExecutionRepository`, `LLMProvider`.
      
      Add method `@Scheduled(fixedDelay = 5000) public void executePendingTasks()`. Inside:
      1. Query `aiTaskRepository.findByStatus(TaskStatus.PENDING)` to get pending tasks.
      2. For each task:
         - Set `task.setStatus(TaskStatus.IN_PROGRESS)`, `task.setExecutionStartTime(LocalDateTime.now())`, save.
         - Create `AgentExecution` record with `status = ExecutionStatus.PENDING`, `agentName = determineAgentName(task.getTaskType())`, `input = task.getDescription()`, `sequenceOrder = 0`.
         - Set `execution.setStatus(ExecutionStatus.RUNNING)`, save.
         - Call the appropriate LLM method based on `task.getTaskType()`:
           - `CODE_ANALYSIS` → `llmProvider.explainCode(task.getSelectedFiles(), "auto-detect")`
           - `REFACTORING` → `llmProvider.improveCode(task.getSelectedFiles(), "auto-detect")`
           - `BUG_FIX` → `llmProvider.detectBugs(task.getSelectedFiles(), "auto-detect")`
           - `TEST_GENERATION` → `llmProvider.generateTests(task.getSelectedFiles(), "auto-detect", "junit")`
         - On success: set `execution.setStatus(ExecutionStatus.SUCCESS)`, `execution.setOutput(llmResult)`, `task.setStatus(TaskStatus.COMPLETED)`, `task.setResult(llmResult)`, `task.setExecutionEndTime(LocalDateTime.now())`, save both.
         - On exception: set `execution.setStatus(ExecutionStatus.FAILED)`, `execution.setErrorMessage(ex.getMessage())`, `task.setStatus(TaskStatus.FAILED)`, `task.setErrorMessage(ex.getMessage())`, `task.setExecutionEndTime(LocalDateTime.now())`, save both.
      
      Helper method `private String determineAgentName(TaskType type)` returns: "CodeAnalysisAgent", "RefactoringAgent", "BugFixAgent", "TestGenerationAgent" based on type.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\agent\AgentExecutor.java` (new class)
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\AgentExecutionRepository.java` (verify exists or create if missing)
      
      Verify: Start the application, create an AITask via TaskController with status PENDING, wait 5-10 seconds, check that task status becomes COMPLETED or FAILED, and AgentExecution record exists with appropriate status and output/errorMessage.

- [ ] 6. **Add @EnableScheduling to CodeForgeApplication**
      
      Add `@EnableScheduling` annotation to `CodeForgeApplication` class (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\CodeForgeApplication.java`). This is required for `@Scheduled` methods to run.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\CodeForgeApplication.java` (modify: add 1 annotation)
      
      Verify: Start the application, confirm in logs that scheduled tasks are enabled and `AgentExecutor.executePendingTasks()` runs every 5 seconds (look for DEBUG logs or add a simple log statement in the method).

- [ ] 7. **Add bucket4j-core dependency to pom.xml**
      
      Add dependency to `d:\projects\CodeForge-AI-main\backend\pom.xml`:
      
      ```xml
      <!-- Bucket4j for rate limiting -->
      <dependency>
          <groupId>com.bucket4j</groupId>
          <artifactId>bucket4j-core</artifactId>
          <version>7.6.0</version>
      </dependency>
      ```
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\pom.xml` (modify: add 1 dependency)
      
      Verify: `mvn clean compile` succeeds and downloads bucket4j-core 7.6.0.

- [ ] 8. **Create RateLimitingFilter using Bucket4j**
      
      Create `RateLimitingFilter` at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\security\RateLimitingFilter.java` extending `OncePerRequestFilter`.
      
      Use `ConcurrentHashMap<String, Bucket>` to store buckets per client IP. Create buckets on-demand using `Bucket.builder().addLimit(Bandwidth.simple(100, Duration.ofMinutes(1))).build()` (100 requests per minute).
      
      In `doFilterInternal()`:
      1. Get client IP from `request.getRemoteAddr()`.
      2. Get or create bucket for IP.
      3. If `bucket.tryConsume(1)` succeeds, call `filterChain.doFilter(request, response)`.
      4. If fails, set `response.setStatus(429)`, write JSON error response: `{"error":"Rate limit exceeded","message":"Maximum 100 requests per minute"}`, return without calling filterChain.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\security\RateLimitingFilter.java` (new class)
      
      Verify: `mvn clean compile` succeeds. No registration yet, so no runtime effect.

- [ ] 9. **Register RateLimitingFilter in SecurityConfig**
      
      Inject `RateLimitingFilter` into `SecurityConfig` (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\config\SecurityConfig.java`).
      
      Add filter registration in `securityFilterChain()` method before JWTFilter: `.addFilterBefore(rateLimitingFilter, JWTFilter.class)`.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\config\SecurityConfig.java` (modify: inject filter, add 1 line in filter chain)
      
      Verify: Start the application, make 101 requests to any endpoint from the same IP within 1 minute. The 101st request should return HTTP 429 with rate limit error.

- [ ] 10. **Create JWTBlacklistService using RedisTemplate**
      
      Create `JWTBlacklistService` at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\security\JWTBlacklistService.java`. Inject `RedisTemplate<String, Object>` and `JWTProvider`.
      
      Add methods:
      - `public void blacklistToken(String token)`: Get expiration date from `jwtProvider.getExpirationDateFromToken(token)`, calculate TTL = `expirationDate.getTime() - System.currentTimeMillis()` in milliseconds. Store in Redis with key `jwt:blacklist:{token}` and value "blacklisted", set expiry to TTL milliseconds using `redisTemplate.opsForValue().set(key, value, ttl, TimeUnit.MILLISECONDS)`.
      - `public boolean isBlacklisted(String token)`: Check if key `jwt:blacklist:{token}` exists in Redis using `redisTemplate.hasKey(key)`. Return true if exists, false otherwise.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\security\JWTBlacklistService.java` (new class)
      
      Verify: `mvn clean compile` succeeds. Unit test: create a token, blacklist it, verify `isBlacklisted()` returns true for 1 second, then false after TTL expires (use short TTL for test).

- [ ] 11. **Add extractTokenFromRequest() method to JWTProvider and update validateToken()**
      
      Add method to `JWTProvider` (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\security\JWTProvider.java`):
      
      ```java
      public String extractTokenFromRequest(HttpServletRequest request) {
          String bearerToken = request.getHeader("Authorization");
          if (StringUtils.hasText(bearerToken) && bearerToken.startsWith("Bearer ")) {
              return bearerToken.substring(7);
          }
          return null;
      }
      ```
      
      Update `validateToken(String token)` to inject `JWTBlacklistService` and check blacklist before verifying token:
      
      ```java
      public Boolean validateToken(String token) {
          if (jwtBlacklistService.isBlacklisted(token)) {
              return false;
          }
          try {
              JWT.require(getAlgorithm()).build().verify(token);
              return !isTokenExpired(token);
          } catch (JWTVerificationException e) {
              return false;
          }
      }
      ```
      
      Note: `extractTokenFromRequest()` is a convenience method but `JWTFilter` already has `extractJwtFromRequest()` doing the same. Consider reusing or consolidating. Decision: Keep both for now (JWTProvider version is for controller use, JWTFilter version is internal).
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\security\JWTProvider.java` (modify: add 1 method, update validateToken to inject JWTBlacklistService and check blacklist)
      
      Verify: `mvn clean compile` succeeds. Create token, blacklist it, call `validateToken()` — should return false.

- [ ] 12. **Add POST /auth/logout endpoint to AuthController**
      
      Add method to `AuthController` (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\controller\AuthController.java`):
      
      ```java
      @PostMapping("/logout")
      public ResponseEntity<Map<String, String>> logout(HttpServletRequest request) {
          String token = jwtProvider.extractTokenFromRequest(request);
          if (token != null) {
              jwtBlacklistService.blacklistToken(token);
          }
          return ResponseEntity.ok(Map.of("message", "Logged out successfully"));
      }
      ```
      
      Inject `JWTProvider` and `JWTBlacklistService` into AuthController.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\controller\AuthController.java` (modify: inject 2 services, add 1 method)
      
      Verify: `mvn clean compile` succeeds. Integration test: login to get token, call `/auth/logout` with that token in Authorization header, then try to call a protected endpoint with same token — should get 401 Unauthorized.

- [ ] 13. **Add validation annotations to ChatRequest**
      
      Modify `ChatRequest` (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\request\ChatRequest.java`):
      
      Change `private String question;` to:
      
      ```java
      @NotBlank(message = "Question is required")
      @Size(max = 5000, message = "Question must be at most 5000 characters")
      private String question;
      ```
      
      Add imports: `jakarta.validation.constraints.NotBlank` and `jakarta.validation.constraints.Size`.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\request\ChatRequest.java` (modify: add 2 annotations to question field)
      
      Verify: `mvn clean compile` succeeds. Send POST to `/v1/projects/{id}/ai/chat` with empty question or question > 5000 chars — should get 400 Bad Request with validation error from GlobalExceptionHandler.

- [ ] 14. **Add validation annotations to CodeAnalysisRequest**
      
      Modify `CodeAnalysisRequest` (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\request\CodeAnalysisRequest.java`):
      
      Change `private String code;` to:
      
      ```java
      @NotBlank(message = "Code is required")
      @Size(max = 50000, message = "Code must be at most 50000 characters")
      private String code;
      ```
      
      Add imports: `jakarta.validation.constraints.NotBlank` and `jakarta.validation.constraints.Size`.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\request\CodeAnalysisRequest.java` (modify: add 2 annotations to code field)
      
      Verify: `mvn clean compile` succeeds. Send POST to `/v1/projects/{id}/ai/explain` with empty code or code > 50000 chars — should get 400 Bad Request with validation error.

- [ ] 15. **Verify GlobalExceptionHandler handles MethodArgumentNotValidException**
      
      Review `GlobalExceptionHandler` (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\exception\GlobalExceptionHandler.java`) to confirm `@ExceptionHandler(MethodArgumentNotValidException.class)` method exists and returns 400 Bad Request with field validation errors.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\exception\GlobalExceptionHandler.java` (verify only, already exists based on earlier reading)
      
      Verify: No code changes needed. Test with invalid request to any endpoint with `@Valid` annotation — should return 400 with structured error response showing field name and validation message.

- [ ] 16. **Add status and result query endpoints to TaskController**
      
      TaskController already has `getTask(projectId, taskId)` which returns `AITaskResponse`. Verify that `AITaskResponse` DTO includes fields for: `status`, `result`, `executionStartTime`, `executionEndTime`, `errorMessage`. If missing, add them to `AITaskResponse` (at `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\AITaskResponse.java`).
      
      No new endpoints needed — existing `GET /v1/projects/{projectId}/ai/tasks/{taskId}` already serves task status and result. Update `TaskService.getTask()` to map the new AITask fields to the response DTO.
      
      Files:
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\AITaskResponse.java` (modify if needed: add fields for executionStartTime, executionEndTime, errorMessage)
      - `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java` (modify: update getTask() to map new fields)
      
      Verify: `mvn clean compile` succeeds. Create task, wait for execution, call `GET /v1/projects/{id}/ai/tasks/{taskId}` — response should include status, result, executionStartTime, executionEndTime, errorMessage (if failed).

- [ ] 17. **End-to-end integration test: Real LLM flow (manual)**
      
      This is a manual verification step, not code.
      
      1. Set environment variable `app.ai.llm.provider=openai` and `app.ai.llm.api-key={valid-openai-key}` in `application.properties` or as JVM args.
      2. Start the application: `mvn spring-boot:run`.
      3. Login to get JWT token.
      4. Create an AITask via `POST /v1/projects/{projectId}/ai/tasks` with taskType=CODE_ANALYSIS, description="Analyze this function", selectedFiles="def foo(): pass".
      5. Wait 5-10 seconds for AgentExecutor to pick up the task.
      6. Query `GET /v1/projects/{projectId}/ai/tasks/{taskId}` — should show status=COMPLETED, result containing OpenAI's analysis.
      7. Call `POST /v1/projects/{projectId}/ai/chat` with question="What is this code doing?" — should get real OpenAI response in answer field.
      8. Call `POST /auth/logout` with JWT token, then try calling chat again with same token — should get 401 Unauthorized.
      9. Make 101 requests to any endpoint from same IP within 1 minute — 101st should get 429 Rate Limit Exceeded.
      
      Verify: All steps above succeed with OpenAI provider. Switch back to `app.ai.llm.provider=mock` (default) and verify mock responses work as before.

- [ ] 18. **Run full test suite and verify no regressions**
      
      Run all backend tests: `mvn clean test`.
      
      Expected: All existing tests pass. No new test coverage added in this phase (integration tests for OpenAI would require API key management and are excluded). Rate limiting and JWT blacklist tests are manual or can be added later.
      
      Files: No files modified.
      
      Verify: `mvn test` exits with success (exit code 0), all tests green.

---

## Summary

This plan adds:
- Real LLM integration via OpenAI API with provider abstraction (OpenAI vs Mock)
- Async agent task execution via Spring @Scheduled polling (5s interval)
- Rate limiting (100 req/min per IP) via Bucket4j servlet filter
- JWT token revocation (logout blacklist) via Redis with TTL
- Input validation on ChatRequest.question (5000 chars max) and CodeAnalysisRequest.code (50000 chars max)
- Database schema evolution (3 new columns on ai_tasks) via Flyway migration V2
- Task status/result query endpoints (reusing existing TaskController GET endpoint)

All changes respect existing codebase patterns:
- Spring Boot 3.2 + Java 17
- Spring Data JPA with MSSQL
- Redis for caching and blacklist
- Lombok for entity/DTO boilerplate
- GlobalExceptionHandler for validation errors
- Flyway for database migrations
- Maven for builds, H2 for tests

Build command: `mvn clean install`
Test command: `mvn test`
Run command: `mvn spring-boot:run` or `java -jar target/codeforge-backend-1.0.0.jar`
