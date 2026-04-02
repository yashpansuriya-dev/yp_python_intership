package com.yash.bugtracker.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import java.time.LocalDate;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "time_logs")
public class TimeLog extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private BugTicket bug;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private UserAccount user;

    @Column(nullable = false)
    private Integer minutesSpent;

    @Column(nullable = false)
    private LocalDate logDate;

    @Column(length = 1000)
    private String note;
}
