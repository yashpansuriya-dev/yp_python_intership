package com.yash.bugtracker.dto;

import com.yash.bugtracker.entity.ActivityLog;
import com.yash.bugtracker.entity.BugTicket;
import java.util.List;

public record DashboardData(
        DashboardSummary summary,
        List<ProjectOverview> projectOverviews,
        List<DeveloperMetrics> developerMetrics,
        List<BugTicket> recentBugs,
        List<ActivityLog> recentActivities
) {
}
