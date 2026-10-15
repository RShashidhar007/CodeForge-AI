package com.codeforge.exception;

/**
 * Exception thrown when repository import operations fail
 */
public class RepositoryImportException extends RuntimeException {
    public RepositoryImportException(String message) {
        super(message);
    }
    
    public RepositoryImportException(String message, Throwable cause) {
        super(message, cause);
    }
}
