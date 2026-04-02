package com.yash.bugtracker.enums;

public enum BugStatus {
    OPEN("Open"),
    IN_PROGRESS("In Progress"),
    RESOLVED("Resolved"),
    REOPENED("Reopened"),
    CLOSED("Closed");

    private final String label;

    BugStatus(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
