package com.codeforge.service.ai;

public interface LLMProvider {
    String chat(String prompt, String context);
    String explainCode(String code, String language);
    String detectBugs(String code, String language);
    String improveCode(String code, String language);
    String generateTests(String code, String language, String testFramework);
    float[] getEmbedding(String text);
}
