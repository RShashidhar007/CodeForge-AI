# Multi-stage build for Spring Boot application
# Stage 1: Build
FROM maven:3.9.4-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build application
RUN mvn clean package -DskipTests -B

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Install bash for debugging
RUN apk add --no-cache bash

# Copy JAR from builder
COPY --from=builder /app/target/codeforge-backend-*.jar app.jar

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD java -cp app.jar -Dspring.config.location=classpath:/application.properties \
    org.springframework.boot.loader.JarLauncher health || exit 1

# Run application
ENTRYPOINT ["java", "-jar", "app.jar"]
