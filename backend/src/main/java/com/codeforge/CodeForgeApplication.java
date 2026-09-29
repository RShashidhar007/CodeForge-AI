package com.codeforge;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Main Spring Boot application entry point for CodeForge AI Backend.
 * 
 * Migrated from Python FastAPI backend to Spring Boot 3.x
 * 
 * Features:
 * - REST API for recruitment platform
 * - User authentication with JWT
 * - AI-powered code analysis and retrieval
 * - Multi-agent task execution
 * - Redis caching
 * - MSSQL database persistence
 */
@SpringBootApplication
@EnableCaching
@EnableAsync
public class CodeForgeApplication {

    public static void main(String[] args) {
        SpringApplication.run(CodeForgeApplication.class, args);
    }
}
