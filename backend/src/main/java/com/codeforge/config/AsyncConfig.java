package com.codeforge.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;

/**
 * Configuration for asynchronous method execution
 */
@Configuration
@EnableAsync
public class AsyncConfig {
    // Async support enabled for @Async annotated methods
}
