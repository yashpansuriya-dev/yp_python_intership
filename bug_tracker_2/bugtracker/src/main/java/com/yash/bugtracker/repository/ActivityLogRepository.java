package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.ActivityLog;
import com.yash.bugtracker.entity.BugTicket;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ActivityLogRepository extends JpaRepository<ActivityLog, Long> {

    List<ActivityLog> findByBugOrderByCreatedAtDesc(BugTicket bug);

    List<ActivityLog> findTop20ByOrderByCreatedAtDesc();
}
