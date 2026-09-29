package com.codeforge.config;

import com.codeforge.security.JWTFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
<<<<<<< HEAD
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
=======
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
<<<<<<< HEAD
import org.springframework.security.web.authentication.HttpStatusEntryPoint;
=======
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Spring Security configuration
 * Configures JWT authentication, endpoint protection, CORS, session management
 */
@Configuration
@EnableWebSecurity
<<<<<<< HEAD
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JWTFilter jwtFilter;

=======
@EnableGlobalMethodSecurity(prePostEnabled = true)
@RequiredArgsConstructor
public class SecurityConfig {
    
    private final JWTFilter jwtFilter;
    
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
    /**
     * Password encoder using BCrypt
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
<<<<<<< HEAD

=======
    
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
    /**
     * Authentication manager for authentication processing
     */
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
<<<<<<< HEAD

=======
    
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
    /**
     * Main security filter chain configuration
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
<<<<<<< HEAD
            // Uses the CorsConfigurationSource bean from CorsConfig. Without this,
            // browser preflight (OPTIONS) requests from the frontend are rejected.
            .cors(Customizer.withDefaults())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // Unauthenticated requests get 401 (the frontend clears its session on 401).
            .exceptionHandling(ex -> ex.authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)))
            .authorizeHttpRequests(auth -> auth
=======
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeRequests(auth -> auth
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
                // Public endpoints
                .requestMatchers(HttpMethod.POST, "/auth/register/candidate").permitAll()
                .requestMatchers(HttpMethod.POST, "/auth/register/recruiter").permitAll()
                .requestMatchers(HttpMethod.POST, "/auth/login").permitAll()
                .requestMatchers(HttpMethod.GET, "/actuator/health").permitAll()
<<<<<<< HEAD
                .requestMatchers("/error").permitAll()

                // Role-restricted endpoints
                .requestMatchers("/candidates/**").hasRole("CANDIDATE")
                .requestMatchers("/recruiters/**").hasRole("RECRUITER")
                .requestMatchers("/admin/**").hasRole("ADMIN")

                // AI endpoints (any authenticated user) and everything else
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);

=======
                
                // Protected endpoints - CANDIDATE role
                .requestMatchers(HttpMethod.GET, "/candidates/me").hasRole("CANDIDATE")
                .requestMatchers(HttpMethod.PUT, "/candidates/me").hasRole("CANDIDATE")
                
                // Protected endpoints - RECRUITER role
                .requestMatchers(HttpMethod.GET, "/recruiters/me").hasRole("RECRUITER")
                .requestMatchers(HttpMethod.PUT, "/recruiters/me").hasRole("RECRUITER")
                
                // Protected endpoints - ADMIN role
                .requestMatchers(HttpMethod.GET, "/admin/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.PATCH, "/admin/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.POST, "/admin/**").hasRole("ADMIN")
                
                // Protected endpoints - AI endpoints (any authenticated user)
                .requestMatchers(HttpMethod.POST, "/v1/projects/*/ai/**").authenticated()
                .requestMatchers(HttpMethod.GET, "/v1/projects/*/ai/**").authenticated()
                
                // All other requests require authentication
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
        
>>>>>>> 019e83b0908bbf90a27da40578fca8faea6942c8
        return http.build();
    }
}
