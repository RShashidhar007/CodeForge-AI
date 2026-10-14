package com.codeforge.service.ai;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@ConditionalOnProperty(name = "app.ai.llm.provider", havingValue = "mock", matchIfMissing = true)
public class MockLLMProvider implements LLMProvider {

    @Override
    public String chat(String prompt, String context) {
        return "Mock response to: " + prompt;
    }

    @Override
    public String explainCode(String code, String language) {
        return "Mock explanation for " + language + " code: " + (code.length() > 50 ? code.substring(0, 50) : code);
    }

    @Override
    public String detectBugs(String code, String language) {
        return "Mock bug analysis for " + language + " code. No bugs found (mock).";
    }

    @Override
    public String improveCode(String code, String language) {
        return "Mock improvement suggestions for " + language + " code.";
    }

    @Override
    public String generateTests(String code, String language, String testFramework) {
        return "Mock " + testFramework + " tests for " + language + " code.";
    }

    @Override
    public float[] getEmbedding(String text) {
        return new float[1536];
    }
}
