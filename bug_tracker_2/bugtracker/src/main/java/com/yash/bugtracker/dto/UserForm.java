package com.yash.bugtracker.dto;

import com.yash.bugtracker.enums.Role;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.HashSet;
import java.util.Set;
import lombok.Getter;
import lombok.Setter;
import org.springframework.util.StringUtils;

@Getter
@Setter
public class UserForm {

    @NotBlank(message = "Full name is required.")
    @Size(max = 120, message = "Full name must be under 120 characters.")
    private String fullName;

    @NotBlank(message = "Email is required.")
    @Email(message = "Enter a valid email address.")
    private String email;

    @Size(max = 100, message = "Password must be under 100 characters.")
    private String password;

    private String confirmPassword;

    @NotNull(message = "Role is required.")
    private Role role;

    private boolean active = true;

    private Set<Long> projectIds = new HashSet<>();

    @AssertTrue(message = "Passwords do not match.")
    public boolean isPasswordConfirmed() {
        if (!StringUtils.hasText(password) && !StringUtils.hasText(confirmPassword)) {
            return true;
        }
        return password != null && password.equals(confirmPassword);
    }
}
