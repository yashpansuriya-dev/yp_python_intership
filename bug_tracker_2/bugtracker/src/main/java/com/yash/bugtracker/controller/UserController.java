package com.yash.bugtracker.controller;

import com.yash.bugtracker.dto.UserForm;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.service.CurrentUserService;
import com.yash.bugtracker.service.ProjectService;
import com.yash.bugtracker.service.UserService;
import jakarta.validation.Valid;
import java.util.Arrays;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final ProjectService projectService;
    private final CurrentUserService currentUserService;

    @GetMapping
    public String listUsers(Model model) {
        model.addAttribute("users", userService.getAllUsers());
        return "users/list";
    }

    @GetMapping("/new")
    public String newUser(Model model) {
        if (!model.containsAttribute("userForm")) {
            UserForm userForm = new UserForm();
            userForm.setActive(true);
            model.addAttribute("userForm", userForm);
        }
        populateFormOptions(model);
        model.addAttribute("formMode", "create");
        model.addAttribute("formAction", "/users");
        return "users/form";
    }

    @PostMapping
    public String createUser(
            @Valid @ModelAttribute("userForm") UserForm userForm,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes
    ) {
        if (bindingResult.hasErrors()) {
            populateFormOptions(model);
            model.addAttribute("formMode", "create");
            model.addAttribute("formAction", "/users");
            return "users/form";
        }

        userService.createUser(userForm);
        redirectAttributes.addFlashAttribute("successMessage", "User created successfully.");
        return "redirect:/users";
    }

    @GetMapping("/{id}/edit")
    public String editUser(@PathVariable Long id, Model model) {
        UserAccount user = userService.getByIdWithProjectMemberships(id);
        if (!model.containsAttribute("userForm")) {
            model.addAttribute("userForm", toForm(user));
        }
        populateFormOptions(model);
        model.addAttribute("managedUser", user);
        model.addAttribute("formMode", "edit");
        model.addAttribute("formAction", "/users/" + id);
        return "users/form";
    }

    @PostMapping({"/{id}", "/{id}/edit"})
    public String updateUser(
            @PathVariable Long id,
            @Valid @ModelAttribute("userForm") UserForm userForm,
            BindingResult bindingResult,
            Model model,
            RedirectAttributes redirectAttributes
    ) {
        UserAccount existingUser = userService.getById(id);
        if (bindingResult.hasErrors()) {
            populateFormOptions(model);
            model.addAttribute("managedUser", existingUser);
            model.addAttribute("formMode", "edit");
            model.addAttribute("formAction", "/users/" + id);
            return "users/form";
        }

        userService.updateUser(id, userForm);
        String successMessage = currentUserService.getCurrentUser().getId().equals(id)
                ? "Your account was updated successfully."
                : "User updated successfully.";
        redirectAttributes.addFlashAttribute("successMessage", successMessage);
        return "redirect:/users";
    }

    private void populateFormOptions(Model model) {
        model.addAttribute("roleOptions", Arrays.stream(Role.values()).collect(Collectors.toList()));
        model.addAttribute("projects", projectService.listAccessibleProjects(currentUserService.getCurrentUser()));
    }

    private UserForm toForm(UserAccount user) {
        UserForm form = new UserForm();
        form.setFullName(user.getFullName());
        form.setEmail(user.getEmail());
        form.setRole(user.getRole());
        form.setActive(user.isActive());
        form.setProjectIds(user.getProjectMemberships().stream()
                .map(membership -> membership.getProject().getId())
                .collect(Collectors.toSet()));
        return form;
    }
}
