package com.yash.bugtracker.controller;

import com.yash.bugtracker.service.CurrentUserService;
import com.yash.bugtracker.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@RequiredArgsConstructor
public class DashboardController {

    private final CurrentUserService currentUserService;
    private final DashboardService dashboardService;

    @GetMapping({"/", "/dashboard"})
    public String dashboard(Model model) {
        model.addAttribute("dashboardData", dashboardService.getDashboardData(currentUserService.getCurrentUser()));
        return "dashboard";
    }
}
