package com.codeforge.exception;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.util.List;

/**
 * Standardized error response DTO.
 * Sent in all error responses to match frontend expectations.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ErrorResponse {
    
    private String timestamp;
    private int status;
    private String error;
    private String message;
    private String path;
    private List<String> details;

    public static ErrorResponse of(int status, String error, String message, String path) {
        return ErrorResponse.builder()
            .timestamp(ZonedDateTime.now().toString())
            .status(status)
            .error(error)
            .message(message)
            .path(path)
            .build();
    }

    public static ErrorResponse of(int status, String error, String message, String path, List<String> details) {
        return ErrorResponse.builder()
            .timestamp(ZonedDateTime.now().toString())
            .status(status)
            .error(error)
            .message(message)
            .path(path)
            .details(details)
            .build();
    }
}
