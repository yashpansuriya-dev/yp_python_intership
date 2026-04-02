package com.yash.bugtracker.service;

import com.yash.bugtracker.dto.DashboardData;
import com.yash.bugtracker.dto.DeveloperMetrics;
import com.yash.bugtracker.dto.ProjectOverview;
import com.yash.bugtracker.entity.UserAccount;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ReportService {

    private final DashboardService dashboardService;

    public String buildProjectSummaryCsv(UserAccount user) {
        DashboardData dashboardData = dashboardService.getDashboardData(user);
        StringBuilder builder = new StringBuilder();
        builder.append("Project Code,Project Name,Status,Team Size,Total Bugs,Open Bugs,Resolved Bugs\n");
        for (ProjectOverview overview : dashboardData.projectOverviews()) {
            builder.append(csv(overview.code())).append(',')
                    .append(csv(overview.name())).append(',')
                    .append(csv(overview.status().getLabel())).append(',')
                    .append(overview.teamSize()).append(',')
                    .append(overview.totalBugs()).append(',')
                    .append(overview.openBugs()).append(',')
                    .append(overview.resolvedBugs()).append('\n');
        }
        return builder.toString();
    }

    public String buildDeveloperSummaryCsv(UserAccount user) {
        DashboardData dashboardData = dashboardService.getDashboardData(user);
        StringBuilder builder = new StringBuilder();
        builder.append("Developer,Resolved Bugs,Assigned Bugs,Total Minutes\n");
        for (DeveloperMetrics metrics : dashboardData.developerMetrics()) {
            builder.append(csv(metrics.fullName())).append(',')
                    .append(metrics.resolvedCount()).append(',')
                    .append(metrics.assignedCount()).append(',')
                    .append(metrics.totalMinutes()).append('\n');
        }
        return builder.toString();
    }

    private String csv(String value) {
        if (value == null) {
            return "\"\"";
        }
        return "\"" + value.replace("\"", "\"\"") + "\"";
    }
}
