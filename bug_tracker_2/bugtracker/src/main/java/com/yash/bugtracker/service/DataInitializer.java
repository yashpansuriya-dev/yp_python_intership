package com.yash.bugtracker.service;

import com.yash.bugtracker.entity.BugComment;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.ProjectMembership;
import com.yash.bugtracker.entity.TimeLog;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.ActivityAction;
import com.yash.bugtracker.enums.BugPriority;
import com.yash.bugtracker.enums.BugSeverity;
import com.yash.bugtracker.enums.BugStatus;
import com.yash.bugtracker.enums.ProjectStatus;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.repository.BugCommentRepository;
import com.yash.bugtracker.repository.BugTicketRepository;
import com.yash.bugtracker.repository.ProjectMembershipRepository;
import com.yash.bugtracker.repository.ProjectRepository;
import com.yash.bugtracker.repository.TimeLogRepository;
import com.yash.bugtracker.repository.UserAccountRepository;
import java.time.LocalDate;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@ConditionalOnProperty(name = "app.seed-demo-data", havingValue = "true", matchIfMissing = true)
public class DataInitializer implements CommandLineRunner {

    private final UserAccountRepository userAccountRepository;
    private final ProjectRepository projectRepository;
    private final ProjectMembershipRepository projectMembershipRepository;
    private final BugTicketRepository bugTicketRepository;
    private final BugCommentRepository bugCommentRepository;
    private final TimeLogRepository timeLogRepository;
    private final PasswordEncoder passwordEncoder;
    private final ActivityService activityService;

    @Override
    public void run(String... args) {
        if (userAccountRepository.count() > 0) {
            return;
        }

        UserAccount admin = createUser("Admin User", "admin@bugtrackpro.local", "Admin@123", Role.ADMIN);
        UserAccount manager = createUser("Priya Manager", "manager@bugtrackpro.local", "Manager@123", Role.PROJECT_MANAGER);
        UserAccount developer = createUser("Rahul Developer", "developer@bugtrackpro.local", "Developer@123", Role.DEVELOPER);
        UserAccount tester = createUser("Ananya Tester", "tester@bugtrackpro.local", "Tester@123", Role.TESTER);

        Project project = new Project();
        project.setCode("BTP");
        project.setName("BugTrackPro");
        project.setDescription("Degree project implementation for bug tracking, task analytics, and collaboration.");
        project.setStartDate(LocalDate.now().minusDays(10));
        project.setTargetEndDate(LocalDate.now().plusDays(45));
        project.setStatus(ProjectStatus.ACTIVE);
        project.setManager(manager);
        project = projectRepository.save(project);

        addMembership(project, manager);
        addMembership(project, developer);
        addMembership(project, tester);

        BugTicket bug = new BugTicket();
        bug.setTicketId("PENDING");
        bug.setProject(project);
        bug.setReporter(tester);
        bug.setAssignee(developer);
        bug.setTitle("Dashboard widgets overlap on smaller screens");
        bug.setDescription("When viewport width is below 1024px, the dashboard summary cards overlap the project table.");
        bug.setStepsToReproduce("1. Login as tester. 2. Open dashboard. 3. Resize window to tablet width.");
        bug.setExpectedResult("Cards should wrap cleanly.");
        bug.setActualResult("Cards overlap and hide labels.");
        bug.setPriority(BugPriority.HIGH);
        bug.setSeverity(BugSeverity.MAJOR);
        bug.setStatus(BugStatus.IN_PROGRESS);
        bug = bugTicketRepository.save(bug);
        bug.setTicketId("BTP-%05d".formatted(bug.getId()));
        bugTicketRepository.save(bug);

        BugComment comment = new BugComment();
        comment.setBug(bug);
        comment.setAuthor(developer);
        comment.setMessage("Investigating the card grid and responsive spacing rules.");
        bugCommentRepository.save(comment);

        TimeLog timeLog = new TimeLog();
        timeLog.setBug(bug);
        timeLog.setUser(developer);
        timeLog.setMinutesSpent(90);
        timeLog.setLogDate(LocalDate.now());
        timeLog.setNote("Checked dashboard CSS and viewport behavior.");
        timeLogRepository.save(timeLog);

        activityService.log(bug, tester, ActivityAction.BUG_CREATED, "Created sample bug for demo data.");
        activityService.log(bug, manager, ActivityAction.ASSIGNED, "Assigned sample bug to Rahul Developer.");
        activityService.log(bug, developer, ActivityAction.TIME_LOGGED, "Logged initial effort against the sample bug.");
        activityService.log(bug, developer, ActivityAction.COMMENT_ADDED, "Added a solution update on the sample bug.");
    }

    private UserAccount createUser(String fullName, String email, String rawPassword, Role role) {
        UserAccount user = new UserAccount();
        user.setFullName(fullName);
        user.setEmail(email);
        user.setPassword(passwordEncoder.encode(rawPassword));
        user.setRole(role);
        user.setActive(true);
        return userAccountRepository.save(user);
    }

    private void addMembership(Project project, UserAccount user) {
        ProjectMembership membership = new ProjectMembership();
        membership.setProject(project);
        membership.setUser(user);
        projectMembershipRepository.save(membership);
    }
}
