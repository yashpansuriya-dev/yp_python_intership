package com.yash.bugtracker.dto;

public record DashboardSummary(
        long totalBugs,
        long openBugs,
        long inProgressBugs,
        long resolvedBugs,
        long closedBugs,
        long unassignedBugs,
        long activeProjects
) {
}
