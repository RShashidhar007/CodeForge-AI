package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for platform statistics
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PlatformStatsResponse {
    
    @JsonProperty("total_users")
    private Long totalUsers;
    
    @JsonProperty("total_candidates")
    private Long totalCandidates;
    
    @JsonProperty("total_recruiters")
    private Long totalRecruiters;
    
    @JsonProperty("total_companies")
    private Long totalCompanies;
    
    @JsonProperty("total_projects")
    private Long totalProjects;
    
    @JsonProperty("enabled_users")
    private Long enabledUsers;
    
    @JsonProperty("disabled_users")
    private Long disabledUsers;
}
