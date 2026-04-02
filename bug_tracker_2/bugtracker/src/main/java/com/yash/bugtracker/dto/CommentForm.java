package com.yash.bugtracker.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CommentForm {

    @NotBlank(message = "Comment message is required.")
    @Size(max = 2000, message = "Comment must be under 2000 characters.")
    private String message;
}
