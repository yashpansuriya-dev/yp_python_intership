package com.yash.bugtracker.enums;

public enum ProjectStatus {
    ACTIVE("Active"),
    COMPLETED("Completed"),
    ARCHIVED("Archived");

    private final String label;

    ProjectStatus(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
