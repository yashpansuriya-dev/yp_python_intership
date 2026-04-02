package com.yash.bugtracker.dto;

import com.yash.bugtracker.enums.BugPriority;
import com.yash.bugtracker.enums.BugSeverity;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BugForm {

    @NotNull(message = "Select a project.")
    private Long projectId;

    @NotBlank(message = "Bug title is required.")
    @Size(max = 180, message = "Bug title must be under 180 characters.")
    private String title;

    @NotBlank(message = "Description is required.")
    @Size(max = 4000, message = "Description must be under 4000 characters.")
    private String description;

    @Size(max = 2000, message = "Steps to reproduce must be under 2000 characters.")
    private String stepsToReproduce;

    @Size(max = 2000, message = "Expected result must be under 2000 characters.")
    private String expectedResult;

    @Size(max = 2000, message = "Actual result must be under 2000 characters.")
    private String actualResult;

    @NotNull(message = "Priority is required.")
    private BugPriority priority;

    @NotNull(message = "Severity is required.")
    private BugSeverity severity;
}
