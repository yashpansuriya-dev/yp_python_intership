package com.yash.bugtracker.enums;

public enum BugPriority {
    LOW("Low"),
    MEDIUM("Medium"),
    HIGH("High"),
    CRITICAL("Critical");

    private final String label;

    BugPriority(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
