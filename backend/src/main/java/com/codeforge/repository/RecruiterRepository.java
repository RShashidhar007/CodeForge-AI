package com.codeforge.repository;

import com.codeforge.entity.Recruiter;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository for Recruiter entity
 */
@Repository
public interface RecruiterRepository extends JpaRepository<Recruiter, Long> {
    Page<Recruiter> findAll(Pageable pageable);
}
