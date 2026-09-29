# CodeForge AI - Deployment Guide

Complete guide for deploying CodeForge AI with Spring Boot backend to production environments.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Monitoring & Logging](#monitoring--logging)
7. [Troubleshooting](#troubleshooting)

---

## Local Development

### Prerequisites
- **Java 17+** (check: `java -version`)
- **Maven 3.9+** (check: `mvn -version`)
- **Node.js 18+** (check: `node -v`)
- **Docker & Docker Compose** (for database & cache)
- **Git**

### Quick Setup (5 minutes)

**1. Clone Repository:**
```bash
git clone https://github.com/RShashidhar007/CodeForge-AI.git
cd CodeForge-AI
```

**2. Setup Backend:**
```bash
cd backend

# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional for local dev)
# nano .env  # or edit in your editor

# Build with Maven
mvn clean install

# Run the application
java -jar target/codeforge-backend-1.0.0.jar
```

**3. Setup Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend will be available at http://localhost:5173
```

**4. Access Services:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080/api
- Health Check: http://localhost:8080/api/actuator/health
- Swagger UI: http://localhost:8080/api/swagger-ui.html

---

## Docker Deployment

### Complete Stack with Docker Compose

**Start all services:**
```bash
cd CodeForge-AI

# Copy environment configuration
cp backend/.env.example backend/.env

# Build and start all services
docker-compose up --build

# Wait 30-60 seconds for all services to start...
```

**Access points:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080/api
- MSSQL Server: localhost:1433 (user: sa, password: Admin@123456)
- Redis: localhost:6379

**View logs:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f mssql
docker-compose logs -f redis
```

**Stop services:**
```bash
# Graceful stop
docker-compose down

# Stop and remove data
docker-compose down -v
```

**Rebuild specific service:**
```bash
docker-compose build --no-cache backend
docker-compose up backend
```

### Docker Service Details

**Spring Boot Backend Container:**
- Image: `codeforge-backend:latest`
- Port: 8080
- Context Path: `/api`
- Health Check: Enabled (every 30s)
- Depends On: MSSQL (healthy), Redis (healthy)

**MSSQL Server Container:**
- Image: `mcr.microsoft.com/mssql/server:2022-latest`
- Port: 1433
- Default User: `sa`
- Default Password: `Admin@123456`
- Volume: Named volume `recruitment_platform_mssqldata`

**Redis Container:**
- Image: `redis:7-alpine`
- Port: 6379
- Volume: Named volume `recruitment_platform_redisdata`
- Health Check: Enabled (every 5s)

---

## Production Deployment

### Prerequisites for Production
- Java 17+ (Long-Term Support version recommended)
- MSSQL Server 2022+ (managed service or self-hosted)
- Redis 7+ (managed service or self-hosted)
- SSL/TLS certificates
- Domain name

### Option 1: Docker Swarm

**Initialize Swarm:**
```bash
docker swarm init
```

**Create secrets:**
```bash
echo "your-jwt-secret-32-chars-minimum" | docker secret create jwt_secret -
echo "Admin@123456" | docker secret create db_password -
echo "sk-xxx..." | docker secret create openai_key -
```

**Deploy stack:**
```bash
docker stack deploy -c docker-compose.yml codeforge
```

**Monitor deployment:**
```bash
docker service ls
docker service logs codeforge_backend
```

### Option 2: Kubernetes

**Create namespace:**
```bash
kubectl create namespace codeforge
```

**Create secrets:**
```bash
kubectl create secret generic app-secrets \
  --from-literal=jwt-secret='your-jwt-secret-32-chars' \
  --from-literal=db-password='your-db-password' \
  --from-literal=openai-key='sk-xxx...' \
  -n codeforge
```

**Deploy:**
```bash
kubectl apply -f k8s/deployment.yaml -n codeforge
```

**Monitor:**
```bash
kubectl get pods -n codeforge
kubectl logs -f deployment/codeforge-backend -n codeforge
```

### Option 3: Virtual Machine Deployment

**1. Install Java:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y openjdk-17-jdk

# CentOS/RHEL
sudo yum install -y java-17-openjdk
```

**2. Setup application user:**
```bash
sudo useradd -r -m -s /bin/bash codeforge
```

**3. Deploy JAR:**
```bash
sudo cp target/codeforge-backend-1.0.0.jar /opt/codeforge/
sudo chown codeforge:codeforge /opt/codeforge/codeforge-backend-1.0.0.jar
sudo chmod 755 /opt/codeforge/codeforge-backend-1.0.0.jar
```

**4. Create systemd service:**
```bash
sudo nano /etc/systemd/system/codeforge-backend.service
```

**Service content:**
```ini
[Unit]
Description=CodeForge AI Backend
After=network.target

[Service]
Type=simple
User=codeforge
WorkingDirectory=/opt/codeforge
Environment="SPRING_PROFILES_ACTIVE=prod"
Environment="SPRING_CONFIG_LOCATION=file:/etc/codeforge/.env"
ExecStart=/usr/lib/jvm/java-17-openjdk-amd64/bin/java -jar codeforge-backend-1.0.0.jar
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**5. Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable codeforge-backend
sudo systemctl start codeforge-backend
sudo systemctl status codeforge-backend
```

**View logs:**
```bash
sudo journalctl -u codeforge-backend -f
```

---

## Environment Configuration

### Spring Boot Properties

**Production Configuration (`application-prod.properties`):**

```properties
# Server
server.port=8080
server.servlet.context-path=/api
server.compression.enabled=true
server.compression.min-response-size=1024

# Database
spring.datasource.url=jdbc:sqlserver://mssql-server:1433;databaseName=recruitment_platform;encrypt=true;trustServerCertificate=true;
spring.datasource.username=sa
spring.datasource.password=${DB_PASSWORD}
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000

# JPA/Hibernate
spring.jpa.database-platform=org.hibernate.dialect.SQLServerDialect
spring.jpa.hibernate.ddl-auto=none
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=false
spring.jpa.properties.hibernate.jdbc.batch_size=20
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true

# Redis
spring.redis.host=${REDIS_HOST}
spring.redis.port=${REDIS_PORT}
spring.redis.timeout=60000ms
spring.cache.type=redis
spring.cache.redis.time-to-live=3600000

# JWT
app.jwt.secret=${JWT_SECRET}
app.jwt.expiration=${JWT_EXPIRATION_SECONDS:86400}
app.jwt.algorithm=HS256

# CORS
app.cors.allowed-origins=${CORS_ALLOWED_ORIGINS}

# Admin Bootstrap
app.admin.email=${ADMIN_EMAIL}
app.admin.password=${ADMIN_PASSWORD}
app.admin.name=${ADMIN_NAME}

# AI/LLM
app.ai.llm.provider=${LLM_PROVIDER:openai}
app.ai.llm.model=${LLM_MODEL:gpt-4-turbo}
app.ai.llm.api-key=${LLM_API_KEY}

# Logging
logging.level.root=WARN
logging.level.com.codeforge=INFO
logging.file.name=/var/log/codeforge/app.log
logging.file.max-size=10MB
logging.file.max-history=10
logging.pattern.file=%d{yyyy-MM-dd HH:mm:ss} - %msg%n

# Actuator
management.endpoints.web.exposure.include=health,metrics,prometheus
management.endpoint.health.show-details=when-authorized
management.health.livenessState.enabled=true
management.health.readinessState.enabled=true
```

### Environment Variables

**Required for Production:**
```bash
# Database
DB_PASSWORD=your-secure-password-here

# JWT (minimum 32 characters)
JWT_SECRET=your-super-secret-jwt-key-minimum-32-chars-long

# Admin Account
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=YourSecureAdminPassword!123

# Redis
REDIS_HOST=redis-server.internal
REDIS_PORT=6379

# AI/LLM (if using OpenAI)
LLM_API_KEY=sk-your-openai-key-here

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Optional:**
```bash
JWT_EXPIRATION_SECONDS=86400
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
EMBEDDING_API_KEY=sk-your-embedding-key
ADMIN_NAME=Platform Administrator
```

---

## Database Setup

### MSSQL Server 2022

**1. Create Database:**
```sql
CREATE DATABASE recruitment_platform;
USE recruitment_platform;
```

**2. Create Login:**
```sql
CREATE LOGIN codeforge WITH PASSWORD = 'YourSecurePassword123!';
CREATE USER codeforge FOR LOGIN codeforge;
ALTER ROLE db_owner ADD MEMBER codeforge;
```

**3. Verify Connection:**
```bash
# From command line
sqlcmd -S <server> -U codeforge -P <password> -d recruitment_platform -Q "SELECT 1;"
```

**4. Backup Strategy:**
```sql
-- Full backup daily
BACKUP DATABASE recruitment_platform 
TO DISK = '/var/opt/mssql/backup/codeforge_full.bak' 
WITH INIT, COMPRESSION;

-- Transaction log backup every hour
BACKUP LOG recruitment_platform 
TO DISK = '/var/opt/mssql/backup/codeforge_log.trn' 
WITH INIT, COMPRESSION;
```

### Redis Configuration

**Production Redis Setup:**
```bash
# Install Redis on Linux
sudo apt-get install -y redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf

# Key settings:
# maxmemory 1gb
# maxmemory-policy allkeys-lru
# appendonly yes  (for persistence)
# requirepass your-redis-password

# Start Redis
sudo systemctl restart redis-server
```

---

## Monitoring & Logging

### Health Checks

**Liveness Probe:**
```bash
curl http://localhost:8080/api/actuator/health/liveness
```

**Readiness Probe:**
```bash
curl http://localhost:8080/api/actuator/health/readiness
```

**Full Health:**
```bash
curl http://localhost:8080/api/actuator/health
```

### Metrics

**Prometheus Endpoint:**
```bash
curl http://localhost:8080/api/actuator/prometheus
```

**Key Metrics:**
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `db_connection_pool_active` - Active database connections
- `cache_hits_total` - Redis cache hits
- `jvm_memory_used_bytes` - JVM memory usage

### Logging

**Structured Logging with JSON:**
```bash
# Update application-prod.properties
logging.pattern.json={"timestamp":"%d{ISO8601}","level":"%p","logger":"%c","message":"%m"}
```

**Log Aggregation (ELK Stack):**
```bash
# Use Logstash to forward logs
logstash -e 'input { file { path => "/var/log/codeforge/app.log" } } 
             output { elasticsearch { hosts => ["elasticsearch:9200"] } }'
```

### Performance Tuning

**JVM Heap Configuration:**
```bash
# Set in systemd service or Docker environment
JAVA_OPTS="-Xms1g -Xmx2g -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
```

**Connection Pooling:**
```properties
spring.datasource.hikari.maximum-pool-size=30
spring.datasource.hikari.minimum-idle=10
spring.datasource.hikari.connection-timeout=30000
```

---

## Troubleshooting

### Backend Won't Start

**Check Java version:**
```bash
java -version  # Should be 17+
```

**Check port in use:**
```bash
# Linux/Mac
lsof -i :8080

# Windows
netstat -ano | findstr :8080
```

**Check logs:**
```bash
# Docker
docker logs codeforge_backend

# Systemd
sudo journalctl -u codeforge-backend -f

# Direct run
# Check console output for errors
```

### Database Connection Issues

**Test MSSQL Connection:**
```bash
# Using sqlcmd
sqlcmd -S localhost,1433 -U sa -P Admin@123456 -Q "SELECT 1;"

# Using Docker
docker exec -it recruitment-platform-mssql \
  /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P Admin@123456 -Q "SELECT 1;"
```

**Check connection pool:**
```
GET http://localhost:8080/api/actuator/health

# Look for DataSourceHealthIndicator.database=UP
```

### Redis Connection Issues

**Test Redis Connection:**
```bash
# Using redis-cli
redis-cli ping

# From Docker
docker exec -it recruitment-platform-redis redis-cli ping
```

**Check cache:**
```bash
# Monitor Redis commands
redis-cli MONITOR

# Check memory usage
redis-cli INFO memory
```

### High Memory Usage

**Check JVM heap:**
```bash
# Get heap dump
jmap -dump:live,format=b,file=heap.bin <pid>

# Analyze with Eclipse MAT or jhat
jhat heap.bin
```

**Reduce heap size:**
```bash
# In application-prod.properties
JAVA_OPTS="-Xms512m -Xmx1g"
```

### Slow Queries

**Enable query logging:**
```properties
# In application-prod.properties
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.type.descriptor.sql.BasicBinder=TRACE
```

**Analyze slow queries:**
```sql
-- In MSSQL
SET STATISTICS IO ON;
SET STATISTICS TIME ON;

-- Run your query
SELECT * FROM users WHERE email = 'user@example.com';

-- Check execution plan
```

### SSL/TLS Configuration

**Enable HTTPS:**
```properties
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=${KEYSTORE_PASSWORD}
server.ssl.key-store-type=PKCS12
server.ssl.key-alias=tomcat
```

**Generate Keystore:**
```bash
keytool -genkey -alias tomcat -storetype PKCS12 -keyalg RSA \
  -keysize 2048 -keystore keystore.p12 -validity 365
```

---

## Scaling & Load Balancing

### Horizontal Scaling with Docker Compose

```yaml
services:
  backend:
    replicas: 3  # Run 3 instances
    deploy:
      replicas: 3
```

### Nginx Load Balancer Configuration

```nginx
upstream codeforge_backend {
    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location /api {
        proxy_pass http://codeforge_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Security Checklist

- ✅ Environment variables for all secrets (never in code)
- ✅ HTTPS/TLS enabled in production
- ✅ JWT secret is 32+ characters
- ✅ Passwords hashed with BCrypt
- ✅ Database user has minimal required permissions
- ✅ Redis requires authentication
- ✅ CORS configured to specific domains only
- ✅ SQL injection protection (Spring Data JPA)
- ✅ Rate limiting enabled
- ✅ Audit logging configured

---

## Backup & Disaster Recovery

### Database Backups

**Daily Backup Script:**
```bash
#!/bin/bash
BACKUP_DIR="/mnt/backups/codeforge"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Backup MSSQL
docker exec recruitment-platform-mssql \
  /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P $DB_PASSWORD \
  -Q "BACKUP DATABASE recruitment_platform TO DISK = '/var/opt/mssql/backup/codeforge_$TIMESTAMP.bak';"

# Backup Redis
docker exec recruitment-platform-redis \
  redis-cli BGSAVE

# Copy to safe location
cp /var/opt/mssql/backup/codeforge_$TIMESTAMP.bak $BACKUP_DIR/

# Keep only last 7 days
find $BACKUP_DIR -name "codeforge_*.bak" -mtime +7 -delete
```

**Schedule with cron:**
```bash
# Daily at 2 AM
0 2 * * * /path/to/backup-script.sh
```

### Restore Procedure

```sql
-- Restore MSSQL
USE master;
RESTORE DATABASE recruitment_platform 
FROM DISK = '/var/opt/mssql/backup/codeforge_20260922_020000.bak' 
WITH REPLACE;
```

---

## Support & Documentation

- **Backend Docs**: See `docs/BACKEND.md`
- **Testing Guide**: See `docs/TESTING.md`
- **Project Docs**: See `docs/PROJECT_DOCUMENTATION.md`
- **API Reference**: http://your-domain:8080/api/swagger-ui.html
- **GitHub Issues**: https://github.com/RShashidhar007/CodeForge-AI/issues

---

**Last Updated**: September 2026  
**Version**: 1.0.0
