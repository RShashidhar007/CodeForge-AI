package com.codeforge.exception;

/**
 * Exception thrown when a requested resource is not found in the database.
 * Maps to HTTP 404 status.
 */
public class ResourceNotFoundException extends RuntimeException {
    
    public ResourceNotFoundException(String message) {
        super(message);
    }

    public ResourceNotFoundException(String message, Throwable cause) {
        super(message, cause);
    }

    public static ResourceNotFoundException notFound(String resourceName, String fieldName, Object value) {
        return new ResourceNotFoundException(
            String.format("%s not found with %s: '%s'", resourceName, fieldName, value)
        );
    }
}
