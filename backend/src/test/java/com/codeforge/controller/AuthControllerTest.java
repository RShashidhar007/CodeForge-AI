package com.codeforge.controller;

import com.codeforge.dto.request.LoginRequest;
import com.codeforge.dto.request.RegisterCandidateRequest;
import com.codeforge.dto.response.LoginResponse;
import com.codeforge.dto.response.UserResponse;
import com.codeforge.service.AuthService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Integration tests for AuthController
 */
@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @MockBean
    private AuthService authService;
    
    private RegisterCandidateRequest registerRequest;
    private LoginRequest loginRequest;
    
    @BeforeEach
    void setUp() {
        registerRequest = new RegisterCandidateRequest("John Doe", "john@example.com", "password123");
        loginRequest = new LoginRequest("john@example.com", "password123");
    }
    
    @Test
    void testRegisterCandidateSuccess() throws Exception {
        // Arrange
        UserResponse userResponse = UserResponse.builder()
            .id(1L)
            .name("John Doe")
            .email("john@example.com")
            .role("CANDIDATE")
            .enabled(true)
            .build();
        
        when(authService.registerCandidate(any())).thenReturn(userResponse);
        
        // Act & Assert
        mockMvc.perform(post("/auth/register/candidate")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(registerRequest)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("John Doe"))
            .andExpect(jsonPath("$.email").value("john@example.com"))
            .andExpect(jsonPath("$.role").value("CANDIDATE"));
    }
    
    @Test
    void testLoginSuccess() throws Exception {
        // Arrange
        UserResponse userResponse = UserResponse.builder()
            .id(1L)
            .name("John Doe")
            .email("john@example.com")
            .role("CANDIDATE")
            .enabled(true)
            .build();
        
        LoginResponse loginResponse = LoginResponse.builder()
            .token("jwt_token")
            .tokenType("Bearer")
            .expiresInSeconds(86400)
            .user(userResponse)
            .build();
        
        when(authService.login(any())).thenReturn(loginResponse);
        
        // Act & Assert
        mockMvc.perform(post("/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(loginRequest)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.token").value("jwt_token"))
            .andExpect(jsonPath("$.token_type").value("Bearer"))
            .andExpect(jsonPath("$.expires_in_seconds").value(86400))
            .andExpect(jsonPath("$.user.email").value("john@example.com"));
    }
    
    @Test
    void testLoginValidationError() throws Exception {
        // Arrange
        LoginRequest invalidRequest = new LoginRequest("", "");
        
        // Act & Assert
        mockMvc.perform(post("/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(invalidRequest)))
            .andExpect(status().isBadRequest());
    }
}
