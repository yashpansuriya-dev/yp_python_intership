package com.yash.bugtracker.dto;

import com.yash.bugtracker.enums.ProjectStatus;

public record ProjectOverview(
        Long id,
        String code,
        String name,
        ProjectStatus status,
        long teamSize,
        long totalBugs,
        long openBugs,
        long resolvedBugs
) {
}
