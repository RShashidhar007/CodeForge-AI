package com.codeforge.exception;

/**
 * Exception thrown when user lacks required permissions.
 * Maps to HTTP 403 Forbidden status.
 */
public class AccessDeniedException extends RuntimeException {
    
    public AccessDeniedException(String message) {
        super(message);
    }

    public AccessDeniedException(String message, Throwable cause) {
        super(message, cause);
    }
}
