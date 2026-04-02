package com.yash.bugtracker.enums;

public enum ActivityAction {
    BUG_CREATED("Bug Created"),
    ASSIGNED("Assigned"),
    STATUS_CHANGED("Status Changed"),
    COMMENT_ADDED("Comment Added"),
    TIME_LOGGED("Time Logged"),
    BUG_ARCHIVED("Bug Archived");

    private final String label;

    ActivityAction(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
