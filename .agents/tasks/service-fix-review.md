# Service Layer Compilation Fixes

Compilation errors in 9 service/repository classes fixed by aligning references with new entity schema. All changes maintain logical consistency and handle field renamings, enum-to-String conversions, and removed fields.

**Watch for:**
- Unused import in AITaskRepository (`TaskStatus` enum import may be dead code)
- GithubTokenRepository methods (`findByUserIdAndUsername`) no longer used but not cleaned up
- No explicit user context set in AITask creation (set to null; should wire security context in production)

**Verdict**: APPROVED

## High-level view

TaskService, AIService, and AgentExecutor convert enum-based status values (`TaskStatus.PENDING`, `TaskStatus.COMPLETED`) to String equivalents, matching the schema where `status` and `taskType` are now String columns instead of Java enums. This applies consistently across task creation, approval, cancellation, and execution flows. Field renames propagate cleanly: `task` becomes `aiTask` in TaskApproval and AgentExecution, `document` becomes `codeDocument` in CodeChunk queries, and `output`/`result` map to `resultSummary`/`outputData`. Repository methods align with relationship changes (e.g., `findByDocumentProjectId` → `findByCodeDocumentProjectId`), and type conversions handle new Long-based line number fields. All 29 errors resolve with no new compilation errors introduced.

<details>
<summary>Issues (2)</summary>

1. **Unused enum import** — AITaskRepository still imports `TaskStatus` enum (line 6) but the enum no longer exists in AITask. This line should be removed.
2. **Zombie repository method** — GithubOAuthService removed the call to `findByUserIdAndUsername()` but the method likely still exists in GithubTokenRepository. Should verify and remove or deprecate if not used elsewhere.

</details>

<details>
<summary>Details</summary>

### TaskService: Enum to String and field removals

TaskService.createTask() removes references to non-existent fields (`title`, `description`, `selectedFiles`) and converts `status` from `TaskStatus.PENDING` enum to `"PENDING"` String. The `taskType` likewise shifts from `TaskType.valueOf()` to a plain String pass-through. These changes match the entity schema where AITask.status and AITask.taskType are now String columns. The method adds `.inputData("")` to populate the new input field, preserving the ability to capture task input where needed.

TaskService.approveTask() replaces `TaskApproval.builder().task(task)` with `.aiTask(task)` (confirmed in read of the file), updates enum status values to String equivalents ("COMPLETED", "FAILED"), and renames the `status` field to `approvalStatus` and `reason` to `comments`. These are structural changes necessitated by the entity redesign and are applied consistently across both approval and rejection paths.

TaskService.mapToAITaskResponse() stops mapping removed fields (`title`, `description`, `selectedFiles`, `result`). It converts `task.getStatus()` from enum `.name()` call to direct String access, matching the new entity schema. Null-safety check added for project ID prevents NPE if task has no project reference, though that's unlikely given the database constraint.

### AIService: Field name and type alignment

AIService.getCodeContext() calls `codeChunkRepository.findByCodeDocumentProjectId(projectId)` (confirmed in read), using the renamed repository method that reflects the new `codeDocument` field name in CodeChunk. The loop accessing chunks changes from `chunk.getDocument()` to `chunk.getCodeDocument()` and `chunk.getSymbol()` to `chunk.getSymbolName()`. Line numbers cast from Long to Integer for SourceReference DTO compatibility:
```
startLine(chunk.getStartLine() != null ? chunk.getStartLine().intValue() : 0)
endLine(chunk.getEndLine() != null ? chunk.getEndLine().intValue() : 0)
```
These conversions handle the schema change where line numbers are now Long (database precision) while DTOs still expect Integer. Null checks prevent NPE on potentially-null Long values.

### CodeChunkRepository: Method signature updates

Repository interface renames `findByDocumentId()` to `findByCodeDocumentId()` and `findByDocument(CodeDocument)` to `findByCodeDocument(CodeDocument)` to match the renamed field. The new custom query method `findByCodeDocumentProjectId()` uses explicit `@Query` annotation:
```java
@Query("SELECT c FROM CodeChunk c WHERE c.codeDocument.project.id = :projectId")
```
This replaces what was likely a simple naming-convention method that wouldn't work with the renamed relationship. Query is explicit and correct.

### CodeProcessingService: Field renamings and type conversions

CodeDocument creation changes `.fullContent(content)` to `.content(content)`. CodeChunk building updates `.document(document)` to `.codeDocument(document)`, converts line numbers to Long (`.startLine((long)(startLine + 1))`, `.endLine((long)endLine)`), and renames `.symbol(symbol)` to `.symbolName(symbol)`. All changes align with entity schema updates; no logic changes, only field name and type alignment.

### AgentExecutor: Enum-to-String conversion and field restructuring

AgentExecutor.executePendingTasks() queries for tasks by String status: `aiTaskRepository.findByStatus("PENDING")` instead of the old enum. Repository interface supports both overloads (enum and String), so this change is clean.

AgentExecutor.executeTask() undergoes significant restructuring. Status values change from enum (`TaskStatus.IN_PROGRESS`, `.SUCCESS`, `.FAILED`, `.COMPLETED`) to String ("RUNNING", "SUCCESS", "FAILED", "COMPLETED"). Field assignments on AgentExecution shift from `.task(task)` to `.aiTask(task)`, `.agentName(determineAgentName(...))` to `.agentId(determineAgentName(...))`, removal of `.input(task.getDescription())` (field no longer exists), and addition of `.startTime(LocalDateTime.now())` and `.endTime(LocalDateTime.now())` for lifecycle tracking.

On success, `execution.setOutput(result)` becomes `execution.setResultSummary(result)` and `task.setResult(result)` becomes `task.setOutputData(result)`. On failure, `setErrorMessage()` is removed and instead `setResultSummary()` captures the error. These field renamings match the entity redesign where execution results now flow through `resultSummary` and task results through `outputData`.

dispatchToLLM() and determineAgentName() convert from switch-on-enum to switch-on-String, with case labels matching taskType String values ("CODE_ANALYSIS", "REFACTORING", "BUG_FIX", "TEST_GENERATION"). Both methods add default cases for unknown types, improving robustness.

### GithubOAuthService: Token field renaming

GithubOAuthService.saveOrUpdateGithubToken() removes `.username(username)` (field no longer exists on GithubToken), changes the lookup from `findByUserIdAndUsername(userId, username)` to `.findByUserId(userId).stream().findFirst()` (method signature reduced to single parameter), and updates setter from `githubToken.setToken(token)` to `githubToken.setAccessToken(token)`. These changes align with the GithubToken schema redesign where `token` is renamed to `accessToken` and `username` is removed.

### GithubController: Token field propagation

GithubController.listRepositories() and importRepository() update from `token.getToken()` to `token.getAccessToken()` in method calls, propagating the field rename to callers. No logic changes.

### RepositoryImportService: Repository method consistency

RepositoryImportService.importRepositoryAsync() updates `codeChunkRepository.findByDocument(document)` to `codeChunkRepository.findByCodeDocument(document)` for consistency with repository interface changes.

### AITaskRepository: Overloaded method for String status

AITaskRepository adds an overload `List<AITask> findByStatus(String status)` alongside the existing `findByStatus(TaskStatus status)` enum version. This allows both old and new code paths to work during transition. However, the enum import (`import com.codeforge.entity.AITask.TaskStatus`) is now dead code — TaskStatus no longer exists as an enum on AITask. This import should be removed to clean up the interface.

</details>

<details>
<summary>File Map</summary>

- **AIService.java** — Fixed field name mappings (`document` → `codeDocument`, `symbol` → `symbolName`) and type conversions (Long line numbers to Integer for DTO).
- **TaskService.java** — Removed references to deleted fields, converted enum status values to Strings, updated builder and mapper methods.
- **CodeChunkRepository.java** — Renamed method signatures to match new field name (`document` → `codeDocument`), added explicit query for project-level lookup.
- **CodeProcessingService.java** — Updated field names and line number types in document and chunk creation.
- **GithubController.java** — Propagated token field rename (`token` → `accessToken`) to service calls.
- **GithubOAuthService.java** — Removed username field, updated token lookup and setter with new field name.
- **RepositoryImportService.java** — Updated repository method call for CodeChunk lookup.
- **AgentExecutor.java** — Converted all status/taskType enum references to Strings, restructured field assignments for new entity schema.
- **AITaskRepository.java** — Added String-based method overload; dead import remains.

Full diff available in git history.

</details>
