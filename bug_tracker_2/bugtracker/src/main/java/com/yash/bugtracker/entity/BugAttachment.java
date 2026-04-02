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
@Table(name = "bug_attachments")
public class BugAttachment extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private BugTicket bug;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private UserAccount uploadedBy;

    @Column(nullable = false, length = 255)
    private String originalFilename;

    @Column(nullable = false, length = 255)
    private String storedFilename;

    @Column(nullable = false, length = 255)
    private String filePath;

    @Column(length = 100)
    private String contentType;

    @Column(nullable = false)
    private long size;
}
