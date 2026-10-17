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
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;

/**
 * Seeds the database with demo recruiters and candidates on application startup.
 * This makes it easy to test the platform without manual registration.
 */
@Component  // Enabled to create demo users
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

    @Transactional
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

    @Transactional
    private void seedCandidates() {
        if (candidateRepository.count() > 0) {
            log.info("Candidates already exist, skipping candidate seeding");
            return;
        }

        // Alice - Full Stack Developer
        User alice = createUserIfNotExists("alice@student.com", "Alice Johnson", User.UserRole.CANDIDATE);
        if (alice != null && !candidateRepository.existsById(alice.getId())) {
            Candidate candidate = new Candidate();
            candidate.setUser(alice);  // This sets the ID via @MapsId
            candidate.setPhone("+1-555-0101");
            candidate.setLocation("San Francisco, CA");
            candidate.setBio("Full Stack Developer with 5+ years of experience in Java, React, and cloud technologies");
            candidate.setGithubUrl("https://github.com/alice");
            candidate.setLinkedinUrl("https://linkedin.com/in/alice");
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", alice.getEmail());
        }

        // Bob - Backend Developer
        User bob = createUserIfNotExists("bob@student.com", "Bob Smith", User.UserRole.CANDIDATE);
        if (bob != null && !candidateRepository.existsById(bob.getId())) {
            Candidate candidate = new Candidate();
            candidate.setUser(bob);
            candidate.setPhone("+1-555-0102");
            candidate.setLocation("New York, NY");
            candidate.setBio("Backend Engineer specializing in microservices, Spring Boot, and databases");
            candidate.setGithubUrl("https://github.com/bob");
            candidate.setLinkedinUrl("https://linkedin.com/in/bob");
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", bob.getEmail());
        }

        // Carol - Data Scientist
        User carol = createUserIfNotExists("carol@student.com", "Carol Williams", User.UserRole.CANDIDATE);
        if (carol != null && !candidateRepository.existsById(carol.getId())) {
            Candidate candidate = new Candidate();
            candidate.setUser(carol);
            candidate.setPhone("+1-555-0103");
            candidate.setLocation("Boston, MA");
            candidate.setBio("Data Scientist with expertise in Python, Machine Learning, and Data Analytics");
            candidate.setGithubUrl("https://github.com/carol");
            candidate.setLinkedinUrl("https://linkedin.com/in/carol");
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", carol.getEmail());
        }

        // David - Frontend Developer
        User david = createUserIfNotExists("david@student.com", "David Brown", User.UserRole.CANDIDATE);
        if (david != null && !candidateRepository.existsById(david.getId())) {
            Candidate candidate = new Candidate();
            candidate.setUser(david);
            candidate.setPhone("+1-555-0104");
            candidate.setLocation("Seattle, WA");
            candidate.setBio("Frontend Developer passionate about React, TypeScript, and UX design");
            candidate.setGithubUrl("https://github.com/david");
            candidate.setLinkedinUrl("https://linkedin.com/in/david");
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", david.getEmail());
        }

        // Emma - DevOps Engineer
        User emma = createUserIfNotExists("emma@student.com", "Emma Davis", User.UserRole.CANDIDATE);
        if (emma != null && !candidateRepository.existsById(emma.getId())) {
            Candidate candidate = new Candidate();
            candidate.setUser(emma);
            candidate.setPhone("+1-555-0105");
            candidate.setLocation("Austin, TX");
            candidate.setBio("DevOps Engineer with 6+ years in AWS, Kubernetes, and CI/CD pipelines");
            candidate.setGithubUrl("https://github.com/emma");
            candidate.setLinkedinUrl("https://linkedin.com/in/emma");
            candidateRepository.save(candidate);
            log.info("Seeded candidate: {}", emma.getEmail());
        }

        log.info("Candidate seeding completed");
    }

    @Transactional
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
            Recruiter recruiter = new Recruiter();
            recruiter.setUser(sarah);  // This sets the ID via @MapsId
            recruiter.setCompany(techCorp);
            recruiter.setPhone("+1-555-1001");
            recruiter.setPosition("Senior Technical Recruiter");
            recruiter.setBio("Specialized in recruiting software engineers for full-stack and backend positions");
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", sarah.getEmail());
        }

        // James - DataViz Analytics
        User james = createUserIfNotExists("james@recruiter.com", "James Miller", User.UserRole.RECRUITER);
        if (james != null && dataViz != null && !recruiterRepository.existsById(james.getId())) {
            Recruiter recruiter = new Recruiter();
            recruiter.setUser(james);
            recruiter.setCompany(dataViz);
            recruiter.setPhone("+1-555-1002");
            recruiter.setPosition("Hiring Manager");
            recruiter.setBio("Looking for talented data scientists and analytics engineers");
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", james.getEmail());
        }

        // Lisa - CloudStack Systems
        User lisa = createUserIfNotExists("lisa@recruiter.com", "Lisa Taylor", User.UserRole.RECRUITER);
        if (lisa != null && cloudStack != null && !recruiterRepository.existsById(lisa.getId())) {
            Recruiter recruiter = new Recruiter();
            recruiter.setUser(lisa);
            recruiter.setCompany(cloudStack);
            recruiter.setPhone("+1-555-1003");
            recruiter.setPosition("DevOps Recruiter");
            recruiter.setBio("Recruiting cloud architects and DevOps engineers for enterprise solutions");
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", lisa.getEmail());
        }

        // Michael - FinTech Innovations
        User michael = createUserIfNotExists("michael@recruiter.com", "Michael Chen", User.UserRole.RECRUITER);
        if (michael != null && fintech != null && !recruiterRepository.existsById(michael.getId())) {
            Recruiter recruiter = new Recruiter();
            recruiter.setUser(michael);
            recruiter.setCompany(fintech);
            recruiter.setPhone("+1-555-1004");
            recruiter.setPosition("Engineering Recruiter");
            recruiter.setBio("Building the team for blockchain and fintech innovation");
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", michael.getEmail());
        }

        // Jennifer - AI Research Labs
        User jennifer = createUserIfNotExists("jennifer@recruiter.com", "Jennifer Wilson", User.UserRole.RECRUITER);
        if (jennifer != null && aiLabs != null && !recruiterRepository.existsById(jennifer.getId())) {
            Recruiter recruiter = new Recruiter();
            recruiter.setUser(jennifer);
            recruiter.setCompany(aiLabs);
            recruiter.setPhone("+1-555-1005");
            recruiter.setPosition("AI/ML Recruiter");
            recruiter.setBio("Recruiting ML engineers and AI researchers for cutting-edge projects");
            recruiterRepository.save(recruiter);
            log.info("Seeded recruiter: {}", jennifer.getEmail());
        }

        log.info("Recruiter seeding completed");
    }

    /**
     * Creates a user if it doesn't already exist.
     * Returns the user entity (either existing or newly created).
     * The returned User is always attached to the current persistence context.
     */
    @Transactional(propagation = org.springframework.transaction.annotation.Propagation.REQUIRED)
    private User createUserIfNotExists(String email, String name, User.UserRole role) {
        // Check if user exists and return it from the database (attached)
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
        
        // Refetch to ensure it's attached to persistence context
        return userRepository.findByEmail(email).orElse(savedUser);
    }
}
