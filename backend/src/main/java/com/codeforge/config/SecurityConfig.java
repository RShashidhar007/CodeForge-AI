package com.codeforge.config;

import com.codeforge.security.JWTFilter;
import com.codeforge.security.JWTProvider;
import com.codeforge.security.RateLimitingFilter;
import com.codeforge.security.UserDetailsServiceImpl;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfigurationSource;

/**
 * Spring Security configuration
 * Configures JWT authentication, endpoint protection, CORS, session management
 */
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final JWTProvider jwtProvider;
    private final UserDetailsServiceImpl userDetailsService;
    private final CorsConfigurationSource corsConfigurationSource;

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
        // Create filter instances directly
        RateLimitingFilter rateLimitingFilter = new RateLimitingFilter();
        JWTFilter jwtFilter = new JWTFilter(jwtProvider, userDetailsService);
        
        http
            .cors(cors -> cors.configurationSource(corsConfigurationSource))
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                // Public endpoints
                .requestMatchers(HttpMethod.POST, "/auth/register/candidate").permitAll()
                .requestMatchers(HttpMethod.POST, "/auth/register/recruiter").permitAll()
                .requestMatchers(HttpMethod.POST, "/auth/login").permitAll()
                .requestMatchers(HttpMethod.POST, "/github/oauth/callback").permitAll()
                .requestMatchers(HttpMethod.GET, "/github/oauth/authorize").permitAll()
                .requestMatchers(HttpMethod.GET, "/actuator/health").permitAll()
                .requestMatchers("/error").permitAll()

                // Role-restricted endpoints
                .requestMatchers("/candidates/**").hasRole("CANDIDATE")
                .requestMatchers("/recruiters/**").hasRole("RECRUITER")
                .requestMatchers("/admin/**").hasRole("ADMIN")

                // AI endpoints (any authenticated user) and everything else
                .anyRequest().authenticated()
            )
            // Add filters before UsernamePasswordAuthenticationFilter
            // Both filters are independent and run before authentication
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
            .addFilterBefore(rateLimitingFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
