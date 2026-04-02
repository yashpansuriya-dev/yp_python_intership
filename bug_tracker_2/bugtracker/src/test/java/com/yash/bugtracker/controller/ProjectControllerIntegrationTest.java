package com.yash.bugtracker.controller;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.ProjectMembership;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.repository.ProjectMembershipRepository;
import com.yash.bugtracker.repository.ProjectRepository;
import com.yash.bugtracker.repository.UserAccountRepository;
import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class ProjectControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserAccountRepository userAccountRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private ProjectMembershipRepository projectMembershipRepository;

    private UserAccount manager;
    private UserAccount developer;
    private UserAccount tester;

    @BeforeEach
    void setUp() {
        projectMembershipRepository.deleteAll();
        projectRepository.deleteAll();
        userAccountRepository.deleteAll();

        manager = saveUser("manager@test.local", "Manager User", Role.PROJECT_MANAGER);
        developer = saveUser("developer@test.local", "Developer User", Role.DEVELOPER);
        tester = saveUser("tester@test.local", "Tester User", Role.TESTER);
    }

    @Test
    void managerCanOpenNewProjectForm() throws Exception {
        mockMvc.perform(get("/projects/new")
                        .with(user(manager.getEmail()).roles(manager.getRole().name())))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("Create project workspace")));
    }

    @Test
    void testerCannotOpenNewProjectForm() throws Exception {
        mockMvc.perform(get("/projects/new")
                        .with(user(tester.getEmail()).roles(tester.getRole().name())))
                .andExpect(status().isForbidden());
    }

    @Test
    void managerCanCreateProjectSuccessfully() throws Exception {
        mockMvc.perform(post("/projects")
                        .with(user(manager.getEmail()).roles(manager.getRole().name()))
                        .with(csrf())
                        .param("name", "Regression Safe Project")
                        .param("code", "")
                        .param("description", "Project created through integration test.")
                        .param("startDate", LocalDate.now().plusDays(1).toString())
                        .param("targetEndDate", LocalDate.now().plusDays(20).toString())
                        .param("status", "ACTIVE")
                        .param("managerId", manager.getId().toString())
                        .param("memberIds", developer.getId().toString()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/projects"));

        Project savedProject = projectRepository.findAllByOrderByNameAsc().stream()
                .filter(project -> "Regression Safe Project".equals(project.getName()))
                .findFirst()
                .orElseThrow();

        assertThat(savedProject.getManager().getId()).isEqualTo(manager.getId());
        List<Long> memberIds = projectMembershipRepository.findByProjectOrderByUser_FullNameAsc(savedProject).stream()
                .map(ProjectMembership::getUser)
                .map(UserAccount::getId)
                .toList();
        assertThat(memberIds).contains(manager.getId(), developer.getId());
    }

    @Test
    void editProjectFormUsesUpdateEndpoint() throws Exception {
        Project project = saveProject("Editable Project", manager);

        mockMvc.perform(get("/projects/" + project.getId() + "/edit")
                        .with(user(manager.getEmail()).roles(manager.getRole().name())))
                .andExpect(status().isOk())
                .andExpect(content().string(org.hamcrest.Matchers.containsString("action=\"/projects/" + project.getId() + "\"")));
    }

    @Test
    void managerCanUpdateProjectSuccessfully() throws Exception {
        Project project = saveProject("Project Before Edit", manager);

        mockMvc.perform(post("/projects/" + project.getId() + "/edit")
                        .with(user(manager.getEmail()).roles(manager.getRole().name()))
                        .with(csrf())
                        .param("name", "Project After Edit")
                        .param("code", "PAE")
                        .param("description", "Updated through integration test.")
                        .param("startDate", LocalDate.now().plusDays(2).toString())
                        .param("targetEndDate", LocalDate.now().plusDays(30).toString())
                        .param("status", "COMPLETED")
                        .param("managerId", manager.getId().toString())
                        .param("memberIds", developer.getId().toString()))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/projects/" + project.getId()));

        Project updatedProject = projectRepository.findById(project.getId()).orElseThrow();
        assertThat(updatedProject.getName()).isEqualTo("Project After Edit");
        assertThat(updatedProject.getStatus().name()).isEqualTo("COMPLETED");
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

    private Project saveProject(String name, UserAccount projectManager) {
        Project project = new Project();
        project.setName(name);
        project.setCode(name.substring(0, Math.min(3, name.length())).toUpperCase());
        project.setDescription("Saved for controller integration testing.");
        project.setStartDate(LocalDate.now().plusDays(1));
        project.setStatus(com.yash.bugtracker.enums.ProjectStatus.ACTIVE);
        project.setManager(projectManager);
        Project savedProject = projectRepository.save(project);

        ProjectMembership membership = new ProjectMembership();
        membership.setProject(savedProject);
        membership.setUser(projectManager);
        projectMembershipRepository.save(membership);
        return savedProject;
    }
}
