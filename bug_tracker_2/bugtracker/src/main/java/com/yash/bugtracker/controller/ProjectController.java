package com.yash.bugtracker.controller;

import com.yash.bugtracker.dto.BugSearchCriteria;
import com.yash.bugtracker.dto.ProjectForm;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.ProjectStatus;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.exception.BusinessException;
import com.yash.bugtracker.service.BugService;
import com.yash.bugtracker.service.CurrentUserService;
import com.yash.bugtracker.service.ProjectService;
import com.yash.bugtracker.service.UserService;
import jakarta.validation.Valid;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import org.springframework.security.access.prepost.PreAuthorize;

@Controller
@RequestMapping("/projects")
@RequiredArgsConstructor
public class ProjectController {

    private final ProjectService projectService;
    private final UserService userService;
    private final BugService bugService;
    private final CurrentUserService currentUserService;

    @GetMapping
    public String listProjects(Model model) {
        model.addAttribute("projects", projectService.listAccessibleProjects(currentUserService.getCurrentUser()));
        return "projects/list";
    }

    @PreAuthorize("hasAnyRole('ADMIN','PROJECT_MANAGER')")
    @GetMapping("/new")
    public String newProject(Model model) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        if (!model.containsAttribute("projectForm")) {
            ProjectForm projectForm = new ProjectForm();
            projectForm.setStatus(ProjectStatus.ACTIVE);
            if (currentUser.getRole() == Role.PROJECT_MANAGER) {
                projectForm.setManagerId(currentUser.getId());
            }
            model.addAttribute("projectForm", projectForm);
        }
        populateFormOptions(model, currentUser);
        model.addAttribute("formMode", "create");
        model.addAttribute("formAction", "/projects");
        return "projects/form";
    }

    @PreAuthorize("hasAnyRole('ADMIN','PROJECT_MANAGER')")
    @PostMapping
    public String createProject(
            @Valid @ModelAttribute("projectForm") ProjectForm projectForm,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes
    ) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        if (bindingResult.hasErrors()) {
            populateFormOptions(model, currentUser);
            model.addAttribute("formMode", "create");
            model.addAttribute("formAction", "/projects");
            return "projects/form";
        }

        projectService.createProject(projectForm, currentUser);
        redirectAttributes.addFlashAttribute("successMessage", "Project created successfully.");
        return "redirect:/projects";
    }

    @GetMapping("/{id}")
    public String projectDetail(@PathVariable Long id, Model model) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        Project project = projectService.getProjectForUser(id, currentUser);

        BugSearchCriteria criteria = new BugSearchCriteria();
        criteria.setProjectId(project.getId());

        model.addAttribute("project", project);
        model.addAttribute("projectMembers", projectService.getProjectMembers(project));
        model.addAttribute("projectBugs", bugService.searchBugs(criteria, currentUser));
        model.addAttribute("canManageProject", projectService.canManage(project, currentUser));
        return "projects/detail";
    }

    @PreAuthorize("hasAnyRole('ADMIN','PROJECT_MANAGER')")
    @GetMapping("/{id}/edit")
    public String editProject(@PathVariable Long id, Model model) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        Project project = requireManageableProject(id, currentUser);
        if (!model.containsAttribute("projectForm")) {
            model.addAttribute("projectForm", toForm(project));
        }
        populateFormOptions(model, currentUser);
        model.addAttribute("project", project);
        model.addAttribute("formMode", "edit");
        model.addAttribute("formAction", "/projects/" + id);
        return "projects/form";
    }

    @PreAuthorize("hasAnyRole('ADMIN','PROJECT_MANAGER')")
    @PostMapping({"/{id}", "/{id}/edit"})
    public String updateProject(
            @PathVariable Long id,
            @Valid @ModelAttribute("projectForm") ProjectForm projectForm,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes
    ) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        Project existingProject = requireManageableProject(id, currentUser);
        if (bindingResult.hasErrors()) {
            populateFormOptions(model, currentUser);
            model.addAttribute("project", existingProject);
            model.addAttribute("formMode", "edit");
            model.addAttribute("formAction", "/projects/" + id);
            return "projects/form";
        }

        projectService.updateProject(id, projectForm, currentUser);
        redirectAttributes.addFlashAttribute("successMessage", "Project updated successfully.");
        return "redirect:/projects/" + id;
    }

    private void populateFormOptions(Model model, UserAccount currentUser) {
        model.addAttribute("statusOptions", Arrays.stream(ProjectStatus.values()).collect(Collectors.toList()));
        List<UserAccount> managerOptions = currentUser.getRole() == Role.ADMIN
                ? userService.getProjectManagers()
                : List.of(currentUser);
        model.addAttribute("managerOptions", managerOptions);
        model.addAttribute("memberOptions", userService.getActiveUsers());
    }

    private Project requireManageableProject(Long id, UserAccount currentUser) {
        Project project = projectService.getProjectForUser(id, currentUser);
        if (!projectService.canManage(project, currentUser)) {
            throw new BusinessException("You are not allowed to manage this project.");
        }
        return project;
    }

    private ProjectForm toForm(Project project) {
        ProjectForm form = new ProjectForm();
        form.setName(project.getName());
        form.setCode(project.getCode());
        form.setDescription(project.getDescription());
        form.setStartDate(project.getStartDate());
        form.setTargetEndDate(project.getTargetEndDate());
        form.setStatus(project.getStatus());
        form.setManagerId(project.getManager().getId());
        form.setMemberIds(project.getMemberships().stream()
                .map(membership -> membership.getUser().getId())
                .collect(Collectors.toSet()));
        return form;
    }
}
