package com.codeforge.service.agent;

import com.codeforge.entity.AgentExecution;
import com.codeforge.entity.AgentExecution.ExecutionStatus;
import com.codeforge.entity.AITask;
import com.codeforge.entity.AITask.TaskStatus;
import com.codeforge.entity.AITask.TaskType;
import com.codeforge.repository.AgentExecutionRepository;
import com.codeforge.repository.AITaskRepository;
import com.codeforge.service.ai.LLMProvider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class AgentExecutor {

    private final AITaskRepository aiTaskRepository;
    private final AgentExecutionRepository agentExecutionRepository;
    private final LLMProvider llmProvider;

    @Scheduled(fixedDelay = 5000)
    @Transactional
    public void executePendingTasks() {
        List<AITask> pendingTasks = aiTaskRepository.findByStatus(TaskStatus.PENDING);
        log.debug("Found {} pending tasks", pendingTasks.size());

        for (AITask task : pendingTasks) {
            executeTask(task);
        }
    }

    private void executeTask(AITask task) {
        log.info("Executing task id={} type={}", task.getId(), task.getTaskType());

        task.setStatus(TaskStatus.IN_PROGRESS);
        task.setExecutionStartTime(LocalDateTime.now());
        aiTaskRepository.save(task);

        AgentExecution execution = AgentExecution.builder()
                .task(task)
                .agentName(determineAgentName(task.getTaskType()))
                .input(task.getDescription())
                .status(ExecutionStatus.RUNNING)
                .sequenceOrder(0)
                .build();
        agentExecutionRepository.save(execution);

        try {
            String input = task.getSelectedFiles() != null ? task.getSelectedFiles() : task.getDescription();
            String result = dispatchToLLM(task.getTaskType(), input);

            execution.setStatus(ExecutionStatus.SUCCESS);
            execution.setOutput(result);
            agentExecutionRepository.save(execution);

            task.setStatus(TaskStatus.COMPLETED);
            task.setResult(result);
            task.setExecutionEndTime(LocalDateTime.now());
            aiTaskRepository.save(task);

            log.info("Task id={} completed successfully", task.getId());
        } catch (Exception ex) {
            log.error("Task id={} failed: {}", task.getId(), ex.getMessage(), ex);

            execution.setStatus(ExecutionStatus.FAILED);
            execution.setErrorMessage(ex.getMessage());
            agentExecutionRepository.save(execution);

            task.setStatus(TaskStatus.FAILED);
            task.setErrorMessage(ex.getMessage());
            task.setExecutionEndTime(LocalDateTime.now());
            aiTaskRepository.save(task);
        }
    }

    private String dispatchToLLM(TaskType type, String input) {
        if (type == null) {
            return llmProvider.explainCode(input, "unknown");
        }
        return switch (type) {
            case CODE_ANALYSIS -> llmProvider.explainCode(input, "auto-detect");
            case REFACTORING   -> llmProvider.improveCode(input, "auto-detect");
            case BUG_FIX       -> llmProvider.detectBugs(input, "auto-detect");
            case TEST_GENERATION -> llmProvider.generateTests(input, "auto-detect", "junit");
        };
    }

    private String determineAgentName(TaskType type) {
        if (type == null) return "GenericAgent";
        return switch (type) {
            case CODE_ANALYSIS  -> "CodeAnalysisAgent";
            case REFACTORING    -> "RefactoringAgent";
            case BUG_FIX        -> "BugFixAgent";
            case TEST_GENERATION -> "TestGenerationAgent";
        };
    }
}
