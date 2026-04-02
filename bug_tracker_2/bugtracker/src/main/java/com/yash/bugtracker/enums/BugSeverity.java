package com.yash.bugtracker.enums;

public enum BugSeverity {
    MINOR("Minor"),
    MAJOR("Major"),
    CRITICAL("Critical"),
    BLOCKER("Blocker");

    private final String label;

    BugSeverity(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
