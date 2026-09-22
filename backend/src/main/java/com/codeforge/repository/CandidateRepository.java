package com.codeforge.repository;

import com.codeforge.entity.Candidate;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * Repository for Candidate entity
 */
@Repository
public interface CandidateRepository extends JpaRepository<Candidate, Long> {
    Page<Candidate> findAll(Pageable pageable);
}
