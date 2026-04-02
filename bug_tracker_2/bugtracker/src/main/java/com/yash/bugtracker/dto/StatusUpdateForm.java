package com.yash.bugtracker.dto;

import com.yash.bugtracker.enums.BugStatus;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class StatusUpdateForm {

    @NotNull(message = "Select a status.")
    private BugStatus status;

    @Size(max = 500, message = "Note must be under 500 characters.")
    private String note;
}
