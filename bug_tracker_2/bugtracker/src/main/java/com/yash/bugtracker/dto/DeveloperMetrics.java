package com.yash.bugtracker.dto;

public record DeveloperMetrics(
        Long id,
        String fullName,
        long resolvedCount,
        long assignedCount,
        long totalMinutes
) {
}
