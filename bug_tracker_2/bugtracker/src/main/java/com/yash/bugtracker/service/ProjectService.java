package com.yash.bugtracker.service;

import com.yash.bugtracker.dto.ProjectForm;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.ProjectMembership;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.ProjectStatus;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.exception.BusinessException;
import com.yash.bugtracker.exception.NotFoundException;
import com.yash.bugtracker.repository.ProjectMembershipRepository;
import com.yash.bugtracker.repository.ProjectRepository;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

@Service
@RequiredArgsConstructor
public class ProjectService {

    private final ProjectRepository projectRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final UserService userService;

    @Transactional(readOnly = true)
    public List<Project> listAccessibleProjects(UserAccount user) {
        if (user.getRole() == Role.ADMIN) {
            return projectRepository.findAllByOrderByNameAsc();
        }
        return projectMembershipRepository.findByUserOrderByProject_NameAsc(user).stream()
                .map(ProjectMembership::getProject)
                .toList();
    }

    @Transactional(readOnly = true)
    public Project getProject(Long projectId) {
        return projectRepository.findById(projectId)
                .orElseThrow(() -> new NotFoundException("Project not found."));
    }

    @Transactional(readOnly = true)
    public Project getProjectForUser(Long projectId, UserAccount user) {
        Project project = projectRepository.findWithManagerAndMembershipsById(projectId)
                .orElseThrow(() -> new NotFoundException("Project not found."));
        if (!isMember(project, user)) {
            throw new BusinessException("You do not have access to this project.");
        }
        return project;
    }

    @Transactional
    public Project createProject(ProjectForm form, UserAccount actor) {
        if (!canCreateOrEditProject(actor)) {
            throw new BusinessException("Only Admins and Project Managers can create projects.");
        }

        UserAccount manager = requireValidManager(form.getManagerId());
        Project project = new Project();
        applyForm(project, form, manager, null);
        Project savedProject = projectRepository.save(project);
        syncProjectMembers(savedProject, form.getMemberIds());
        return savedProject;
    }

    @Transactional
    public Project updateProject(Long projectId, ProjectForm form, UserAccount actor) {
        Project project = getProject(projectId);
        if (!canManage(project, actor)) {
            throw new BusinessException("You are not allowed to update this project.");
        }

        UserAccount manager = requireValidManager(form.getManagerId());
        applyForm(project, form, manager, project);
        Project savedProject = projectRepository.save(project);
        syncProjectMembers(savedProject, form.getMemberIds());
        return savedProject;
    }

    @Transactional(readOnly = true)
    public boolean isMember(Project project, UserAccount user) {
        return user.getRole() == Role.ADMIN || projectMembershipRepository.existsByProjectAndUser(project, user);
    }

    @Transactional(readOnly = true)
    public boolean canManage(Project project, UserAccount actor) {
        return actor.getRole() == Role.ADMIN
                || (actor.getRole() == Role.PROJECT_MANAGER
                && project.getManager() != null
                && project.getManager().getId().equals(actor.getId()));
    }

    @Transactional(readOnly = true)
    public long countMembers(Project project) {
        return projectMembershipRepository.countByProject(project);
    }

    @Transactional(readOnly = true)
    public List<UserAccount> getProjectMembers(Project project) {
        return projectMembershipRepository.findByProjectOrderByUser_FullNameAsc(project).stream()
                .map(ProjectMembership::getUser)
                .toList();
    }

    @Transactional
    public void syncProjectMembers(Project project, Set<Long> requestedMemberIds) {
        Set<Long> desiredMemberIds = requestedMemberIds == null ? new HashSet<>() : new HashSet<>(requestedMemberIds);
        desiredMemberIds.add(project.getManager().getId());

        List<ProjectMembership> existingMemberships = projectMembershipRepository.findByProjectOrderByUser_FullNameAsc(project);
        Set<Long> existingMemberIds = existingMemberships.stream()
                .map(membership -> membership.getUser().getId())
                .collect(Collectors.toSet());

        for (ProjectMembership membership : existingMemberships) {
            if (!desiredMemberIds.contains(membership.getUser().getId())) {
                projectMembershipRepository.delete(membership);
            }
        }

        List<UserAccount> desiredUsers = userService.getActiveUsers().stream()
                .filter(user -> desiredMemberIds.contains(user.getId()))
                .toList();

        for (UserAccount user : desiredUsers) {
            if (!existingMemberIds.contains(user.getId())) {
                ProjectMembership membership = new ProjectMembership();
                membership.setProject(project);
                membership.setUser(user);
                projectMembershipRepository.save(membership);
            }
        }
    }

    private void applyForm(Project project, ProjectForm form, UserAccount manager, Project existingProject) {
        project.setName(form.getName().trim());
        project.setCode(resolveProjectCode(form.getCode(), form.getName(), existingProject));
        project.setDescription(form.getDescription().trim());
        project.setStartDate(form.getStartDate());
        project.setTargetEndDate(form.getTargetEndDate());
        project.setStatus(form.getStatus() == null ? ProjectStatus.ACTIVE : form.getStatus());
        project.setManager(manager);
    }

    private boolean canCreateOrEditProject(UserAccount actor) {
        return actor.getRole() == Role.ADMIN || actor.getRole() == Role.PROJECT_MANAGER;
    }

    private UserAccount requireValidManager(Long managerId) {
        UserAccount manager = userService.getActiveById(managerId);
        if (manager.getRole() != Role.PROJECT_MANAGER) {
            throw new BusinessException("Project manager must have the Project Manager role.");
        }
        return manager;
    }

    private String resolveProjectCode(String requestedCode, String projectName, Project existingProject) {
        String baseCode = StringUtils.hasText(requestedCode)
                ? requestedCode.trim().toUpperCase().replaceAll("[^A-Z0-9-]", "")
                : generateCodeFromName(projectName);

        if (!StringUtils.hasText(baseCode)) {
            baseCode = "PRJ";
        }

        if (existingProject != null && baseCode.equalsIgnoreCase(existingProject.getCode())) {
            return existingProject.getCode();
        }

        String candidate = baseCode;
        int counter = 1;
        while (projectRepository.existsByCodeIgnoreCase(candidate)) {
            candidate = baseCode + "-" + counter++;
        }
        return candidate;
    }

    private String generateCodeFromName(String projectName) {
        String normalized = projectName == null ? "" : projectName.toUpperCase().replaceAll("[^A-Z0-9 ]", " ");
        String[] parts = normalized.trim().split("\\s+");
        StringBuilder builder = new StringBuilder();
        for (String part : parts) {
            if (!part.isBlank()) {
                builder.append(part.charAt(0));
            }
            if (builder.length() == 4) {
                break;
            }
        }
        return builder.isEmpty() ? "PRJ" : builder.toString();
    }
}
