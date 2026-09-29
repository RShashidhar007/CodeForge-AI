package com.codeforge.repository;

import com.codeforge.entity.GithubToken;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * Repository for GithubToken entity
 */
@Repository
public interface GithubTokenRepository extends JpaRepository<GithubToken, Long> {
    List<GithubToken> findByUserId(Long userId);
    
    Optional<GithubToken> findByUserIdAndUsername(Long userId, String username);
}
