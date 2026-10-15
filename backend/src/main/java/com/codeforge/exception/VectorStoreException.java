package com.codeforge.exception;

/**
 * Exception thrown when vector store (Qdrant) operations fail
 */
public class VectorStoreException extends RuntimeException {
    public VectorStoreException(String message) {
        super(message);
    }
    
    public VectorStoreException(String message, Throwable cause) {
        super(message, cause);
    }
}
