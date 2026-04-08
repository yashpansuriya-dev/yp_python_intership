package com.yash.bugtracker.entity;

import com.yash.bugtracker.enums.BugPriority;
import com.yash.bugtracker.enums.BugSeverity;
import com.yash.bugtracker.enums.BugStatus;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.Index;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import java.time.LocalDateTime;
import java.util.LinkedHashSet;
import java.util.Set;
import lombok.Getter;
import lombok.Setter;

// entity represents database tables

@Getter
@Setter
@Entity
@Table(
        name = "bug_tickets",
        indexes = {
                @Index(name = "idx_bug_ticket_id", columnList = "ticketId"),
                @Index(name = "idx_bug_status", columnList = "status"),
                @Index(name = "idx_bug_priority", columnList = "priority")
        }
)
public class BugTicket extends BaseEntity {

    @Column(nullable = false, unique = true, length = 20)
    private String ticketId;

    @Column(nullable = false, length = 180)
    private String title;

    @Column(nullable = false, length = 4000)
    private String description;

    @Column(length = 2000)
    private String stepsToReproduce;

    @Column(length = 2000)
    private String expectedResult;

    @Column(length = 2000)
    private String actualResult;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private BugPriority priority;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private BugSeverity severity;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private BugStatus status = BugStatus.OPEN;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Project project;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private UserAccount reporter;

    @ManyToOne(fetch = FetchType.LAZY)
    private UserAccount assignee;

    @Column(nullable = false)
    private boolean archived = false;

    private LocalDateTime resolvedAt;

    private LocalDateTime closedAt;

    @OneToMany(mappedBy = "bug")
    private Set<BugAttachment> attachments = new LinkedHashSet<>();

    @OneToMany(mappedBy = "bug")
    private Set<BugComment> comments = new LinkedHashSet<>();

    @OneToMany(mappedBy = "bug")
    private Set<TimeLog> timeLogs = new LinkedHashSet<>();

    @OneToMany(mappedBy = "bug")
    private Set<ActivityLog> activities = new LinkedHashSet<>();
}