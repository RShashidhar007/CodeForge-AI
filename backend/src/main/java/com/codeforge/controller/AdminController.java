package com.codeforge.controller;

import com.codeforge.dto.request.CreateCompanyRequest;
import com.codeforge.dto.response.CompanyResponse;
import com.codeforge.dto.response.PageResponse;
import com.codeforge.dto.response.PlatformStatsResponse;
import com.codeforge.dto.response.UserSummaryResponse;
import com.codeforge.entity.User.UserRole;
import com.codeforge.service.AdminService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

/**
 * Admin controller
 * Endpoints:
 * - GET /admin/stats
 * - GET /admin/users
 * - PATCH /admin/users/{id}/status
 * - POST /admin/companies
 * - GET /admin/companies
 */
@RestController
@RequestMapping("/admin")
@RequiredArgsConstructor
@PreAuthorize("hasRole('ADMIN')")
public class AdminController {
    
    private final AdminService adminService;
    
    /**
     * Get platform statistics
     * GET /admin/stats
     */
    @GetMapping("/stats")
    public ResponseEntity<PlatformStatsResponse> getStats() {
        PlatformStatsResponse response = adminService.getPlatformStats();
        return ResponseEntity.ok(response);
    }
    
    /**
     * List users with optional role filter and pagination
     * GET /admin/users?role=CANDIDATE&page=0&size=20
     */
    @GetMapping("/users")
    public ResponseEntity<PageResponse<UserSummaryResponse>> listUsers(
            @RequestParam(required = false) UserRole role,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        PageResponse<UserSummaryResponse> response = adminService.listUsers(role, pageable);
        return ResponseEntity.ok(response);
    }
    
    /**
     * Set user enabled/disabled status
     * PATCH /admin/users/{id}/status
     */
    @PatchMapping("/users/{id}/status")
    public ResponseEntity<UserSummaryResponse> setUserStatus(
            @PathVariable Long id,
            @RequestBody SetUserStatusRequest request) {
        UserSummaryResponse response = adminService.setUserEnabled(id, request.getEnabled());
        return ResponseEntity.ok(response);
    }
    
    /**
     * Create a new company
     * POST /admin/companies
     */
    @PostMapping("/companies")
    public ResponseEntity<CompanyResponse> createCompany(
            @Valid @RequestBody CreateCompanyRequest request) {
        CompanyResponse response = adminService.createCompany(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    /**
     * List companies with pagination
     * GET /admin/companies?page=0&size=20
     */
    @GetMapping("/companies")
    public ResponseEntity<PageResponse<CompanyResponse>> listCompanies(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        
        Pageable pageable = PageRequest.of(page, size);
        PageResponse<CompanyResponse> response = adminService.listCompanies(pageable);
        return ResponseEntity.ok(response);
    }
    
    /**
     * DTO for setting user status
     */
    @lombok.Data
    @lombok.NoArgsConstructor
    @lombok.AllArgsConstructor
    static class SetUserStatusRequest {
        private Boolean enabled;
    }
}
