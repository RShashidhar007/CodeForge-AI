package com.codeforge.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Health check endpoint
 * GET /actuator/health
 */
@RestController
public class HealthController {
    
    /**
     * Health check endpoint
     * GET /actuator/health
     */
    @GetMapping("/actuator/health")
    public Map<String, Object> health() {
        Map<String, Object> response = new LinkedHashMap<>();
        response.put("status", "UP");
        response.put("timestamp", System.currentTimeMillis());
        return response;
    }
}
