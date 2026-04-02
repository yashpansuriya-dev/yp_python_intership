package com.yash.bugtracker.enums;

public enum Role {
    ADMIN("Admin"),
    PROJECT_MANAGER("Project Manager"),
    DEVELOPER("Developer"),
    TESTER("Tester");

    private final String label;

    Role(String label) {
        this.label = label;
    }

    public String getLabel() {
        return label;
    }
}
