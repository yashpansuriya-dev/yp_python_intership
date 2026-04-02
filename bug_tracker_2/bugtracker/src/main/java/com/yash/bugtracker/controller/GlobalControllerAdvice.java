package com.yash.bugtracker.controller;

import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.service.CurrentUserService;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ModelAttribute;

@ControllerAdvice
@RequiredArgsConstructor
public class GlobalControllerAdvice {

    private final CurrentUserService currentUserService;

    @ModelAttribute
    public void addGlobalAttributes(Model model, Authentication authentication, HttpServletRequest request) {
        model.addAttribute("currentUser", null);
        model.addAttribute("isAdmin", false);
        model.addAttribute("isProjectManager", false);
        model.addAttribute("isDeveloper", false);
        model.addAttribute("isTester", false);
        model.addAttribute("requestPath", request.getRequestURI());

        if (authentication == null || !authentication.isAuthenticated()
                || authentication instanceof AnonymousAuthenticationToken) {
            return;
        }

        try {
            UserAccount currentUser = currentUserService.getCurrentUser();
            model.addAttribute("currentUser", currentUser);
            model.addAttribute("isAdmin", currentUser.getRole() == Role.ADMIN);
            model.addAttribute("isProjectManager", currentUser.getRole() == Role.PROJECT_MANAGER);
            model.addAttribute("isDeveloper", currentUser.getRole() == Role.DEVELOPER);
            model.addAttribute("isTester", currentUser.getRole() == Role.TESTER);
        } catch (Exception ignored) {
        }
    }
}
