package com.codeforge.config;

import com.codeforge.entity.User;
import com.codeforge.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

/**
 * Creates the initial platform admin from the app.admin.* properties
 * (ADMIN_EMAIL / ADMIN_PASSWORD / ADMIN_NAME) on first startup.
 *
 * Without this there is no way to obtain an ADMIN account, since public
 * registration only creates candidates and recruiters.
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class AdminBootstrap implements ApplicationRunner {

    private final AppProperties appProperties;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(ApplicationArguments args) {
        AppProperties.Admin admin = appProperties.getAdmin();

        if (admin.getEmail() == null || admin.getEmail().isBlank()
                || admin.getPassword() == null || admin.getPassword().isBlank()) {
            log.warn("Admin bootstrap skipped: ADMIN_EMAIL / ADMIN_PASSWORD are not configured");
            return;
        }

        if (userRepository.existsByEmail(admin.getEmail())) {
            log.info("Admin bootstrap: account {} already exists", admin.getEmail());
            return;
        }

        User user = User.builder()
            .name(admin.getName() != null && !admin.getName().isBlank() ? admin.getName() : "Platform Admin")
            .email(admin.getEmail())
            .passwordHash(passwordEncoder.encode(admin.getPassword()))
            .role(User.UserRole.ADMIN)
            .enabled(true)
            .build();
        userRepository.save(user);
        log.info("Admin bootstrap: created admin account {}", admin.getEmail());
    }
}
