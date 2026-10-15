package com.codeforge.service.vector;

import com.codeforge.config.AppProperties;
import com.codeforge.entity.CodeChunk;
import com.codeforge.exception.VectorStoreException;
import com.codeforge.service.ai.LLMProvider;
import io.qdrant.client.QdrantClient;
import io.qdrant.client.grpc.Points;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Service for vector store operations (Qdrant)
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class VectorStoreService {
    
    private final QdrantClient qdrantClient;
    private final LLMProvider llmProvider;
    private final AppProperties appProperties;
    
    /**
     * Store code chunk embedding in Qdrant
     */
    public void storeEmbedding(CodeChunk chunk, float[] embedding) {
        if (qdrantClient == null) {
            log.warn("Qdrant client not available, skipping embedding storage for chunk {}", chunk.getId());
            return;
        }
        
        try {
            String collectionName = appProperties.getQdrant().getCollectionName();
            
            // Create point with chunk ID and embedding
            Points.PointStruct point = Points.PointStruct.newBuilder()
                .setId(Points.PointId.newBuilder().setNum(chunk.getId()).build())
                .setVectors(Points.Vectors.newBuilder()
                    .setVector(Points.Vector.newBuilder()
                        .addAllData(toList(embedding))
                        .build())
                    .build())
                .build();
            
            qdrantClient.upsertAsync(collectionName, List.of(point)).get();
            log.debug("Stored embedding for chunk {} in Qdrant", chunk.getId());
            
        } catch (Exception e) {
            log.error("Failed to store embedding for chunk {}: {}", chunk.getId(), e.getMessage());
            throw new VectorStoreException("Failed to store embedding", e);
        }
    }
    
    /**
     * Store multiple embeddings in batch
     */
    public void storeEmbeddingsBatch(Map<CodeChunk, float[]> chunkEmbeddings) {
        if (qdrantClient == null) {
            log.warn("Qdrant client not available, skipping batch embedding storage");
            return;
        }
        
        try {
            String collectionName = appProperties.getQdrant().getCollectionName();
            
            List<Points.PointStruct> points = chunkEmbeddings.entrySet().stream()
                .map(entry -> {
                    CodeChunk chunk = entry.getKey();
                    float[] embedding = entry.getValue();
                    
                    return Points.PointStruct.newBuilder()
                        .setId(Points.PointId.newBuilder().setNum(chunk.getId()).build())
                        .setVectors(Points.Vectors.newBuilder()
                            .setVector(Points.Vector.newBuilder()
                                .addAllData(toList(embedding))
                                .build())
                            .build())
                        .build();
                })
                .collect(Collectors.toList());
            
            qdrantClient.upsertAsync(collectionName, points).get();
            log.info("Stored {} embeddings in Qdrant", points.size());
            
        } catch (Exception e) {
            log.error("Failed to store batch embeddings: {}", e.getMessage());
            throw new VectorStoreException("Failed to store batch embeddings", e);
        }
    }
    
    /**
     * Search for similar code chunks using semantic search
     */
    public List<SearchResult> search(String query, Long projectId, int limit) {
        if (qdrantClient == null) {
            log.warn("Qdrant client not available, returning empty search results");
            return Collections.emptyList();
        }
        
        try {
            // Generate embedding for query
            float[] queryEmbedding = llmProvider.getEmbedding(query);
            
            String collectionName = appProperties.getQdrant().getCollectionName();
            
            // Build search request with project filter
            Points.Filter filter = Points.Filter.newBuilder()
                .addMust(Points.Condition.newBuilder()
                    .setField(Points.FieldCondition.newBuilder()
                        .setKey("projectId")
                        .setMatch(Points.Match.newBuilder()
                            .setInteger(projectId)
                            .build())
                        .build())
                    .build())
                .build();
            
            Points.SearchPoints searchPoints = Points.SearchPoints.newBuilder()
                .setCollectionName(collectionName)
                .addAllVector(toList(queryEmbedding))
                .setFilter(filter)
                .setLimit(limit)
                .setWithPayload(Points.WithPayloadSelector.newBuilder().setEnable(true).build())
                .build();
            
            List<Points.ScoredPoint> results = qdrantClient.searchAsync(searchPoints).get();
            
            return results.stream()
                .map(this::toSearchResult)
                .collect(Collectors.toList());
            
        } catch (Exception e) {
            log.error("Failed to search embeddings: {}", e.getMessage());
            throw new VectorStoreException("Failed to search embeddings", e);
        }
    }
    
    /**
     * Delete embeddings for a project
     */
    public void deleteProjectEmbeddings(Long projectId) {
        if (qdrantClient == null) {
            log.warn("Qdrant client not available, skipping deletion for project {}", projectId);
            return;
        }
        
        try {
            String collectionName = appProperties.getQdrant().getCollectionName();
            
            Points.Filter filter = Points.Filter.newBuilder()
                .addMust(Points.Condition.newBuilder()
                    .setField(Points.FieldCondition.newBuilder()
                        .setKey("projectId")
                        .setMatch(Points.Match.newBuilder()
                            .setInteger(projectId)
                            .build())
                        .build())
                    .build())
                .build();
            
            qdrantClient.deleteAsync(collectionName, filter).get();
            log.info("Deleted embeddings for project {}", projectId);
            
        } catch (Exception e) {
            log.error("Failed to delete embeddings for project {}: {}", projectId, e.getMessage());
            throw new VectorStoreException("Failed to delete embeddings", e);
        }
    }
    
    /**
     * Convert float array to List<Float>
     */
    private List<Float> toList(float[] array) {
        List<Float> list = new ArrayList<>(array.length);
        for (float f : array) {
            list.add(f);
        }
        return list;
    }
    
    /**
     * Convert ScoredPoint to SearchResult
     */
    private SearchResult toSearchResult(Points.ScoredPoint point) {
        // Note: payload not stored in this version, using point ID as chunk ID
        return SearchResult.builder()
            .chunkId(point.getId().getNum())
            .documentId(0L) // Will be loaded from database
            .filePath("") // Will be loaded from database
            .startLine(0) // Will be loaded from database
            .endLine(0) // Will be loaded from database
            .symbol("") // Will be loaded from database
            .score(point.getScore())
            .build();
    }
    
    /**
     * Search result DTO
     */
    @lombok.Data
    @lombok.Builder
    public static class SearchResult {
        private Long chunkId;
        private Long documentId;
        private String filePath;
        private int startLine;
        private int endLine;
        private String symbol;
        private float score;
    }
}
