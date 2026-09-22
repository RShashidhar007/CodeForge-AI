package com.codeforge.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for company
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CompanyResponse {
    
    private Long id;
    private String name;
    private String description;
    private String website;
    
    @JsonProperty("logo_url")
    private String logoUrl;
    
    @JsonProperty("created_at")
    private String createdAt;
}
