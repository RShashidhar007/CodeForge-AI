package com.codeforge.service;

import com.codeforge.service.ai.MockLLMProvider;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for MockLLMProvider — the default provider active when
 * app.ai.llm.provider=mock (or unset).  No Spring context needed.
 */
class MockLLMProviderTest {

    private MockLLMProvider provider;

    @BeforeEach
    void setUp() {
        provider = new MockLLMProvider();
    }

    @Test
    void chat_returnsNonBlankResponse() {
        String response = provider.chat("What is Java?", "");
        assertNotNull(response);
        assertFalse(response.isBlank());
    }

    @Test
    void chat_responseContainsPrompt() {
        String response = provider.chat("explain streams", null);
        assertTrue(response.toLowerCase().contains("explain streams")
                || response.toLowerCase().contains("mock"),
                "Mock response should reference prompt or label itself as mock");
    }

    @Test
    void explainCode_returnsNonBlankString() {
        String result = provider.explainCode("public void foo() {}", "java");
        assertNotNull(result);
        assertFalse(result.isBlank());
    }

    @Test
    void detectBugs_returnsNonBlankString() {
        String result = provider.detectBugs("int x = null;", "java");
        assertNotNull(result);
        assertFalse(result.isBlank());
    }

    @Test
    void improveCode_returnsNonBlankString() {
        String result = provider.improveCode("for(int i=0;i<10;i++)", "java");
        assertNotNull(result);
        assertFalse(result.isBlank());
    }

    @Test
    void generateTests_returnsNonBlankString() {
        String result = provider.generateTests("public int add(int a, int b){}", "java", "junit");
        assertNotNull(result);
        assertFalse(result.isBlank());
    }

    @Test
    void getEmbedding_returns1536DimensionVector() {
        float[] embedding = provider.getEmbedding("hello world");
        assertNotNull(embedding);
        assertEquals(1536, embedding.length);
    }

    @Test
    void getEmbedding_zeroVector() {
        float[] embedding = provider.getEmbedding("anything");
        for (float v : embedding) {
            assertEquals(0.0f, v);
        }
    }
}
