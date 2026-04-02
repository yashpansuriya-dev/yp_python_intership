package com.yash.bugtracker.service;

import com.yash.bugtracker.dto.BugSearchCriteria;
import com.yash.bugtracker.dto.DashboardData;
import com.yash.bugtracker.dto.DashboardSummary;
import com.yash.bugtracker.dto.DeveloperMetrics;
import com.yash.bugtracker.dto.ProjectOverview;
import com.yash.bugtracker.entity.ActivityLog;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.BugStatus;
import com.yash.bugtracker.enums.ProjectStatus;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.repository.ActivityLogRepository;
import com.yash.bugtracker.repository.TimeLogRepository;
import java.util.Comparator;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class DashboardService {

    private final ProjectService projectService;
    private final BugService bugService;
    private final ActivityLogRepository activityLogRepository;
    private final TimeLogRepository timeLogRepository;

    @Transactional(readOnly = true)
    public DashboardData getDashboardData(UserAccount user) {
        List<Project> accessibleProjects = projectService.listAccessibleProjects(user);

        BugSearchCriteria criteria = new BugSearchCriteria();
        criteria.setSortBy("updatedDesc");
        List<BugTicket> accessibleBugs = bugService.searchBugs(criteria, user);

        DashboardSummary summary = new DashboardSummary(
                accessibleBugs.size(),
                accessibleBugs.stream().filter(bug -> bug.getStatus() == BugStatus.OPEN).count(),
                accessibleBugs.stream().filter(bug -> bug.getStatus() == BugStatus.IN_PROGRESS || bug.getStatus() == BugStatus.REOPENED).count(),
                accessibleBugs.stream().filter(bug -> bug.getResolvedAt() != null).count(),
                accessibleBugs.stream().filter(bug -> bug.getStatus() == BugStatus.CLOSED).count(),
                accessibleBugs.stream().filter(bug -> bug.getAssignee() == null).count(),
                accessibleProjects.stream().filter(project -> project.getStatus() == ProjectStatus.ACTIVE).count()
        );

        List<ProjectOverview> projectOverviews = accessibleProjects.stream()
                .map(project -> {
                    List<BugTicket> projectBugs = accessibleBugs.stream()
                            .filter(bug -> bug.getProject().getId().equals(project.getId()))
                            .toList();
                    return new ProjectOverview(
                            project.getId(),
                            project.getCode(),
                            project.getName(),
                            project.getStatus(),
                            projectService.countMembers(project),
                            projectBugs.size(),
                            projectBugs.stream().filter(bug -> bug.getStatus() == BugStatus.OPEN).count(),
                            projectBugs.stream().filter(bug -> bug.getResolvedAt() != null).count()
                    );
                })
                .toList();

        Set<UserAccount> developers = new LinkedHashSet<>();
        for (Project project : accessibleProjects) {
            projectService.getProjectMembers(project).stream()
                    .filter(member -> member.getRole() == Role.DEVELOPER)
                    .forEach(developers::add);
        }

        List<DeveloperMetrics> developerMetrics = developers.stream()
                .sorted(Comparator.comparing(UserAccount::getFullName))
                .map(developer -> new DeveloperMetrics(
                        developer.getId(),
                        developer.getFullName(),
                        accessibleBugs.stream()
                                .filter(bug -> bug.getAssignee() != null
                                        && bug.getAssignee().getId().equals(developer.getId())
                                        && bug.getResolvedAt() != null)
                                .count(),
                        accessibleBugs.stream()
                                .filter(bug -> bug.getAssignee() != null
                                        && bug.getAssignee().getId().equals(developer.getId())
                                        && (bug.getStatus() == BugStatus.OPEN
                                        || bug.getStatus() == BugStatus.IN_PROGRESS
                                        || bug.getStatus() == BugStatus.REOPENED))
                                .count(),
                        timeLogRepository.sumMinutesByUser(developer)
                ))
                .toList();

        List<BugTicket> recentBugs = accessibleBugs.stream()
                .sorted(Comparator.comparing(BugTicket::getCreatedAt).reversed())
                .limit(8)
                .toList();

        List<ActivityLog> recentActivities = activityLogRepository.findTop20ByOrderByCreatedAtDesc().stream()
                .filter(activity -> user.getRole() == Role.ADMIN || projectService.isMember(activity.getBug().getProject(), user))
                .limit(10)
                .toList();

        return new DashboardData(summary, projectOverviews, developerMetrics, recentBugs, recentActivities);
    }
}
