package com.codeforge.exception;

/**
 * Exception thrown when attempting to create a resource that already exists.
 * Maps to HTTP 409 Conflict status.
 */
public class DuplicateResourceException extends RuntimeException {
    
    public DuplicateResourceException(String message) {
        super(message);
    }

    public DuplicateResourceException(String message, Throwable cause) {
        super(message, cause);
    }

    public static DuplicateResourceException alreadyExists(String resourceName, String fieldName, Object value) {
        return new DuplicateResourceException(
            String.format("%s already exists with %s: '%s'", resourceName, fieldName, value)
        );
    }
}
