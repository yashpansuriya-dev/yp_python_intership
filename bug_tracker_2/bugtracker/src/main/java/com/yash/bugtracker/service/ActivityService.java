package com.yash.bugtracker.service;

import com.yash.bugtracker.entity.ActivityLog;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.ActivityAction;
import com.yash.bugtracker.repository.ActivityLogRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ActivityService {

    private final ActivityLogRepository activityLogRepository;

    @Transactional
    public void log(BugTicket bug, UserAccount actor, ActivityAction action, String description) {
        ActivityLog activityLog = new ActivityLog();
        activityLog.setBug(bug);
        activityLog.setActor(actor);
        activityLog.setAction(action);
        activityLog.setDescription(description);
        activityLogRepository.save(activityLog);
    }
}
