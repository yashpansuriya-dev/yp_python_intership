package com.yash.bugtracker.controller;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
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
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserAccountRepository userAccountRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private ProjectMembershipRepository projectMembershipRepository;

    private UserAccount admin;
    private UserAccount developer;

    @BeforeEach
    void setUp() {
        projectMembershipRepository.deleteAll();
        projectRepository.deleteAll();
        userAccountRepository.deleteAll();

        admin = saveUser("admin@test.local", "Admin User", Role.ADMIN);
        developer = saveUser("developer@test.local", "Developer User", Role.DEVELOPER);
    }

    @Test
    void adminCanOpenEditUserForm() throws Exception {
        mockMvc.perform(get("/users/" + developer.getId() + "/edit")
                        .with(user(admin.getEmail()).roles(admin.getRole().name())))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("action=\"/users/" + developer.getId() + "\"")));
    }

    @Test
    void adminCanUpdateUserThroughEditEndpointCompatibilityRoute() throws Exception {
        mockMvc.perform(post("/users/" + developer.getId() + "/edit")
                        .with(user(admin.getEmail()).roles(admin.getRole().name()))
                        .with(csrf())
                        .param("fullName", "Developer Renamed")
                        .param("email", developer.getEmail())
                        .param("role", Role.DEVELOPER.name())
                        .param("active", "true")
                        .param("password", "")
                        .param("confirmPassword", ""))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/users"));

        UserAccount updatedUser = userAccountRepository.findById(developer.getId()).orElseThrow();
        assertThat(updatedUser.getFullName()).isEqualTo("Developer Renamed");
        assertThat(updatedUser.isActive()).isTrue();
    }

    private UserAccount saveUser(String email, String fullName, Role role) {
        UserAccount user = new UserAccount();
        user.setEmail(email);
        user.setFullName(fullName);
        user.setPassword("encoded-password");
        user.setRole(role);
        user.setActive(true);
        return userAccountRepository.save(user);
    }
}
