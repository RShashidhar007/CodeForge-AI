package com.codeforge.service;

import com.codeforge.dto.request.CreateCompanyRequest;
import com.codeforge.dto.response.CompanyResponse;
import com.codeforge.dto.response.PageResponse;
import com.codeforge.dto.response.PlatformStatsResponse;
import com.codeforge.dto.response.UserSummaryResponse;
import com.codeforge.entity.Company;
import com.codeforge.entity.User;
import com.codeforge.entity.User.UserRole;
import com.codeforge.exception.DuplicateResourceException;
import com.codeforge.exception.ResourceNotFoundException;
import com.codeforge.repository.CandidateRepository;
import com.codeforge.repository.CompanyRepository;
import com.codeforge.repository.ProjectRepository;
import com.codeforge.repository.RecruiterRepository;
import com.codeforge.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.format.DateTimeFormatter;

/**
 * Service for admin operations
 */
@Service
@RequiredArgsConstructor
public class AdminService {
    
    private final UserRepository userRepository;
    private final CandidateRepository candidateRepository;
    private final RecruiterRepository recruiterRepository;
    private final CompanyRepository companyRepository;
    private final ProjectRepository projectRepository;
    
    /**
     * Get platform statistics
     */
    public PlatformStatsResponse getPlatformStats() {
        long totalUsers = userRepository.count();
        long totalCandidates = userRepository.countByRole(UserRole.CANDIDATE);
        long totalRecruiters = userRepository.countByRole(UserRole.RECRUITER);
        long totalCompanies = companyRepository.count();
        long totalProjects = projectRepository.count();
        
        long enabledUsers = userRepository.findAll().stream()
            .filter(User::getEnabled)
            .count();
        long disabledUsers = totalUsers - enabledUsers;
        
        return PlatformStatsResponse.builder()
            .totalUsers(totalUsers)
            .totalCandidates(totalCandidates)
            .totalRecruiters(totalRecruiters)
            .totalCompanies(totalCompanies)
            .totalProjects(totalProjects)
            .enabledUsers(enabledUsers)
            .disabledUsers(disabledUsers)
            .build();
    }
    
    /**
     * List users with pagination and optional role filter
     */
    public PageResponse<UserSummaryResponse> listUsers(UserRole role, Pageable pageable) {
        Page<User> page;
        
        if (role != null) {
            page = userRepository.findByRole(role, pageable);
        } else {
            page = userRepository.findAll(pageable);
        }
        
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
        
        return PageResponse.<UserSummaryResponse>builder()
            .content(page.getContent().stream()
                .map(user -> UserSummaryResponse.builder()
                    .id(user.getId())
                    .name(user.getName())
                    .email(user.getEmail())
                    .role(user.getRole().name())
                    .enabled(user.getEnabled())
                    .createdAt(user.getCreatedAt().format(formatter))
                    .build())
                .toList())
            .page(page.getNumber())
            .size(page.getSize())
            .totalPages(page.getTotalPages())
            .totalElements(page.getTotalElements())
            .last(page.isLast())
            .build();
    }
    
    /**
     * Set user enabled/disabled status
     */
    @Transactional
    public UserSummaryResponse setUserEnabled(Long userId, boolean enabled) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> ResourceNotFoundException.notFound("User", "id", userId));
        
        user.setEnabled(enabled);
        user = userRepository.save(user);
        
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
        
        return UserSummaryResponse.builder()
            .id(user.getId())
            .name(user.getName())
            .email(user.getEmail())
            .role(user.getRole().name())
            .enabled(user.getEnabled())
            .createdAt(user.getCreatedAt().format(formatter))
            .build();
    }
    
    /**
     * Create a new company
     */
    @Transactional
    public CompanyResponse createCompany(CreateCompanyRequest request) {
        if (companyRepository.existsByName(request.getName())) {
            throw DuplicateResourceException.alreadyExists("Company", "name", request.getName());
        }
        
        Company company = Company.builder()
            .name(request.getName())
            .description(request.getDescription())
            .website(request.getWebsite())
            .logoUrl(request.getLogoUrl())
            .build();
        
        company = companyRepository.save(company);
        
        return mapToCompanyResponse(company);
    }
    
    /**
     * List companies with pagination
     */
    public PageResponse<CompanyResponse> listCompanies(Pageable pageable) {
        Page<Company> page = companyRepository.findAll(pageable);
        
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
        
        return PageResponse.<CompanyResponse>builder()
            .content(page.getContent().stream()
                .map(this::mapToCompanyResponse)
                .toList())
            .page(page.getNumber())
            .size(page.getSize())
            .totalPages(page.getTotalPages())
            .totalElements(page.getTotalElements())
            .last(page.isLast())
            .build();
    }
    
    private CompanyResponse mapToCompanyResponse(Company company) {
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
        
        return CompanyResponse.builder()
            .id(company.getId())
            .name(company.getName())
            .description(company.getDescription())
            .website(company.getWebsite())
            .logoUrl(company.getLogoUrl())
            .createdAt(company.getCreatedAt().format(formatter))
            .build();
    }
}
