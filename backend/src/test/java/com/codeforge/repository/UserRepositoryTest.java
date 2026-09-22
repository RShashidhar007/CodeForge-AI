package com.codeforge.repository;

import com.codeforge.entity.User;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Integration tests for UserRepository
 */
@DataJpaTest
class UserRepositoryTest {
    
    @Autowired
    private UserRepository userRepository;
    
    private User testUser;
    
    @BeforeEach
    void setUp() {
        testUser = User.builder()
            .name("Test User")
            .email("test@example.com")
            .passwordHash("hashed_password")
            .role(User.UserRole.CANDIDATE)
            .enabled(true)
            .build();
    }
    
    @Test
    void testSaveUser() {
        // Act
        User savedUser = userRepository.save(testUser);
        
        // Assert
        assertNotNull(savedUser.getId());
        assertEquals("Test User", savedUser.getName());
        assertEquals("test@example.com", savedUser.getEmail());
    }
    
    @Test
    void testFindByEmail() {
        // Arrange
        userRepository.save(testUser);
        
        // Act
        Optional<User> foundUser = userRepository.findByEmail("test@example.com");
        
        // Assert
        assertTrue(foundUser.isPresent());
        assertEquals("Test User", foundUser.get().getName());
    }
    
    @Test
    void testFindByEmailNotFound() {
        // Act
        Optional<User> foundUser = userRepository.findByEmail("nonexistent@example.com");
        
        // Assert
        assertFalse(foundUser.isPresent());
    }
    
    @Test
    void testExistsByEmail() {
        // Arrange
        userRepository.save(testUser);
        
        // Act
        boolean exists = userRepository.existsByEmail("test@example.com");
        
        // Assert
        assertTrue(exists);
    }
    
    @Test
    void testCountByRole() {
        // Arrange
        userRepository.save(testUser);
        
        // Act
        long count = userRepository.countByRole(User.UserRole.CANDIDATE);
        
        // Assert
        assertTrue(count > 0);
    }
}
