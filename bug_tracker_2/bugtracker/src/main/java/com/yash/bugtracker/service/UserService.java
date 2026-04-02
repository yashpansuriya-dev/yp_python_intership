package com.yash.bugtracker.service;

import com.yash.bugtracker.dto.RegistrationForm;
import com.yash.bugtracker.dto.UserForm;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.ProjectMembership;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.exception.BusinessException;
import com.yash.bugtracker.exception.NotFoundException;
import com.yash.bugtracker.repository.ProjectMembershipRepository;
import com.yash.bugtracker.repository.ProjectRepository;
import com.yash.bugtracker.repository.UserAccountRepository;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserAccountRepository userAccountRepository;
    private final ProjectRepository projectRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final PasswordEncoder passwordEncoder;

    @Transactional(readOnly = true)
    public List<UserAccount> getAllUsers() {
        return userAccountRepository.findAllByOrderByFullNameAsc();
    }

    @Transactional(readOnly = true)
    public List<UserAccount> getActiveUsers() {
        return userAccountRepository.findAllByActiveTrueOrderByFullNameAsc();
    }

    @Transactional(readOnly = true)
    public List<UserAccount> getActiveDevelopers() {
        return userAccountRepository.findAllByRoleAndActiveTrueOrderByFullNameAsc(Role.DEVELOPER);
    }

    @Transactional(readOnly = true)
    public List<UserAccount> getProjectManagers() {
        return userAccountRepository.findAllByRoleAndActiveTrueOrderByFullNameAsc(Role.PROJECT_MANAGER);
    }

    @Transactional(readOnly = true)
    public UserAccount getById(Long id) {
        return userAccountRepository.findById(id)
                .orElseThrow(() -> new NotFoundException("User not found."));
    }

    @Transactional(readOnly = true)
    public UserAccount getByIdWithProjectMemberships(Long id) {
        return userAccountRepository.findWithProjectMembershipsById(id)
                .orElseThrow(() -> new NotFoundException("User not found."));
    }

    @Transactional(readOnly = true)
    public UserAccount getActiveById(Long id) {
        UserAccount user = getById(id);
        if (!user.isActive()) {
            throw new BusinessException("Selected user is inactive.");
        }
        return user;
    }

    @Transactional
    public UserAccount registerSelf(RegistrationForm form) {
        if (form.getRole() != Role.DEVELOPER && form.getRole() != Role.TESTER) {
            throw new BusinessException("Self-registration is only allowed for Developers and Testers.");
        }
        assertEmailAvailable(form.getEmail(), null);

        UserAccount user = new UserAccount();
        user.setFullName(form.getFullName().trim());
        user.setEmail(form.getEmail().trim().toLowerCase());
        user.setPassword(passwordEncoder.encode(form.getPassword()));
        user.setRole(form.getRole());
        user.setActive(true);
        return userAccountRepository.save(user);
    }

    @Transactional
    public UserAccount createUser(UserForm form) {
        if (!StringUtils.hasText(form.getPassword())) {
            throw new BusinessException("Password is required when creating a user.");
        }
        assertEmailAvailable(form.getEmail(), null);

        UserAccount user = new UserAccount();
        applyForm(user, form, true);
        UserAccount savedUser = userAccountRepository.save(user);
        syncProjectMemberships(savedUser, form.getProjectIds());
        return savedUser;
    }

    @Transactional
    public UserAccount updateUser(Long userId, UserForm form) {
        UserAccount user = getById(userId);
        assertEmailAvailable(form.getEmail(), user.getId());

        if (!user.getManagedProjects().isEmpty()
                && form.getRole() != Role.PROJECT_MANAGER
                && form.getRole() != Role.ADMIN) {
            throw new BusinessException("This user manages projects. Reassign their projects before changing the role.");
        }

        if (!form.isActive() && user.getRole() == Role.ADMIN
                && userAccountRepository.countByRoleAndActiveTrue(Role.ADMIN) <= 1) {
            throw new BusinessException("At least one active admin must remain in the system.");
        }

        applyForm(user, form, false);
        UserAccount savedUser = userAccountRepository.save(user);
        syncProjectMemberships(savedUser, form.getProjectIds());
        return savedUser;
    }

    @Transactional
    public void syncProjectMemberships(UserAccount user, Set<Long> requestedProjectIds) {
        Set<Long> desiredProjectIds = requestedProjectIds == null ? new HashSet<>() : new HashSet<>(requestedProjectIds);
        desiredProjectIds.addAll(projectRepository.findByManager(user).stream()
                .map(Project::getId)
                .collect(Collectors.toSet()));

        List<ProjectMembership> existingMemberships = projectMembershipRepository.findByUser(user);
        Set<Long> existingProjectIds = existingMemberships.stream()
                .map(membership -> membership.getProject().getId())
                .collect(Collectors.toSet());

        for (ProjectMembership membership : existingMemberships) {
            if (!desiredProjectIds.contains(membership.getProject().getId())) {
                projectMembershipRepository.delete(membership);
            }
        }

        if (desiredProjectIds.isEmpty()) {
            return;
        }

        List<Project> desiredProjects = projectRepository.findAllById(desiredProjectIds);
        for (Project project : desiredProjects) {
            if (!existingProjectIds.contains(project.getId())) {
                ProjectMembership membership = new ProjectMembership();
                membership.setProject(project);
                membership.setUser(user);
                projectMembershipRepository.save(membership);
            }
        }
    }

    private void applyForm(UserAccount user, UserForm form, boolean creating) {
        user.setFullName(form.getFullName().trim());
        user.setEmail(form.getEmail().trim().toLowerCase());
        user.setRole(form.getRole());
        user.setActive(form.isActive());

        if (creating || StringUtils.hasText(form.getPassword())) {
            if (!StringUtils.hasText(form.getPassword()) || form.getPassword().length() < 8) {
                throw new BusinessException("Password must be at least 8 characters.");
            }
            user.setPassword(passwordEncoder.encode(form.getPassword()));
        }
    }

    private void assertEmailAvailable(String email, Long currentUserId) {
        userAccountRepository.findByEmailIgnoreCase(email.trim())
                .filter(user -> currentUserId == null || !user.getId().equals(currentUserId))
                .ifPresent(user -> {
                    throw new BusinessException("A user with this email already exists.");
                });
    }
}
