package com.yash.bugtracker.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "bug_comments")
public class BugComment extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private BugTicket bug;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private UserAccount author;

    @Column(nullable = false, length = 2000)
    private String message;
}
