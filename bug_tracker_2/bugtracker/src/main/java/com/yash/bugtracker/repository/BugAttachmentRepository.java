package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.BugAttachment;
import com.yash.bugtracker.entity.BugTicket;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BugAttachmentRepository extends JpaRepository<BugAttachment, Long> {

    List<BugAttachment> findByBugOrderByCreatedAtAsc(BugTicket bug);
}
