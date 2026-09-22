package com.codeforge.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * JPA configuration
 * Enables auditing and repository scanning
 */
@Configuration
@EnableJpaRepositories(basePackages = "com.codeforge.repository")
@EnableJpaAuditing
public class JpaConfig {
}
