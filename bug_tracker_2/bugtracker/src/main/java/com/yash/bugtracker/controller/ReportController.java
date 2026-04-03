package com.yash.bugtracker.controller;

import com.yash.bugtracker.service.CurrentUserService;
import com.yash.bugtracker.service.DashboardService;
import com.yash.bugtracker.service.ReportService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
@RequiredArgsConstructor
public class ReportController {

    private final DashboardService dashboardService;
    private final ReportService reportService;
    private final CurrentUserService currentUserService;

    @GetMapping("/reports")
    public String reports(Model model) {
        model.addAttribute("dashboardData", dashboardService.getDashboardData(currentUserService.getCurrentUser()));
        return "reports/index";
    }

    @GetMapping("/reports/projects.csv")
    public ResponseEntity<String> projectSummaryReport() {
        String csv = reportService.buildProjectSummaryCsv(currentUserService.getCurrentUser());
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"project-summary.csv\"")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(csv);
    }

    @GetMapping("/reports/developers.csv")
    public ResponseEntity<String> developerSummaryReport() {
        String csv = reportService.buildDeveloperSummaryCsv(currentUserService.getCurrentUser());
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=\"developer-summary.csv\"")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(csv);
    }
}
