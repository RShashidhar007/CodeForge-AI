package com.codeforge.service.ai;

import com.codeforge.config.AppProperties;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.List;
import java.util.Map;

@Slf4j
@Service
@ConditionalOnProperty(name = "app.ai.llm.provider", havingValue = "openai")
public class OpenAIProvider implements LLMProvider {

    private final AppProperties appProperties;
    private final WebClient webClient;
    private final ObjectMapper objectMapper;

    public OpenAIProvider(AppProperties appProperties) {
        this.appProperties = appProperties;
        this.webClient = WebClient.builder()
                .baseUrl("https://api.openai.com")
                .defaultHeader("Authorization", "Bearer " + appProperties.getAi().getLlm().getApiKey())
                .defaultHeader("Content-Type", "application/json")
                .build();
        this.objectMapper = new ObjectMapper();
    }

    private String callChatCompletions(String prompt) {
        String model = appProperties.getAi().getLlm().getModel();
        int maxTokens = appProperties.getAi().getLlm().getMaxTokens();
        double temperature = appProperties.getAi().getLlm().getTemperature();

        Map<String, Object> requestBody = Map.of(
                "model", model,
                "messages", List.of(Map.of("role", "user", "content", prompt)),
                "max_tokens", maxTokens,
                "temperature", temperature
        );

        try {
            String responseBody = webClient.post()
                    .uri("/v1/chat/completions")
                    .bodyValue(requestBody)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            JsonNode root = objectMapper.readTree(responseBody);
            return root.path("choices").get(0).path("message").path("content").asText();
        } catch (Exception e) {
            log.error("Error calling OpenAI chat completions: {}", e.getMessage(), e);
            return "";
        }
    }

    @Override
    public String chat(String prompt, String context) {
        try {
            String fullPrompt = (context != null && !context.isEmpty())
                    ? "Context:\n" + context + "\n\nUser: " + prompt
                    : prompt;
            return callChatCompletions(fullPrompt);
        } catch (Exception e) {
            log.error("Error in chat(): {}", e.getMessage(), e);
            return "";
        }
    }

    @Override
    public String explainCode(String code, String language) {
        try {
            String prompt = "Explain the following " + language + " code:\n\n```" + language + "\n" + code + "\n```";
            return callChatCompletions(prompt);
        } catch (Exception e) {
            log.error("Error in explainCode(): {}", e.getMessage(), e);
            return "";
        }
    }

    @Override
    public String detectBugs(String code, String language) {
        try {
            String prompt = "Analyze the following " + language + " code for bugs and issues:\n\n```" + language + "\n" + code + "\n```";
            return callChatCompletions(prompt);
        } catch (Exception e) {
            log.error("Error in detectBugs(): {}", e.getMessage(), e);
            return "";
        }
    }

    @Override
    public String improveCode(String code, String language) {
        try {
            String prompt = "Suggest improvements for the following " + language + " code:\n\n```" + language + "\n" + code + "\n```";
            return callChatCompletions(prompt);
        } catch (Exception e) {
            log.error("Error in improveCode(): {}", e.getMessage(), e);
            return "";
        }
    }

    @Override
    public String generateTests(String code, String language, String testFramework) {
        try {
            String prompt = "Generate " + testFramework + " tests for the following " + language + " code:\n\n```" + language + "\n" + code + "\n```";
            return callChatCompletions(prompt);
        } catch (Exception e) {
            log.error("Error in generateTests(): {}", e.getMessage(), e);
            return "";
        }
    }

    @Override
    public float[] getEmbedding(String text) {
        Map<String, Object> requestBody = Map.of(
                "model", "text-embedding-3-small",
                "input", text
        );

        try {
            String responseBody = webClient.post()
                    .uri("/v1/embeddings")
                    .bodyValue(requestBody)
                    .retrieve()
                    .bodyToMono(String.class)
                    .block();

            JsonNode root = objectMapper.readTree(responseBody);
            JsonNode embeddingArray = root.path("data").get(0).path("embedding");

            float[] result = new float[embeddingArray.size()];
            for (int i = 0; i < embeddingArray.size(); i++) {
                result[i] = (float) embeddingArray.get(i).asDouble();
            }
            return result;
        } catch (Exception e) {
            log.error("Error in getEmbedding(): {}", e.getMessage(), e);
            return new float[0];
        }
    }
}
