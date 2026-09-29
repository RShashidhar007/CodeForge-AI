package com.codeforge.dto.request;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Request DTO for creating a company
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class CreateCompanyRequest {
    
    private String name;
    private String description;
    private String website;
    private String logoUrl;
}
