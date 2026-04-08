package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.UserAccount;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

// jpaspecification for dynamic query support               entitiy   key type
public interface BugTicketRepository extends JpaRepository<BugTicket, Long>, JpaSpecificationExecutor<BugTicket> {

    // find bugs using ticket id
    Optional<BugTicket> findByTicketId(String ticketId);

    // counts bugs in project
    long countByProject(Project project);

    // counts bugs assigned to user in project
    long countByProjectAndAssignee(Project project, UserAccount assignee);

    // gets latest 10 non archived bugs
    List<BugTicket> findTop10ByArchivedFalseOrderByCreatedAtDesc();
}