package com.yash.bugtracker.dto;

import com.yash.bugtracker.enums.ProjectStatus;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;
import java.util.HashSet;
import java.util.Set;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ProjectForm {

    @NotBlank(message = "Project name is required.")
    @Size(max = 120, message = "Project name must be under 120 characters.")
    private String name;

    @Size(max = 30, message = "Project code must be under 30 characters.")
    private String code;

    @NotBlank(message = "Project description is required.")
    @Size(max = 2000, message = "Description must be under 2000 characters.")
    private String description;

    @NotNull(message = "Start date is required.")
    private LocalDate startDate;

    @FutureOrPresent(message = "Target end date cannot be in the past.")
    private LocalDate targetEndDate;

    @NotNull(message = "Project status is required.")
    private ProjectStatus status = ProjectStatus.ACTIVE;

    @NotNull(message = "Project manager is required.")
    private Long managerId;

    private Set<Long> memberIds = new HashSet<>();

    @AssertTrue(message = "Target end date must be after the start date.")
    public boolean isDateRangeValid() {
        return targetEndDate == null || startDate == null || !targetEndDate.isBefore(startDate);
    }
}
