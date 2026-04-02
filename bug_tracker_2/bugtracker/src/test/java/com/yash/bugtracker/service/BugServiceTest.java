package com.yash.bugtracker.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.yash.bugtracker.dto.AssignmentForm;
import com.yash.bugtracker.dto.StatusUpdateForm;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.ActivityAction;
import com.yash.bugtracker.enums.BugStatus;
import com.yash.bugtracker.enums.ProjectStatus;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.exception.BusinessException;
import com.yash.bugtracker.repository.BugAttachmentRepository;
import com.yash.bugtracker.repository.BugCommentRepository;
import com.yash.bugtracker.repository.BugTicketRepository;
import com.yash.bugtracker.repository.TimeLogRepository;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class BugServiceTest {

    @Mock
    private BugTicketRepository bugTicketRepository;
    @Mock
    private BugAttachmentRepository bugAttachmentRepository;
    @Mock
    private BugCommentRepository bugCommentRepository;
    @Mock
    private TimeLogRepository timeLogRepository;
    @Mock
    private ProjectService projectService;
    @Mock
    private UserService userService;
    @Mock
    private ActivityService activityService;
    @Mock
    private FileStorageService fileStorageService;

    @InjectMocks
    private BugService bugService;

    @Test
    void assignBugMovesOpenTicketToInProgress() {
        UserAccount manager = user(1L, "Manager", Role.PROJECT_MANAGER);
        UserAccount developer = user(2L, "Developer", Role.DEVELOPER);
        Project project = project(10L, manager);
        BugTicket bug = bug(100L, project, BugStatus.OPEN);
        bug.setTicketId("BTP-00100");

        AssignmentForm form = new AssignmentForm();
        form.setDeveloperId(developer.getId());

        when(bugTicketRepository.findById(bug.getId())).thenReturn(Optional.of(bug));
        when(projectService.isMember(project, manager)).thenReturn(true);
        when(projectService.canManage(project, manager)).thenReturn(true);
        when(userService.getActiveById(developer.getId())).thenReturn(developer);
        when(projectService.isMember(project, developer)).thenReturn(true);

        bugService.assignBug(bug.getId(), form, manager);

        assertEquals(BugStatus.IN_PROGRESS, bug.getStatus());
        assertEquals(developer, bug.getAssignee());
        verify(activityService).log(eq(bug), eq(manager), eq(ActivityAction.ASSIGNED), any(String.class));
    }

    @Test
    void resolveBugRequiresTimeLogging() {
        UserAccount manager = user(1L, "Manager", Role.PROJECT_MANAGER);
        UserAccount developer = user(2L, "Developer", Role.DEVELOPER);
        Project project = project(10L, manager);
        BugTicket bug = bug(100L, project, BugStatus.IN_PROGRESS);
        bug.setAssignee(developer);

        StatusUpdateForm form = new StatusUpdateForm();
        form.setStatus(BugStatus.RESOLVED);

        when(bugTicketRepository.findById(bug.getId())).thenReturn(Optional.of(bug));
        when(projectService.isMember(project, developer)).thenReturn(true);
        when(timeLogRepository.sumMinutesByBug(bug)).thenReturn(0L);

        assertThrows(BusinessException.class, () -> bugService.updateStatus(bug.getId(), form, developer));
    }

    private UserAccount user(Long id, String name, Role role) {
        UserAccount user = new UserAccount();
        user.setId(id);
        user.setFullName(name);
        user.setEmail(name.toLowerCase() + "@example.com");
        user.setRole(role);
        user.setActive(true);
        return user;
    }

    private Project project(Long id, UserAccount manager) {
        Project project = new Project();
        project.setId(id);
        project.setName("BugTrackPro");
        project.setCode("BTP");
        project.setStatus(ProjectStatus.ACTIVE);
        project.setManager(manager);
        return project;
    }

    private BugTicket bug(Long id, Project project, BugStatus status) {
        BugTicket bug = new BugTicket();
        bug.setId(id);
        bug.setProject(project);
        bug.setStatus(status);
        bug.setTitle("Sample bug");
        bug.setDescription("Sample description");
        return bug;
    }
}
