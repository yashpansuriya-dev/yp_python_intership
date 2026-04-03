package com.yash.bugtracker.controller;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.repository.ProjectMembershipRepository;
import com.yash.bugtracker.repository.ProjectRepository;
import com.yash.bugtracker.repository.UserAccountRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserAccountRepository userAccountRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private ProjectMembershipRepository projectMembershipRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @BeforeEach
    void setUp() {
        projectMembershipRepository.deleteAll();
        projectRepository.deleteAll();
        userAccountRepository.deleteAll();
    }

    @Test
    void registerPageIsPubliclyAccessible() throws Exception {
        mockMvc.perform(get("/register"))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Create an account")));
    }

    @Test
    void selfRegistrationCreatesActiveDeveloperAccount() throws Exception {
        mockMvc.perform(post("/register")
                        .with(csrf())
                        .param("fullName", "Fresh Developer")
                        .param("email", "fresh.dev@test.local")
                        .param("password", "Password@123")
                        .param("confirmPassword", "Password@123")
                        .param("role", Role.DEVELOPER.name()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/login"));

        UserAccount savedUser = userAccountRepository.findByEmailIgnoreCase("fresh.dev@test.local").orElseThrow();
        assertThat(savedUser.getRole()).isEqualTo(Role.DEVELOPER);
        assertThat(savedUser.isActive()).isTrue();
        assertThat(passwordEncoder.matches("Password@123", savedUser.getPassword())).isTrue();
    }
}
