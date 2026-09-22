package com.codeforge.exception;

/**
 * Exception thrown when authentication credentials are invalid.
 * Maps to HTTP 401 Unauthorized status.
 */
public class BadCredentialsException extends RuntimeException {
    
    public BadCredentialsException(String message) {
        super(message);
    }

    public BadCredentialsException(String message, Throwable cause) {
        super(message, cause);
    }
}
