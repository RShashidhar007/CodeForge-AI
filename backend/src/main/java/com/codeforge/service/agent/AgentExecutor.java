package com.codeforge.service.agent;

import com.codeforge.entity.AgentExecution;
import com.codeforge.entity.AITask;
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
        List<AITask> pendingTasks = aiTaskRepository.findByStatus("PENDING");
        log.debug("Found {} pending tasks", pendingTasks.size());

        for (AITask task : pendingTasks) {
            executeTask(task);
        }
    }

    private void executeTask(AITask task) {
        log.info("Executing task id={} type={}", task.getId(), task.getTaskType());

        task.setStatus("RUNNING");
        task.setExecutionStartTime(LocalDateTime.now());
        aiTaskRepository.save(task);

        AgentExecution execution = AgentExecution.builder()
                .aiTask(task)
                .agentId(determineAgentName(task.getTaskType()))
                .status("RUNNING")
                .startTime(LocalDateTime.now())
                .build();
        agentExecutionRepository.save(execution);

        try {
            String input = task.getInputData() != null ? task.getInputData() : "";
            String result = dispatchToLLM(task.getTaskType(), input);

            execution.setStatus("SUCCESS");
            execution.setResultSummary(result);
            execution.setEndTime(LocalDateTime.now());
            agentExecutionRepository.save(execution);

            task.setStatus("COMPLETED");
            task.setOutputData(result);
            task.setExecutionEndTime(LocalDateTime.now());
            aiTaskRepository.save(task);

            log.info("Task id={} completed successfully", task.getId());
        } catch (Exception ex) {
            log.error("Task id={} failed: {}", task.getId(), ex.getMessage(), ex);

            execution.setStatus("FAILED");
            execution.setResultSummary(ex.getMessage());
            execution.setEndTime(LocalDateTime.now());
            agentExecutionRepository.save(execution);

            task.setStatus("FAILED");
            task.setErrorMessage(ex.getMessage());
            task.setExecutionEndTime(LocalDateTime.now());
            aiTaskRepository.save(task);
        }
    }

    private String dispatchToLLM(String taskType, String input) {
        if (taskType == null) {
            return llmProvider.explainCode(input, "unknown");
        }
        return switch (taskType) {
            case "CODE_ANALYSIS" -> llmProvider.explainCode(input, "auto-detect");
            case "REFACTORING" -> llmProvider.improveCode(input, "auto-detect");
            case "BUG_FIX" -> llmProvider.detectBugs(input, "auto-detect");
            case "TEST_GENERATION" -> llmProvider.generateTests(input, "auto-detect", "junit");
            default -> llmProvider.explainCode(input, "unknown");
        };
    }

    private String determineAgentName(String taskType) {
        if (taskType == null) return "GenericAgent";
        return switch (taskType) {
            case "CODE_ANALYSIS" -> "CodeAnalysisAgent";
            case "REFACTORING" -> "RefactoringAgent";
            case "BUG_FIX" -> "BugFixAgent";
            case "TEST_GENERATION" -> "TestGenerationAgent";
            default -> "GenericAgent";
        };
    }
}
