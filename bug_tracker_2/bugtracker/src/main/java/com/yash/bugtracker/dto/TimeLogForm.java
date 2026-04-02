package com.yash.bugtracker.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class TimeLogForm {

    @NotNull(message = "Minutes spent is required.")
    @Min(value = 1, message = "Time spent must be at least 1 minute.")
    private Integer minutesSpent;

    @NotNull(message = "Log date is required.")
    private LocalDate logDate;

    @Size(max = 1000, message = "Note must be under 1000 characters.")
    private String note;
}
