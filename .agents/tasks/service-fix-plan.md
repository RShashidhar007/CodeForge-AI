# Service Layer Compilation Fixes - Detailed Implementation Plan

## Overview
Fix 50+ compilation errors in service and controller classes caused by entity field name changes in the new database schema. The entity classes have been updated but references in services, controllers, and DTOs still use old field names.

## Key Entity Field Changes (Already Applied)
- **CodeDocument**: `fullContent` → `content`, OneToMany mapping field name `document` → `codeDocument`
- **CodeChunk**: `document` → `codeDocument`, `symbol` → `symbolName`, `embedding` is byte[], `startLine`/`endLine` are Long
- **AITask**: removed `title`, `description`, `selectedFiles`, `result`, `taskType` (enum); added `inputData`, `outputData`, `executedByAgentId`; added `user` relationship; `status` is String
- **AIMessage**: added `sources`, `tokensUsed`, `processingTimeMs`
- **AIConversation**: added `user` relationship, added `contextSummary`
- **AgentExecution**: `task` → `aiTask`, removed `input`/`output`/`errorMessage`/`sequenceOrder`; added `agentId`, `status`, `startTime`, `endTime`, `resultSummary`
- **TaskPatch**: `task` → `aiTask`, removed `filePath` (but it's still there, just simplified)
- **TaskTestResult**: `task` → `aiTask`, simplified structure
- **TaskApproval**: `task` → `aiTask` (OneToOne), added `approvedByUser` relationship; removed fields `approverUserId`, `reason`/`status`/`comments` changed
- **GithubToken**: `token`/`username` → `accessToken`/`refreshToken`/`expiresAt`/`scopes`; OneToOne with User

## Compilation Error Categories

### Category 1: AIService.java (AIService.java)
**Location**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\AIService.java`

**Issues Found**:
- Line 74: `chunk.getDocument()` should be `chunk.getCodeDocument()`
- Line 75: `chunk.getDocument().getFilePath()` should be `chunk.getCodeDocument().getFilePath()`
- Line 90: `chunk.getSymbol()` should be `chunk.getSymbolName()`
- Line 65: Missing repository method `findByDocumentProjectId()` → should be `findByCodeDocumentProjectId()`

### Category 2: TaskService.java
**Location**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java`

**Issues Found**:
- Line 47: `task.setTitle()` - field no longer exists
- Line 48: `task.setDescription()` - field no longer exists
- Line 49: `TaskType.valueOf()` - AITask.taskType is String, not enum; should just use `request.getTaskType()`
- Line 50: `task.setSelectedFiles()` - field no longer exists
- Line 53: `TaskStatus.PENDING` - field is String "PENDING", not enum
- Line 102: `task.setStatus(TaskStatus.COMPLETED)` - should be `task.setStatus("COMPLETED")`
- Line 105: `task.setStatus(TaskStatus.FAILED)` - should be `task.setStatus("FAILED")`
- Line 115: `TaskApproval.ApprovalStatus.APPROVED` - enum no longer exists; use String "APPROVED"
- Line 121: `TaskApproval.ApprovalStatus.REJECTED` - use String "REJECTED"
- Line 126: `task.setStatus(TaskStatus.CANCELLED)` - use String "CANCELLED"
- Line 138: `task.getTitle()` - field no longer exists; don't map it
- Line 139: `task.getDescription()` - field no longer exists; don't map it
- Line 141: `task.getStatus().name()` - `status` is already String, remove `.name()`
- Line 142: `task.getTaskType().name()` - `taskType` is already String, remove `.name()`
- Line 143: `task.getSelectedFiles()` - field no longer exists; don't map it
- Line 144: `task.getResult()` - field no longer exists; don't map it
- Line 79-80: `TaskApproval.builder().task()` → `.aiTask()`; `approverUserId()` → remove; `status()` → `approvalStatus()`; `reason()` → `comments()`

### Category 3: Repository Method Signature
**Location**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\AIMessageRepository.java`

**Issues**: Service calls `messageRepository.findByConversationIdOrderByCreatedAtAsc()` — verify this method exists in repository

---

## Implementation Steps

### Step 1: Fix AIService.java
**File**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\AIService.java`

**Changes**:
1. Line 65: Change repository method call from `codeChunkRepository.findByDocumentProjectId(projectId)` to `codeChunkRepository.findByCodeDocumentProjectId(projectId)` OR create a query method if it doesn't exist. Check the repository interface first.

2. Line 74-75: Replace:
   ```java
   context.append("File: ").append(chunk.getDocument().getFilePath())
   ```
   With:
   ```java
   context.append("File: ").append(chunk.getCodeDocument().getFilePath())
   ```

3. Line 90: Replace `chunk.getSymbol()` with `chunk.getSymbolName()`

**Files to modify**: 
- d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\AIService.java

**Verification**: 
```bash
cd d:\projects\CodeForge-AI-main\backend
mvn clean compile -q 2>&1 | grep -i "AIService"
```
Expected: No AIService errors in output (may still have other errors)

---

### Step 2: Fix TaskService.java - Constructor and createTask Method
**File**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java`

**Changes in createTask() method (lines 39-58)**:
Replace:
```java
AITask task = AITask.builder()
    .project(project)
    .title(request.getTitle())
    .description(request.getDescription())
    .taskType(TaskType.valueOf(request.getTaskType()))
    .status(TaskStatus.PENDING)
    .selectedFiles(request.getSelectedFiles() != null ? 
        String.join(",", request.getSelectedFiles()) : "")
    .build();
```

With:
```java
AITask task = AITask.builder()
    .project(project)
    .user(null) // TODO: Get from security context
    .taskType(request.getTaskType()) // Already a String
    .status("PENDING")
    .inputData("") // Store request data if needed
    .build();
```

**Files to modify**: 
- d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java

**Verification**: 
```bash
cd d:\projects\CodeForge-AI-main\backend
mvn clean compile -q 2>&1 | grep -i "createTask"
```

---

### Step 3: Fix TaskService.java - approveTask Method
**File**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java`

**Changes in approveTask() method (lines 95-130)**:
Replace:
```java
if (request.isApproved()) {
    task.setStatus(TaskStatus.COMPLETED);
    
    // Record approval
    TaskApproval approval = TaskApproval.builder()
        .task(task)
        .approverUserId(approverId)
        .status(TaskApproval.ApprovalStatus.APPROVED)
        .reason(request.getReason())
        .build();
    approvalRepository.save(approval);
} else {
    task.setStatus(TaskStatus.FAILED);
    
    // Record rejection
    TaskApproval approval = TaskApproval.builder()
        .task(task)
        .approverUserId(approverId)
        .status(TaskApproval.ApprovalStatus.REJECTED)
        .reason(request.getReason())
        .build();
    approvalRepository.save(approval);
}
```

With:
```java
if (request.isApproved()) {
    task.setStatus("COMPLETED");
    
    // Record approval
    TaskApproval approval = TaskApproval.builder()
        .aiTask(task)
        .approvalStatus("APPROVED")
        .comments(request.getReason())
        .build();
    approvalRepository.save(approval);
} else {
    task.setStatus("FAILED");
    
    // Record rejection
    TaskApproval approval = TaskApproval.builder()
        .aiTask(task)
        .approvalStatus("REJECTED")
        .comments(request.getReason())
        .build();
    approvalRepository.save(approval);
}
```

**Files to modify**: 
- d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java

**Verification**: 
```bash
cd d:\projects\CodeForge-AI-main\backend
mvn clean compile -q 2>&1 | grep -i "approveTask"
```

---

### Step 4: Fix TaskService.java - cancelTask and mapToAITaskResponse Methods
**File**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java`

**Changes in cancelTask() method (line 139)**:
Replace:
```java
task.setStatus(TaskStatus.CANCELLED);
```

With:
```java
task.setStatus("CANCELLED");
```

**Changes in mapToAITaskResponse() method (lines 145-159)**:
Replace entire method:
```java
private AITaskResponse mapToAITaskResponse(AITask task) {
    return AITaskResponse.builder()
        .id(task.getId())
        .projectId(task.getProject().getId())
        .title(task.getTitle())
        .description(task.getDescription())
        .status(task.getStatus().name())
        .taskType(task.getTaskType().name())
        .selectedFiles(task.getSelectedFiles())
        .result(task.getResult())
        .createdAt(task.getCreatedAt())
        .updatedAt(task.getUpdatedAt())
        .executionStartTime(task.getExecutionStartTime())
        .executionEndTime(task.getExecutionEndTime())
        .errorMessage(task.getErrorMessage())
        .build();
}
```

With:
```java
private AITaskResponse mapToAITaskResponse(AITask task) {
    return AITaskResponse.builder()
        .id(task.getId())
        .projectId(task.getProject() != null ? task.getProject().getId() : null)
        .status(task.getStatus()) // Already String
        .taskType(task.getTaskType()) // Already String
        .createdAt(task.getCreatedAt())
        .updatedAt(task.getUpdatedAt())
        .executionStartTime(task.getExecutionStartTime())
        .executionEndTime(task.getExecutionEndTime())
        .errorMessage(task.getErrorMessage())
        .build();
}
```

Note: AITaskResponse DTO may need to have `title`, `description`, `selectedFiles`, `result` fields removed or kept for backward compatibility. If kept, don't set them in the mapper.

**Files to modify**: 
- d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java

**Verification**: 
```bash
cd d:\projects\CodeForge-AI-main\backend
mvn clean compile -q 2>&1 | grep -i "mapToAITaskResponse"
```

---

### Step 5: Update AITaskResponse DTO (if needed)
**File**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\AITaskResponse.java`

**Decision**: Keep fields for backward compatibility but mark as @JsonInclude(Include.NON_NULL) to exclude nulls from JSON. Or remove unused fields entirely if API contract allows.

**Current fields to remove (if not needed)**:
- `title`
- `description`
- `selectedFiles`
- `result`

These are no longer in AITask entity.

**Files to modify**: 
- d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\AITaskResponse.java

**Verification**: Check that DTO compiles and no errors reference these fields

---

### Step 6: Verify AIMessageRepository query method
**File**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\AIMessageRepository.java`

**Check**: Verify the repository has method `findByConversationIdOrderByCreatedAtAsc(Long conversationId)`. If not, add it:

```java
@Query("SELECT m FROM AIMessage m WHERE m.conversation.id = :conversationId ORDER BY m.createdAt ASC")
List<AIMessage> findByConversationIdOrderByCreatedAtAsc(@Param("conversationId") Long conversationId);
```

**Files to check/modify**: 
- d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\AIMessageRepository.java

**Verification**: 
```bash
cd d:\projects\CodeForge-AI-main\backend
mvn clean compile -q 2>&1 | grep -i "AIMessageRepository"
```

---

### Step 7: Check CodeChunkRepository methods
**File**: `d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\CodeChunkRepository.java`

**Check**: Verify method exists: `findByCodeDocumentProjectId(Long projectId)` or `findByCodeDocument_ProjectId(Long projectId)`. If using old name `findByDocumentProjectId()`, rename to new name OR add new query method.

**If method doesn't exist, add**:
```java
@Query("SELECT c FROM CodeChunk c WHERE c.codeDocument.project.id = :projectId")
List<CodeChunk> findByCodeDocumentProjectId(@Param("projectId") Long projectId);
```

**Files to check/modify**: 
- d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\CodeChunkRepository.java

**Verification**: 
```bash
cd d:\projects\CodeForge-AI-main\backend
mvn clean compile -q 2>&1 | grep -i "CodeChunkRepository"
```

---

### Step 8: Full compilation test
**Command**: 
```bash
cd d:\projects\CodeForge-AI-main\backend
mvn clean compile -q
```

**Expected outcome**: No compilation errors. If errors remain, they will point to other files not covered in this plan.

**Success criteria**: Compilation completes with exit code 0.

---

## Summary of Files Modified

1. **d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\AIService.java**
   - Fix getCodeDocument() references
   - Fix getSymbolName() references
   - Fix repository method calls

2. **d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\service\TaskService.java**
   - Remove title, description, selectedFiles, result from createTask
   - Change status/taskType from enum to String
   - Fix TaskApproval builder (task → aiTask, approverUserId removal, field name changes)
   - Fix cancelTask status
   - Fix mapToAITaskResponse to handle new fields only

3. **d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\dto\response\AITaskResponse.java**
   - Optionally remove or mark as optional: title, description, selectedFiles, result

4. **d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\AIMessageRepository.java**
   - Add query method if missing: findByConversationIdOrderByCreatedAtAsc()

5. **d:\projects\CodeForge-AI-main\backend\src\main\java\com\codeforge\repository\CodeChunkRepository.java**
   - Add/rename query method: findByCodeDocumentProjectId()

---

## Notes

- All changes maintain database integrity by using existing entity relationships
- No database schema changes needed — entities already updated
- DTOs may need gradual updates for backward compatibility
- User relationship in AITask is set to null for now — should be populated from security context in production
- Status fields changed from enums to Strings to allow flexibility
- All verified through compilation and tested service methods will be working before moving to integration tests
