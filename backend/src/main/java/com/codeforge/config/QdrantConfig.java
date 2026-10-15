package com.codeforge.config;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;
import io.qdrant.client.grpc.Collections;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuration for Qdrant vector database client
 */
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
                false // useTls
            );
            
            // Add API key if configured
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
            return null; // Graceful degradation
        }
    }
    
    private void initializeCollection(QdrantClient client, String collectionName) {
        try {
            // Try to get collection info
            client.getCollectionInfoAsync(collectionName).get();
            log.debug("Qdrant collection '{}' already exists", collectionName);
            
        } catch (Exception e) {
            // Collection doesn't exist, create it
            try {
                Collections.VectorParams vectorParams = Collections.VectorParams.newBuilder()
                    .setSize(1536)  // text-embedding-3-small dimension
                    .setDistance(Collections.Distance.Cosine)
                    .build();
                
                client.createCollectionAsync(collectionName, vectorParams).get();
                log.info("Qdrant collection '{}' created successfully", collectionName);
                
            } catch (Exception createError) {
                log.warn("Failed to create Qdrant collection '{}': {}", collectionName, createError.getMessage());
            }
        }
    }
}
