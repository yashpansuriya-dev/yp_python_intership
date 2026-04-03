package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.UserAccount;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface BugTicketRepository extends JpaRepository<BugTicket, Long>, JpaSpecificationExecutor<BugTicket> {

    Optional<BugTicket> findByTicketId(String ticketId);

    long countByProject(Project project);

    long countByProjectAndAssignee(Project project, UserAccount assignee);

    List<BugTicket> findTop10ByArchivedFalseOrderByCreatedAtDesc();
}