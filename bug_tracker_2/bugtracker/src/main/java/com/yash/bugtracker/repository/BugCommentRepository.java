package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.BugComment;
import com.yash.bugtracker.entity.BugTicket;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BugCommentRepository extends JpaRepository<BugComment, Long> {

    List<BugComment> findByBugOrderByCreatedAtAsc(BugTicket bug);
}
