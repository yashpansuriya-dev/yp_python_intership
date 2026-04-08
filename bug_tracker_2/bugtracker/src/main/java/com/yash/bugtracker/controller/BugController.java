package com.yash.bugtracker.controller;

import com.yash.bugtracker.dto.AssignmentForm;
import com.yash.bugtracker.dto.BugForm;
import com.yash.bugtracker.dto.BugSearchCriteria;
import com.yash.bugtracker.dto.CommentForm;
import com.yash.bugtracker.dto.StatusUpdateForm;
import com.yash.bugtracker.dto.TimeLogForm;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.BugPriority;
import com.yash.bugtracker.enums.BugSeverity;
import com.yash.bugtracker.enums.BugStatus;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.repository.ActivityLogRepository;
import com.yash.bugtracker.service.BugService;
import com.yash.bugtracker.service.CurrentUserService;
import com.yash.bugtracker.service.ProjectService;
import com.yash.bugtracker.service.UserService;
import jakarta.validation.Valid;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/bugs")
@RequiredArgsConstructor
public class BugController {

    private final BugService bugService;
    private final ProjectService projectService;
    private final UserService userService;
    private final CurrentUserService currentUserService;
    private final ActivityLogRepository activityLogRepository;

    // it lists all bugs 
    @GetMapping
    public String listBugs(@ModelAttribute("criteria") BugSearchCriteria criteria, Model model) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        model.addAttribute("bugs", bugService.searchBugs(criteria, currentUser));
        model.addAttribute("projects", projectService.listAccessibleProjects(currentUser));
        model.addAttribute("developers", userService.getActiveDevelopers());
        model.addAttribute("statusOptions", Arrays.asList(BugStatus.values()));
        model.addAttribute("priorityOptions", Arrays.asList(BugPriority.values()));
        model.addAttribute("severityOptions", Arrays.asList(BugSeverity.values()));
        return "bugs/list";
    }

    // creating new bug -> sends empty form object to form.html and it fills it 
    @GetMapping("/new")
    public String newBug(Model model) {
        if (!model.containsAttribute("bugForm")) {
            model.addAttribute("bugForm", new BugForm());
        }
        populateBugFormOptions(model);
        return "bugs/form";
    }

    // validates form data and sent it to service
    @PostMapping
    public String createBug(
            @Valid @ModelAttribute("bugForm") BugForm bugForm,
            BindingResult bindingResult,
            @RequestParam(name = "files", required = false) MultipartFile[] files,
            Model model,
            RedirectAttributes redirectAttributes
    ) {
        if (bindingResult.hasErrors()) {
            populateBugFormOptions(model);
            return "bugs/form";
        }

        BugTicket createdBug = bugService.createBug(bugForm, files, currentUserService.getCurrentUser());
        redirectAttributes.addFlashAttribute("successMessage", "Bug created with ticket ID " + createdBug.getTicketId() + ".");
        return "redirect:/bugs/" + createdBug.getId();
    }

    // detailed info of bug
    @GetMapping("/{id}")
    public String bugDetail(@PathVariable Long id, Model model) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        BugTicket bug = bugService.getBugForUser(id, currentUser);
        Project project = bug.getProject();

        if (!model.containsAttribute("assignmentForm")) {
            model.addAttribute("assignmentForm", new AssignmentForm());
        }
        if (!model.containsAttribute("statusUpdateForm")) {
            model.addAttribute("statusUpdateForm", new StatusUpdateForm());
        }
        if (!model.containsAttribute("commentForm")) {
            model.addAttribute("commentForm", new CommentForm());
        }
        if (!model.containsAttribute("timeLogForm")) {
            TimeLogForm timeLogForm = new TimeLogForm();
            timeLogForm.setLogDate(LocalDate.now());
            model.addAttribute("timeLogForm", timeLogForm);
        }

        boolean canManage = projectService.canManage(project, currentUser);
        boolean isAssignee = bug.getAssignee() != null && bug.getAssignee().getId().equals(currentUser.getId());
        boolean canVerify = currentUser.getRole() == Role.TESTER || canManage;

        model.addAttribute("bug", bug);
        model.addAttribute("attachments", bugService.getAttachments(bug));
        model.addAttribute("comments", bugService.getComments(bug));
        model.addAttribute("timeLogs", bugService.getTimeLogs(bug));
        model.addAttribute("activities", activityLogRepository.findByBugOrderByCreatedAtDesc(bug));
        model.addAttribute("totalMinutes", bugService.getTotalMinutes(bug));
        model.addAttribute("assignableDevelopers", bugService.getAssignableDevelopers(project));
        model.addAttribute("canAssign", currentUser.getRole() == Role.PROJECT_MANAGER && canManage && bug.getStatus() == BugStatus.OPEN);
        model.addAttribute("canArchive", canManage);
        model.addAttribute("isAssignee", isAssignee);
        model.addAttribute("canVerify", canVerify);
        model.addAttribute("availableStatuses", determineAvailableStatuses(bug, currentUser, canManage, isAssignee, canVerify));
        return "bugs/detail";
    }

    @PostMapping("/{id}/assign")
    public String assignBug(
            @PathVariable Long id,
            @Valid @ModelAttribute("assignmentForm") AssignmentForm assignmentForm,
            BindingResult bindingResult,
            RedirectAttributes redirectAttributes
    ) {
        if (bindingResult.hasErrors()) {
            redirectAttributes.addFlashAttribute("errorMessage", "Select a developer before assigning the bug.");
            return "redirect:/bugs/" + id;
        }

        bugService.assignBug(id, assignmentForm, currentUserService.getCurrentUser());
        redirectAttributes.addFlashAttribute("successMessage", "Bug assigned successfully.");
        return "redirect:/bugs/" + id;
    }

    @PostMapping("/{id}/status")
    public String updateStatus(
            @PathVariable Long id,
            @Valid @ModelAttribute("statusUpdateForm") StatusUpdateForm statusUpdateForm,
            BindingResult bindingResult,
            RedirectAttributes redirectAttributes
    ) {
        if (bindingResult.hasErrors()) {
            redirectAttributes.addFlashAttribute("errorMessage", "Choose a valid status before saving.");
            return "redirect:/bugs/" + id;
        }

        bugService.updateStatus(id, statusUpdateForm, currentUserService.getCurrentUser());
        redirectAttributes.addFlashAttribute("successMessage", "Bug status updated successfully.");
        return "redirect:/bugs/" + id;
    }

    @PostMapping("/{id}/comments")
    public String addComment(
            @PathVariable Long id,
            @Valid @ModelAttribute("commentForm") CommentForm commentForm,
            BindingResult bindingResult,
            RedirectAttributes redirectAttributes
    ) {
        if (bindingResult.hasErrors()) {
            redirectAttributes.addFlashAttribute("errorMessage", "Comment cannot be empty.");
            return "redirect:/bugs/" + id;
        }

        bugService.addComment(id, commentForm, currentUserService.getCurrentUser());
        redirectAttributes.addFlashAttribute("successMessage", "Comment added successfully.");
        return "redirect:/bugs/" + id;
    }

    @PostMapping("/{id}/time-logs")
    public String addTimeLog(
            @PathVariable Long id,
            @Valid @ModelAttribute("timeLogForm") TimeLogForm timeLogForm,
            BindingResult bindingResult,
            RedirectAttributes redirectAttributes
    ) {
        if (bindingResult.hasErrors()) {
            redirectAttributes.addFlashAttribute("errorMessage", "Enter valid time log details.");
            return "redirect:/bugs/" + id;
        }

        bugService.addTimeLog(id, timeLogForm, currentUserService.getCurrentUser());
        redirectAttributes.addFlashAttribute("successMessage", "Time logged successfully.");
        return "redirect:/bugs/" + id;
    }

    @PostMapping("/{id}/archive")
    public String archiveBug(@PathVariable Long id, RedirectAttributes redirectAttributes) {
        bugService.archiveBug(id, currentUserService.getCurrentUser());
        redirectAttributes.addFlashAttribute("successMessage", "Bug archived successfully.");
        return "redirect:/bugs";
    }

    private void populateBugFormOptions(Model model) {
        UserAccount currentUser = currentUserService.getCurrentUser();
        model.addAttribute("projects", projectService.listAccessibleProjects(currentUser));
        model.addAttribute("priorityOptions", Arrays.asList(BugPriority.values()));
        model.addAttribute("severityOptions", Arrays.asList(BugSeverity.values()));
    }

    private List<BugStatus> determineAvailableStatuses(
            BugTicket bug,
            UserAccount currentUser,
            boolean canManage,
            boolean isAssignee,
            boolean canVerify
    ) {
        List<BugStatus> statuses = new ArrayList<>();
        if (bug.getStatus() == BugStatus.REOPENED && (isAssignee || canManage)) {
            statuses.add(BugStatus.IN_PROGRESS);
        }
        if ((bug.getStatus() == BugStatus.IN_PROGRESS || bug.getStatus() == BugStatus.REOPENED)
                && currentUser.getRole() == Role.DEVELOPER && isAssignee) {
            statuses.add(BugStatus.RESOLVED);
        }
        if ((bug.getStatus() == BugStatus.RESOLVED || bug.getStatus() == BugStatus.CLOSED) && canVerify) {
            statuses.add(BugStatus.REOPENED);
        }
        if (bug.getStatus() == BugStatus.RESOLVED && canVerify) {
            statuses.add(BugStatus.CLOSED);
        }
        return statuses;
    }
}
