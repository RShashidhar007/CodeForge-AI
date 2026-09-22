# Testing Guide - CodeForge AI Backend

## Overview

The backend includes comprehensive tests covering:
- Unit tests for services and security components
- Integration tests for controllers
- Repository tests for data access
- Security/authentication tests

## Running Tests

### All Tests
```bash
mvn test
```

### Specific Test Class
```bash
mvn test -Dtest=AuthServiceTest
```

### Specific Test Method
```bash
mvn test -Dtest=AuthServiceTest#testRegisterCandidateSuccess
```

### With Coverage Report
```bash
mvn test jacoco:report
# Report: target/site/jacoco/index.html
```

## Test Structure

### Unit Tests

**AuthServiceTest.java**
- Tests user registration (candidate, recruiter)
- Tests login functionality
- Tests error handling (duplicate user, invalid credentials, disabled user)
- Mocks dependencies (repositories, JWT provider, password encoder)

**JWTProviderTest.java**
- Tests token generation
- Tests token parsing (extract userId, email, role)
- Tests token validation
- Tests expired token handling

**UserRepositoryTest.java**
- Tests CRUD operations
- Tests findByEmail query
- Tests existsByEmail check
- Tests countByRole aggregation

### Integration Tests

**AuthControllerTest.java**
- Tests POST /auth/register/candidate endpoint
- Tests POST /auth/login endpoint
- Tests validation errors (400)
- Uses MockMvc for HTTP testing

## Test Configuration

Tests use `application-test.properties` which:
- Uses H2 in-memory database (instead of MSSQL)
- Disables actual Redis (for unit tests)
- Uses test JWT secret
- Enables debug logging

## Coverage Targets

| Component | Target Coverage |
|-----------|-----------------|
| Services  | 90%+ |
| Controllers | 85%+ |
| Repositories | 80%+ |
| Security | 95%+ |
| Exceptions | 100% |

Current coverage can be checked with:
```bash
mvn jacoco:report
```

## Key Test Scenarios

### Authentication Flow

1. **User Registration**
   ```
   POST /auth/register/candidate
   {
     "name": "John Doe",
     "email": "john@example.com",
     "password": "password123"
   }
   
   Response: 201 CREATED
   {
     "id": 1,
     "name": "John Doe",
     "email": "john@example.com",
     "role": "CANDIDATE"
   }
   ```

2. **User Login**
   ```
   POST /auth/login
   {
     "email": "john@example.com",
     "password": "password123"
   }
   
   Response: 200 OK
   {
     "token": "eyJhbGciOiJIUzI1NiIs...",
     "token_type": "Bearer",
     "expires_in_seconds": 86400,
     "user": {...}
   }
   ```

3. **Protected Endpoint Access**
   ```
   GET /candidates/me
   Authorization: Bearer <token>
   
   Response: 200 OK
   {
     "user_id": 1,
     "name": "John Doe",
     "email": "john@example.com",
     ...
   }
   ```

### Error Scenarios

1. **Duplicate Email**
   ```
   Error: 409 CONFLICT
   {
     "status": 409,
     "error": "Conflict",
     "message": "User already exists with email: john@example.com"
   }
   ```

2. **Invalid Credentials**
   ```
   Error: 401 UNAUTHORIZED
   {
     "status": 401,
     "error": "Unauthorized",
     "message": "Invalid email or password"
   }
   ```

3. **Validation Error**
   ```
   Error: 400 BAD_REQUEST
   {
     "status": 400,
     "error": "Bad Request",
     "message": "Validation failed",
     "details": [
       "email: must not be blank",
       "password: size must be between 8 and 2147483647"
     ]
   }
   ```

## Test Data

### Predefined Test User

Email: `test@example.com`
Password: `TestPassword123!`
Role: CANDIDATE

### Admin User (for admin tests)

Email: `admin@test.com`
Password: `TestPassword123!`
Role: ADMIN

## Mocking Strategy

### Service Layer Tests

Use `@Mock` for dependencies:
- `UserRepository` - User data access
- `CandidateRepository` - Candidate data access
- `JWTProvider` - JWT generation/validation
- `PasswordEncoder` - Password hashing

### Controller Tests

Use `@MockBean` for service layer:
- `AuthService` - Authentication service
- `CandidateService` - Candidate operations
- etc.

Use `MockMvc` for HTTP testing:
```java
mockMvc.perform(post("/auth/login")
    .contentType(MediaType.APPLICATION_JSON)
    .content(json))
    .andExpect(status().isOk())
    .andExpect(jsonPath("$.token").exists());
```

### Repository Tests

Use `@DataJpaTest` for:
- Database integration tests
- Real repository implementation
- H2 in-memory database

## Adding New Tests

### 1. Create Test Class
```java
@ExtendWith(MockitoExtension.class)  // For unit tests with mocks
class NewServiceTest {
    @Mock
    private SomeDependency dependency;
    
    @InjectMocks
    private ServiceUnderTest service;
    
    @Test
    void testSomethingWorks() {
        // Arrange
        when(dependency.doSomething()).thenReturn(value);
        
        // Act
        Result result = service.method();
        
        // Assert
        assertEquals(expected, result);
    }
}
```

### 2. Follow AAA Pattern

- **Arrange:** Set up test data and mocks
- **Act:** Execute the code being tested
- **Assert:** Verify the results

### 3. Name Tests Clearly

```java
// Good
void testRegisterCandidateWithValidDataSuccess() { }

// Bad
void test1() { }
void testStuff() { }
```

## Continuous Integration

Tests run automatically on:
- Every commit (via pre-commit hook if configured)
- Pull request creation
- Before deployment

Ensure all tests pass before pushing:
```bash
mvn clean test
```

## Troubleshooting Tests

### Test Fails: "Could not find constructor for class X"

**Issue:** Missing no-arg constructor in JPA entity
**Solution:** Add `@NoArgsConstructor` from Lombok

### Test Fails: "Database connection error"

**Issue:** Trying to use MSSQL in test (should use H2)
**Solution:** Verify `application-test.properties` is being used
```bash
mvn test -Dspring.profiles.active=test
```

### Test Fails: "JWT validation failed"

**Issue:** JWT secret mismatch
**Solution:** Ensure test JWT secret matches in `application-test.properties`

### Test Timeout

**Issue:** Long-running test or hanging connection
**Solution:** Add timeout annotation:
```java
@Test
@Timeout(5)  // 5 seconds
void testSomething() { }
```

## Performance Testing

For load testing endpoints:

1. **Install Apache JMeter**
2. **Create test plan** with:
   - Thread group (number of concurrent users)
   - HTTP requests (endpoint URLs)
   - Results listeners (latency, throughput)

3. **Run test plan**
```bash
jmeter -n -t testplan.jmx -l results.jtl
```

## Security Testing

### Test Cases

1. **Invalid JWT Token**
   - Expired token
   - Malformed token
   - Token with wrong secret

2. **Authorization**
   - Candidate accessing admin endpoint (403)
   - Missing Authorization header (401)
   - CANDIDATE accessing RECRUITER endpoint (403)

3. **SQL Injection**
   - Email field with SQL characters
   - Should be parameterized (not concatenated)

4. **Password Security**
   - Passwords must be hashed (never stored plaintext)
   - Use BCrypt for verification

## Integration Testing Checklist

- [ ] Database schema matches entity definitions
- [ ] Foreign key relationships work correctly
- [ ] Transactions rollback on error
- [ ] Cascading deletes work as expected
- [ ] Indexes improve query performance
- [ ] Connection pooling works correctly
- [ ] Redis caching functions properly

## Test Report

Generate HTML test report:
```bash
mvn surefire-report:report
```

Report location: `target/site/surefire-report.html`

Includes:
- Total tests run
- Passed/failed/skipped counts
- Failure details and stack traces
- Execution time per test
- Overall success rate
