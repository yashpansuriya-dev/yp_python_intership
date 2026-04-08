package com.yash.bugtracker.service;

import com.yash.bugtracker.dto.AssignmentForm;
import com.yash.bugtracker.dto.BugForm;
import com.yash.bugtracker.dto.BugSearchCriteria;
import com.yash.bugtracker.dto.CommentForm;
import com.yash.bugtracker.dto.StatusUpdateForm;
import com.yash.bugtracker.dto.TimeLogForm;
import com.yash.bugtracker.entity.BugAttachment;
import com.yash.bugtracker.entity.BugComment;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.TimeLog;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.ActivityAction;
import com.yash.bugtracker.enums.BugStatus;
import com.yash.bugtracker.enums.Role;
import com.yash.bugtracker.exception.BusinessException;
import com.yash.bugtracker.exception.NotFoundException;
import com.yash.bugtracker.repository.BugAttachmentRepository;
import com.yash.bugtracker.repository.BugCommentRepository;
import com.yash.bugtracker.repository.BugTicketRepository;
import com.yash.bugtracker.repository.TimeLogRepository;
import com.yash.bugtracker.repository.specification.BugTicketSpecifications;
import java.time.LocalDateTime;
import java.util.List;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

@Service
@RequiredArgsConstructor
public class BugService {

    private final BugTicketRepository bugTicketRepository;
    private final BugAttachmentRepository bugAttachmentRepository;
    private final BugCommentRepository bugCommentRepository;
    private final TimeLogRepository timeLogRepository;
    private final ProjectService projectService;
    private final UserService userService;
    private final ActivityService activityService;
    private final FileStorageService fileStorageService;

    // search bugs based on filters
    @Transactional(readOnly = true)
    public List<BugTicket> searchBugs(BugSearchCriteria criteria, UserAccount user) {
        Specification<BugTicket> specification = Specification
                .where(BugTicketSpecifications.notArchived())
                .and(BugTicketSpecifications.accessibleTo(user))
                .and(BugTicketSpecifications.matches(criteria, user));

        return bugTicketRepository.findAll(specification, resolveSort(criteria.getSortBy()));
    }

    // create bugs
    @Transactional
    public BugTicket createBug(BugForm form, MultipartFile[] attachments, UserAccount reporter) {
        Project project = projectService.getProjectForUser(form.getProjectId(), reporter);
        
        BugTicket bug = new BugTicket();
        bug.setTicketId("PENDING");
        bug.setProject(project);
        bug.setReporter(reporter);
        bug.setTitle(form.getTitle().trim());
        bug.setDescription(form.getDescription().trim());
        bug.setStepsToReproduce(form.getStepsToReproduce());
        bug.setExpectedResult(form.getExpectedResult());
        bug.setActualResult(form.getActualResult());
        bug.setPriority(form.getPriority());
        bug.setSeverity(form.getSeverity());
        bug.setStatus(BugStatus.OPEN);

        BugTicket savedBug = bugTicketRepository.save(bug);
        savedBug.setTicketId("BTP-%05d".formatted(savedBug.getId()));
        savedBug = bugTicketRepository.save(savedBug);

        List<BugAttachment> storedAttachments = fileStorageService.storeAttachments(savedBug, reporter, attachments);
        bugAttachmentRepository.saveAll(storedAttachments);

        activityService.log(savedBug, reporter, ActivityAction.BUG_CREATED,
                "Created bug " + savedBug.getTicketId() + " for project " + project.getName() + ".");
        return savedBug;
    }

    @Transactional(readOnly = true)
    public BugTicket getBugForUser(Long bugId, UserAccount user) {
        BugTicket bug = bugTicketRepository.findById(bugId)
                .orElseThrow(() -> new NotFoundException("Bug not found."));
        if (bug.isArchived()) {
            throw new BusinessException("This bug has been archived.");
        }
        if (!projectService.isMember(bug.getProject(), user)) {
            throw new BusinessException("You do not have access to this bug.");
        }
        return bug;
    }

    @Transactional
    public void assignBug(Long bugId, AssignmentForm form, UserAccount actor) {
        BugTicket bug = getBugForUser(bugId, actor);
        if (actor.getRole() != Role.PROJECT_MANAGER || !projectService.canManage(bug.getProject(), actor)) {
            throw new BusinessException("Only the assigned Project Manager can assign bugs.");
        }
        if (bug.getStatus() != BugStatus.OPEN) {
            throw new BusinessException("Only bugs in Open state can be assigned.");
        }

        UserAccount developer = userService.getActiveById(form.getDeveloperId());
        if (developer.getRole() != Role.DEVELOPER) {
            throw new BusinessException("Bugs can only be assigned to Developers.");
        }
        if (!projectService.isMember(bug.getProject(), developer)) {
            throw new BusinessException("Selected developer is not part of this project.");
        }

        bug.setAssignee(developer);
        bug.setStatus(BugStatus.IN_PROGRESS);
        bugTicketRepository.save(bug);

        activityService.log(bug, actor, ActivityAction.ASSIGNED,
                "Assigned " + bug.getTicketId() + " to " + developer.getFullName() + ".");
    }

    @Transactional
    public void updateStatus(Long bugId, StatusUpdateForm form, UserAccount actor) {
        BugTicket bug = getBugForUser(bugId, actor);
        BugStatus currentStatus = bug.getStatus();
        BugStatus targetStatus = form.getStatus();

        if (targetStatus == currentStatus) {
            throw new BusinessException("The bug is already in " + currentStatus.getLabel() + " state.");
        }

        switch (targetStatus) {
            case IN_PROGRESS -> moveToInProgress(bug, actor);
            case RESOLVED -> resolveBug(bug, actor);
            case REOPENED -> reopenBug(bug, actor);
            case CLOSED -> closeBug(bug, actor);
            case OPEN -> throw new BusinessException("Bugs cannot be moved back to Open manually.");
        }

        bugTicketRepository.save(bug);
        String note = form.getNote() == null || form.getNote().isBlank() ? "" : " Note: " + form.getNote().trim();
        activityService.log(bug, actor, ActivityAction.STATUS_CHANGED,
                "Changed status of " + bug.getTicketId() + " from " + currentStatus.getLabel()
                        + " to " + targetStatus.getLabel() + "." + note);
    }

    @Transactional
    public void addComment(Long bugId, CommentForm form, UserAccount actor) {
        BugTicket bug = getBugForUser(bugId, actor);

        BugComment comment = new BugComment();
        comment.setBug(bug);
        comment.setAuthor(actor);
        comment.setMessage(form.getMessage().trim());
        bugCommentRepository.save(comment);

        activityService.log(bug, actor, ActivityAction.COMMENT_ADDED,
                "Added a collaboration note on " + bug.getTicketId() + ".");
    }

    @Transactional
    public void addTimeLog(Long bugId, TimeLogForm form, UserAccount actor) {
        BugTicket bug = getBugForUser(bugId, actor);
        if (actor.getRole() != Role.DEVELOPER || bug.getAssignee() == null
                || !bug.getAssignee().getId().equals(actor.getId())) {
            throw new BusinessException("Only the assigned developer can log time for this bug.");
        }

        TimeLog timeLog = new TimeLog();
        timeLog.setBug(bug);
        timeLog.setUser(actor);
        timeLog.setMinutesSpent(form.getMinutesSpent());
        timeLog.setLogDate(form.getLogDate());
        timeLog.setNote(form.getNote());
        timeLogRepository.save(timeLog);

        activityService.log(bug, actor, ActivityAction.TIME_LOGGED,
                "Logged " + form.getMinutesSpent() + " minutes on " + bug.getTicketId() + ".");
    }

    @Transactional
    public void archiveBug(Long bugId, UserAccount actor) {
        BugTicket bug = getBugForUser(bugId, actor);
        if (!projectService.canManage(bug.getProject(), actor)) {
            throw new BusinessException("Only Admins and Project Managers can archive bugs.");
        }

        bug.setArchived(true);
        bugTicketRepository.save(bug);
        activityService.log(bug, actor, ActivityAction.BUG_ARCHIVED,
                "Archived bug " + bug.getTicketId() + " instead of permanent deletion.");
    }

    @Transactional(readOnly = true)
    public List<BugAttachment> getAttachments(BugTicket bug) {
        return bugAttachmentRepository.findByBugOrderByCreatedAtAsc(bug);
    }

    @Transactional(readOnly = true)
    public List<BugComment> getComments(BugTicket bug) {
        return bugCommentRepository.findByBugOrderByCreatedAtAsc(bug);
    }

    @Transactional(readOnly = true)
    public List<TimeLog> getTimeLogs(BugTicket bug) {
        return timeLogRepository.findByBugOrderByCreatedAtDesc(bug);
    }

    @Transactional(readOnly = true)
    public long getTotalMinutes(BugTicket bug) {
        return timeLogRepository.sumMinutesByBug(bug);
    }

    @Transactional(readOnly = true)
    public BugAttachment getAttachmentForUser(Long attachmentId, UserAccount user) {
        BugAttachment attachment = bugAttachmentRepository.findById(attachmentId)
                .orElseThrow(() -> new NotFoundException("Attachment not found."));
        getBugForUser(attachment.getBug().getId(), user);
        return attachment;
    }

    @Transactional(readOnly = true)
    public List<UserAccount> getAssignableDevelopers(Project project) {
        return projectService.getProjectMembers(project).stream()
                .filter(member -> member.isActive() && member.getRole() == Role.DEVELOPER)
                .toList();
    }

    private void moveToInProgress(BugTicket bug, UserAccount actor) {
        if (bug.getStatus() != BugStatus.REOPENED) {
            throw new BusinessException("Only reopened bugs can be moved back to In Progress.");
        }
        if (bug.getAssignee() == null) {
            throw new BusinessException("Assign the bug before moving it to In Progress.");
        }
        boolean allowed = bug.getAssignee().getId().equals(actor.getId()) || projectService.canManage(bug.getProject(), actor);
        if (!allowed) {
            throw new BusinessException("Only the assigned developer or project manager can resume this bug.");
        }
        bug.setStatus(BugStatus.IN_PROGRESS);
    }

    private void resolveBug(BugTicket bug, UserAccount actor) {
        if (actor.getRole() != Role.DEVELOPER || bug.getAssignee() == null
                || !bug.getAssignee().getId().equals(actor.getId())) {
            throw new BusinessException("Only the assigned developer can mark a bug as Resolved.");
        }
        if (bug.getStatus() != BugStatus.IN_PROGRESS && bug.getStatus() != BugStatus.REOPENED) {
            throw new BusinessException("Only bugs in progress or reopened can be resolved.");
        }
        if (timeLogRepository.sumMinutesByBug(bug) <= 0) {
            throw new BusinessException("Log time before marking the bug as resolved.");
        }
        bug.setStatus(BugStatus.RESOLVED);
        bug.setResolvedAt(LocalDateTime.now());
        bug.setClosedAt(null);
    }

    private void reopenBug(BugTicket bug, UserAccount actor) {
        if (!canVerifyBug(actor, bug.getProject())) {
            throw new BusinessException("Only Testers and Project Managers can reopen bugs.");
        }
        if (bug.getStatus() != BugStatus.RESOLVED && bug.getStatus() != BugStatus.CLOSED) {
            throw new BusinessException("Only resolved or closed bugs can be reopened.");
        }
        bug.setStatus(BugStatus.REOPENED);
        bug.setClosedAt(null);
    }

    private void closeBug(BugTicket bug, UserAccount actor) {
        if (!canVerifyBug(actor, bug.getProject())) {
            throw new BusinessException("Only Testers and Project Managers can close bugs.");
        }
        if (bug.getStatus() != BugStatus.RESOLVED) {
            throw new BusinessException("Only resolved bugs can be closed.");
        }
        bug.setStatus(BugStatus.CLOSED);
        bug.setClosedAt(LocalDateTime.now());
    }

    private boolean canVerifyBug(UserAccount actor, Project project) {
        return actor.getRole() == Role.TESTER || projectService.canManage(project, actor);
    }

    private Sort resolveSort(String sortBy) {
        if ("createdDesc".equalsIgnoreCase(sortBy)) {
            return Sort.by(Sort.Direction.DESC, "createdAt");
        }
        if ("priority".equalsIgnoreCase(sortBy)) {
            return Sort.by(Sort.Direction.DESC, "priority").and(Sort.by(Sort.Direction.DESC, "updatedAt"));
        }
        if ("status".equalsIgnoreCase(sortBy)) {
            return Sort.by(Sort.Direction.ASC, "status").and(Sort.by(Sort.Direction.DESC, "updatedAt"));
        }
        if ("title".equalsIgnoreCase(sortBy)) {
            return Sort.by(Sort.Direction.ASC, "title");
        }
        return Sort.by(Sort.Direction.DESC, "updatedAt");
    }
}
