package com.codeforge.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

/**
 * Application-wide configuration properties.
 * Mapped from application.properties using Spring's @ConfigurationProperties.
 */
@Component
@ConfigurationProperties(prefix = "app")
@Data
public class AppProperties {

    private final Jwt jwt = new Jwt();
    private final Cors cors = new Cors();
    private final Admin admin = new Admin();
    private final Ai ai = new Ai();

    @Data
    public static class Jwt {
        private String secret;
        private int expiration;
        private String algorithm = "HS256";
    }

    @Data
    public static class Cors {
        private String allowedOrigins;
    }

    @Data
    public static class Admin {
        private String email;
        private String password;
        private String name;
    }

    @Data
    public static class Ai {
        private final Llm llm = new Llm();
        private final Embedding embedding = new Embedding();

        @Data
        public static class Llm {
            private String provider; // openai, mock
            private String model;
            private String apiKey;
            private int maxTokens = 2000;
            private double temperature = 0.7;
        }

        @Data
        public static class Embedding {
            private String provider;
            private String model;
            private String apiKey;
            private int dimension = 1536;
        }
    }
}
