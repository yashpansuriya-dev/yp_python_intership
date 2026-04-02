package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.TimeLog;
import com.yash.bugtracker.entity.UserAccount;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface TimeLogRepository extends JpaRepository<TimeLog, Long> {

    List<TimeLog> findByBugOrderByCreatedAtDesc(BugTicket bug);

    @Query("select coalesce(sum(t.minutesSpent), 0) from TimeLog t where t.bug = :bug")
    long sumMinutesByBug(@Param("bug") BugTicket bug);

    @Query("select coalesce(sum(t.minutesSpent), 0) from TimeLog t where t.user = :user")
    long sumMinutesByUser(@Param("user") UserAccount user);
}
