package com.codeforge.config;

import com.codeforge.security.JWTFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * Spring Security configuration
 * Configures JWT authentication, endpoint protection, CORS, session management
 */
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
@RequiredArgsConstructor
public class SecurityConfig {
    
    private final JWTFilter jwtFilter;
    
    /**
     * Password encoder using BCrypt
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    /**
     * Authentication manager for authentication processing
     */
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
    
    /**
     * Main security filter chain configuration
     */
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeRequests(auth -> auth
                // Public endpoints
                .requestMatchers(HttpMethod.POST, "/auth/register/candidate").permitAll()
                .requestMatchers(HttpMethod.POST, "/auth/register/recruiter").permitAll()
                .requestMatchers(HttpMethod.POST, "/auth/login").permitAll()
                .requestMatchers(HttpMethod.GET, "/actuator/health").permitAll()
                
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
        
        return http.build();
    }
}
