package com.codeforge.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationServiceException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;

import java.util.ArrayList;
import java.util.List;

/**
 * Global exception handler for all REST endpoints.
 * Centralizes error response formatting to match frontend expectations.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handle resource not found (404)
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(
            ResourceNotFoundException ex,
            WebRequest request) {
        
        ErrorResponse error = ErrorResponse.of(
            HttpStatus.NOT_FOUND.value(),
            "Not Found",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );
        
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    /**
     * Handle duplicate resource (409 Conflict)
     */
    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<ErrorResponse> handleDuplicateResource(
            DuplicateResourceException ex,
            WebRequest request) {
        
        ErrorResponse error = ErrorResponse.of(
            HttpStatus.CONFLICT.value(),
            "Conflict",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );
        
        return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
    }

    /**
     * Handle bad credentials (401 Unauthorized)
     */
    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<ErrorResponse> handleBadCredentials(
            BadCredentialsException ex,
            WebRequest request) {
        
        ErrorResponse error = ErrorResponse.of(
            HttpStatus.UNAUTHORIZED.value(),
            "Unauthorized",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );
        
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
    }

    /**
     * Handle Spring Security authentication failures (401)
     */
    @ExceptionHandler(AuthenticationServiceException.class)
    public ResponseEntity<ErrorResponse> handleAuthenticationFailure(
            AuthenticationServiceException ex,
            WebRequest request) {
        
        ErrorResponse error = ErrorResponse.of(
            HttpStatus.UNAUTHORIZED.value(),
            "Unauthorized",
            "Invalid credentials",
            request.getDescription(false).replace("uri=", "")
        );
        
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
    }

    /**
<<<<<<< HEAD
     * Handle access denied (403 Forbidden) — our own AccessDeniedException.
=======
     * Handle access denied (403 Forbidden)
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
     */
    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleAccessDenied(
            AccessDeniedException ex,
            WebRequest request) {
        
        ErrorResponse error = ErrorResponse.of(
            HttpStatus.FORBIDDEN.value(),
            "Forbidden",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );
        
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(error);
    }

    /**
<<<<<<< HEAD
     * Handle access denied (403 Forbidden) — Spring Security's own exception,
     * thrown by @PreAuthorize/hasRole checks. Without this handler these were
     * falling through to handleGlobalException() and returning 500 instead
     * of 403 for any authenticated-but-unauthorized request.
     */
    @ExceptionHandler(org.springframework.security.access.AccessDeniedException.class)
    public ResponseEntity<ErrorResponse> handleSpringSecurityAccessDenied(
            org.springframework.security.access.AccessDeniedException ex,
            WebRequest request) {

        ErrorResponse error = ErrorResponse.of(
            HttpStatus.FORBIDDEN.value(),
            "Forbidden",
            "You do not have permission to perform this action.",
            request.getDescription(false).replace("uri=", "")
        );

        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(error);
    }

    /**
=======
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
     * Handle validation errors (400 Bad Request)
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex,
            WebRequest request) {
        
        List<String> details = new ArrayList<>();
        ex.getBindingResult()
            .getFieldErrors()
            .forEach(error -> details.add(error.getField() + ": " + error.getDefaultMessage()));
        
        ErrorResponse error = ErrorResponse.of(
            HttpStatus.BAD_REQUEST.value(),
            "Bad Request",
            "Validation failed",
            request.getDescription(false).replace("uri=", ""),
            details
        );
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    /**
<<<<<<< HEAD
     * Handle bad request-shaped input (e.g. an invalid enum value such as an
     * unknown taskType in CreateTaskRequest) as 400 instead of 500.
     */
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ErrorResponse> handleIllegalArgument(
            IllegalArgumentException ex,
            WebRequest request) {

        ErrorResponse error = ErrorResponse.of(
            HttpStatus.BAD_REQUEST.value(),
            "Bad Request",
            ex.getMessage(),
            request.getDescription(false).replace("uri=", "")
        );

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    /**
=======
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
     * Handle all other exceptions (500 Internal Server Error)
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGlobalException(
            Exception ex,
            WebRequest request) {
        
        ErrorResponse error = ErrorResponse.of(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "Internal Server Error",
            "An unexpected error occurred",
            request.getDescription(false).replace("uri=", "")
        );
        
        // Log the exception for debugging
        ex.printStackTrace();
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
