package com.codeforge.service.github;

import com.codeforge.entity.*;
import com.codeforge.exception.RepositoryImportException;
import com.codeforge.repository.CodeChunkRepository;
import com.codeforge.repository.ProjectRepository;
import com.codeforge.service.ai.LLMProvider;
import com.codeforge.service.code.CodeProcessingService;
import com.codeforge.service.vector.VectorStoreService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;

/**
 * Service for importing GitHub repositories and creating embeddings
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class RepositoryImportService {
    
    private final GithubService githubService;
    private final CodeProcessingService codeProcessingService;
    private final VectorStoreService vectorStoreService;
    private final LLMProvider llmProvider;
    private final ProjectRepository projectRepository;
    private final CodeChunkRepository codeChunkRepository;
    
    // Track import status in memory (in production, use database)
    private final Map<Long, ImportStatus> importStatusMap = new HashMap<>();
    
    /**
     * Start asynchronous repository import
     */
    @Async
    @Transactional
    public void importRepositoryAsync(Long projectId, String accessToken, String owner, String repo) {
        log.info("Starting import for repository {}/{} into project {}", owner, repo, projectId);
        
        ImportStatus status = new ImportStatus();
        status.setProjectId(projectId);
        status.setStatus("IN_PROGRESS");
        status.setStartTime(LocalDateTime.now());
        importStatusMap.put(projectId, status);
        
        try {
            // Get project
            Project project = projectRepository.findById(projectId)
                .orElseThrow(() -> new RepositoryImportException("Project not found: " + projectId));
            
            // Fetch repository content from GitHub
            status.setCurrentStep("Fetching repository content");
            Map<String, String> allFiles = githubService.fetchRepositoryContent(accessToken, owner, repo);
            status.setTotalFiles(allFiles.size());
            
            // Filter relevant files
            status.setCurrentStep("Filtering source files");
            Map<String, String> relevantFiles = codeProcessingService.filterRelevantFiles(allFiles);
            status.setRelevantFiles(relevantFiles.size());
            log.info("Filtered {} relevant files from {} total", relevantFiles.size(), allFiles.size());
            
            // Process files and create chunks
            status.setCurrentStep("Processing files and creating chunks");
            List<CodeChunk> allChunks = new ArrayList<>();
            int processedFiles = 0;
            
            for (Map.Entry<String, String> entry : relevantFiles.entrySet()) {
                try {
                    String filePath = entry.getKey();
                    String content = entry.getValue();
                    
                    CodeDocument document = codeProcessingService.createCodeDocumentAndChunks(
                        project, filePath, content
                    );
                    
                    List<CodeChunk> chunks = codeChunkRepository.findByDocument(document);
                    allChunks.addAll(chunks);
                    
                    processedFiles++;
                    status.setProcessedFiles(processedFiles);
                    
                    if (processedFiles % 10 == 0) {
                        log.debug("Processed {}/{} files", processedFiles, relevantFiles.size());
                    }
                    
                } catch (Exception e) {
                    log.warn("Failed to process file {}: {}", entry.getKey(), e.getMessage());
                }
            }
            
            log.info("Created {} code chunks from {} files", allChunks.size(), processedFiles);
            status.setTotalChunks(allChunks.size());
            
            // Generate embeddings and store in Qdrant
            status.setCurrentStep("Generating embeddings");
            Map<CodeChunk, float[]> chunkEmbeddings = new HashMap<>();
            int embeddedChunks = 0;
            
            for (CodeChunk chunk : allChunks) {
                try {
                    float[] embedding = llmProvider.getEmbedding(chunk.getContent());
                    chunkEmbeddings.put(chunk, embedding);
                    
                    embeddedChunks++;
                    status.setEmbeddedChunks(embeddedChunks);
                    
                    if (embeddedChunks % 50 == 0) {
                        log.debug("Generated embeddings for {}/{} chunks", embeddedChunks, allChunks.size());
                    }
                    
                } catch (Exception e) {
                    log.warn("Failed to generate embedding for chunk {}: {}", chunk.getId(), e.getMessage());
                }
            }
            
            // Store embeddings in Qdrant (batch operation)
            status.setCurrentStep("Storing embeddings in vector database");
            if (!chunkEmbeddings.isEmpty()) {
                vectorStoreService.storeEmbeddingsBatch(chunkEmbeddings);
            }
            
            // Update project status
            project.setUpdatedAt(LocalDateTime.now());
            projectRepository.save(project);
            
            // Mark import as complete
            status.setStatus("COMPLETED");
            status.setEndTime(LocalDateTime.now());
            log.info("Successfully imported repository {}/{} into project {}. " +
                    "Processed {} files, created {} chunks, generated {} embeddings",
                    owner, repo, projectId, processedFiles, allChunks.size(), embeddedChunks);
            
        } catch (Exception e) {
            log.error("Failed to import repository {}/{}: {}", owner, repo, e.getMessage(), e);
            status.setStatus("FAILED");
            status.setError(e.getMessage());
            status.setEndTime(LocalDateTime.now());
            throw new RepositoryImportException("Failed to import repository", e);
        }
    }
    
    /**
     * Get import status
     */
    public ImportStatus getImportStatus(Long projectId) {
        return importStatusMap.getOrDefault(projectId, null);
    }
    
    /**
     * Import status DTO
     */
    @lombok.Data
    public static class ImportStatus {
        private Long projectId;
        private String status; // IN_PROGRESS, COMPLETED, FAILED
        private String currentStep;
        private int totalFiles;
        private int relevantFiles;
        private int processedFiles;
        private int totalChunks;
        private int embeddedChunks;
        private String error;
        private LocalDateTime startTime;
        private LocalDateTime endTime;
    }
}
