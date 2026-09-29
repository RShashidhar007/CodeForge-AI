package com.codeforge.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

/**
 * Candidate profile entity (1:1 with User, role=CANDIDATE)
 */
@Entity
@Table(name = "candidates")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(exclude = {"user"})
@ToString(exclude = {"user"})
public class Candidate {
    
    @Id
    private Long id;
    
    @MapsId
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "id")
    private User user;
    
    @Column(length = 20)
    private String phone;
    
    @Column(length = 255)
    private String location;
    
    @Column(columnDefinition = "TEXT")
    private String bio;
    
    @Column(length = 500)
    private String githubUrl;
    
    @Column(length = 500)
    private String linkedinUrl;
    
    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;
}
