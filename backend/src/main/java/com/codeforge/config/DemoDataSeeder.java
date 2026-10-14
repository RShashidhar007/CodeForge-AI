package com.codeforge.config;

import com.codeforge.entity.Candidate;
import com.codeforge.entity.Company;
import com.codeforge.entity.Recruiter;
import com.codeforge.entity.User;
import com.codeforge.repository.CandidateRepository;
import com.codeforge.repository.CompanyRepository;
import com.codeforge.repository.RecruiterRepository;
import com.codeforge.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * Seeds the database with demo recruiters and candidates on application startup.
 * This makes it easy to test the platform without manual registration.
 */
//@Component  // Temporarily disabled due to JPA cascade issues
@RequiredArgsConstructor
@Slf4j
public class DemoDataSeeder implements ApplicationRunner {

    private final UserRepository userRepository;
    private final CandidateRepository candidateRepository;
    private final RecruiterRepository recruiterRepository;
    private final CompanyRepository companyRepository;
    private final PasswordEncoder passwordEncoder;

    private static final String DEMO_PASSWORD = "Demo123!";

    @Override
    public void run(ApplicationArguments args) {
        log.info("Starting demo data seeding...");
        seedCompanies();
        seedCandidates();
        seedRecruiters();
        log.info("Demo data seeding completed!");
    }

    private void seedCompanies() {
        if (companyRepository.count() > 0) {
            log.info("Companies already exist, skipping company seeding");
            return;
        }

        List<Company> companies = new ArrayList<>();
        
        companies.add(Company.builder()
            .name("TechCorp Solutions")
            .description("Leading technology solutions provider based in San Francisco, CA")
            .website("https://techcorp.example.com")
            .build());
        
        companies.add(Company.builder()
            .name("DataViz Analytics")
            .description("Advanced data visualization and analytics platform in New York, NY")
            .website("https://dataviz.example.com")
            .build());
        
        companies.add(Company.builder()
            .name("CloudStack Systems")
            .description("Cloud infrastructure and DevOps solutions from Seattle, WA")
            .website("https://cloudstack.example.com")
            .build());
        
        companies.add(Company.builder()
            .name("FinTech Innovations")
            .description("Financial technology and blockchain solutions headquartered in Boston, MA")
            .website("https://fintech.example.com")
            .build());
        
        companies.add(Company.builder()
            .name("AI Research Labs")
            .description("Cutting-edge artificial intelligence research center in Austin, TX")
            .website("https://airesearch.example.com")
            .build());

        companyRepository.saveAll(companies);
        log.info("Seeded {} companies", companies.size());
    }

    private void seedCandidates() {
        if (candidateRepository.count() > 0) {
            log.info("Candidates already exist, skipping candidate seeding");
            return;
        }

        // Alice - Full Stack Developer
        User alice = createUserIfNotExists("alice@student.com", "Alice Johnson", User.UserRole.CANDIDATE);
        if (alice != null && !candidateRepository.existsById(alice.getId())) {
            Candidate candidate = Candidate.builder()
                .id(alice.getId())  // Set ID explicitly
                .user(alice)
                .phone("+1-555-0101")
                .location("San Francisco, CA")
                .bio("Full Stack Developer with 5+ years of experience in Java, React, and cloud technologies")
                .githubUrl("https://github.com/alice")
                .linkedinUrl("https://linkedin.com/in/alice")
                .build();
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", alice.getEmail());
        }

        // Bob - Backend Developer
        User bob = createUserIfNotExists("bob@student.com", "Bob Smith", User.UserRole.CANDIDATE);
        if (bob != null && !candidateRepository.existsById(bob.getId())) {
            Candidate candidate = Candidate.builder()
                .id(bob.getId())
                .user(bob)
                .phone("+1-555-0102")
                .location("New York, NY")
                .bio("Backend Engineer specializing in microservices, Spring Boot, and databases")
                .githubUrl("https://github.com/bob")
                .linkedinUrl("https://linkedin.com/in/bob")
                .build();
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", bob.getEmail());
        }

        // Carol - Data Scientist
        User carol = createUserIfNotExists("carol@student.com", "Carol Williams", User.UserRole.CANDIDATE);
        if (carol != null && !candidateRepository.existsById(carol.getId())) {
            Candidate candidate = Candidate.builder()
                .id(carol.getId())
                .user(carol)
                .phone("+1-555-0103")
                .location("Boston, MA")
                .bio("Data Scientist with expertise in Python, Machine Learning, and Data Analytics")
                .githubUrl("https://github.com/carol")
                .linkedinUrl("https://linkedin.com/in/carol")
                .build();
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", carol.getEmail());
        }

        // David - Frontend Developer
        User david = createUserIfNotExists("david@student.com", "David Brown", User.UserRole.CANDIDATE);
        if (david != null && !candidateRepository.existsById(david.getId())) {
            Candidate candidate = Candidate.builder()
                .id(david.getId())
                .user(david)
                .phone("+1-555-0104")
                .location("Seattle, WA")
                .bio("Frontend Developer passionate about React, TypeScript, and UX design")
                .githubUrl("https://github.com/david")
                .linkedinUrl("https://linkedin.com/in/david")
                .build();
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", david.getEmail());
        }

        // Emma - DevOps Engineer
        User emma = createUserIfNotExists("emma@student.com", "Emma Davis", User.UserRole.CANDIDATE);
        if (emma != null && !candidateRepository.existsById(emma.getId())) {
            Candidate candidate = Candidate.builder()
                .id(emma.getId())
                .user(emma)
                .phone("+1-555-0105")
                .location("Austin, TX")
                .bio("DevOps Engineer with 6+ years in AWS, Kubernetes, and CI/CD pipelines")
                .githubUrl("https://github.com/emma")
                .linkedinUrl("https://linkedin.com/in/emma")
                .build();
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", emma.getEmail());
        }

        log.info("Candidate seeding completed");
    }

    private void seedRecruiters() {
        if (recruiterRepository.count() > 0) {
            log.info("Recruiters already exist, skipping recruiter seeding");
            return;
        }
        
        // Get companies
        Company techCorp = companyRepository.findByName("TechCorp Solutions").orElse(null);
        Company dataViz = companyRepository.findByName("DataViz Analytics").orElse(null);
        Company cloudStack = companyRepository.findByName("CloudStack Systems").orElse(null);
        Company fintech = companyRepository.findByName("FinTech Innovations").orElse(null);
        Company aiLabs = companyRepository.findByName("AI Research Labs").orElse(null);

        // Sarah - TechCorp Solutions
        User sarah = createUserIfNotExists("sarah@recruiter.com", "Sarah Anderson", User.UserRole.RECRUITER);
        if (sarah != null && techCorp != null && !recruiterRepository.existsById(sarah.getId())) {
            Recruiter recruiter = Recruiter.builder()
                .id(sarah.getId())
                .user(sarah)
                .company(techCorp)
                .phone("+1-555-1001")
                .position("Senior Technical Recruiter")
                .bio("Specialized in recruiting software engineers for full-stack and backend positions")
                .build();
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", sarah.getEmail());
        }

        // James - DataViz Analytics
        User james = createUserIfNotExists("james@recruiter.com", "James Miller", User.UserRole.RECRUITER);
        if (james != null && dataViz != null && !recruiterRepository.existsById(james.getId())) {
            Recruiter recruiter = Recruiter.builder()
                .id(james.getId())
                .user(james)
                .company(dataViz)
                .phone("+1-555-1002")
                .position("Hiring Manager")
                .bio("Looking for talented data scientists and analytics engineers")
                .build();
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", james.getEmail());
        }

        // Lisa - CloudStack Systems
        User lisa = createUserIfNotExists("lisa@recruiter.com", "Lisa Taylor", User.UserRole.RECRUITER);
        if (lisa != null && cloudStack != null && !recruiterRepository.existsById(lisa.getId())) {
            Recruiter recruiter = Recruiter.builder()
                .id(lisa.getId())
                .user(lisa)
                .company(cloudStack)
                .phone("+1-555-1003")
                .position("DevOps Recruiter")
                .bio("Recruiting cloud architects and DevOps engineers for enterprise solutions")
                .build();
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", lisa.getEmail());
        }

        // Michael - FinTech Innovations
        User michael = createUserIfNotExists("michael@recruiter.com", "Michael Chen", User.UserRole.RECRUITER);
        if (michael != null && fintech != null && !recruiterRepository.existsById(michael.getId())) {
            Recruiter recruiter = Recruiter.builder()
                .id(michael.getId())
                .user(michael)
                .company(fintech)
                .phone("+1-555-1004")
                .position("Engineering Recruiter")
                .bio("Building the team for blockchain and fintech innovation")
                .build();
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", michael.getEmail());
        }

        // Jennifer - AI Research Labs
        User jennifer = createUserIfNotExists("jennifer@recruiter.com", "Jennifer Wilson", User.UserRole.RECRUITER);
        if (jennifer != null && aiLabs != null && !recruiterRepository.existsById(jennifer.getId())) {
            Recruiter recruiter = Recruiter.builder()
                .id(jennifer.getId())
                .user(jennifer)
                .company(aiLabs)
                .phone("+1-555-1005")
                .position("AI/ML Recruiter")
                .bio("Recruiting ML engineers and AI researchers for cutting-edge projects")
                .build();
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", jennifer.getEmail());
        }

        log.info("Recruiter seeding completed");
    }

    /**
     * Creates a user if it doesn't already exist.
     * Returns the user entity (either existing or newly created).
     */
    private User createUserIfNotExists(String email, String name, User.UserRole role) {
        // Check if user exists and return it
        if (userRepository.existsByEmail(email)) {
            log.debug("User {} already exists", email);
            return userRepository.findByEmail(email).orElse(null);
        }

        // Create and save new user
        User user = User.builder()
            .name(name)
            .email(email)
            .passwordHash(passwordEncoder.encode(DEMO_PASSWORD))
            .role(role)
            .enabled(true)
            .build();

        User savedUser = userRepository.save(user);
        log.debug("Created user {} with role {}", email, role);
        return savedUser;
    }
}
