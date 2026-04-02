package com.yash.bugtracker.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AssignmentForm {

    @NotNull(message = "Select a developer.")
    private Long developerId;
}
