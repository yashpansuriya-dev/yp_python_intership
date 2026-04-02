package com.yash.bugtracker.dto;

import com.yash.bugtracker.enums.BugPriority;
import com.yash.bugtracker.enums.BugSeverity;
import com.yash.bugtracker.enums.BugStatus;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BugSearchCriteria {

    private String keyword;
    private Long projectId;
    private BugStatus status;
    private BugPriority priority;
    private BugSeverity severity;
    private Long assigneeId;
    private String viewMode = "all";
    private String sortBy = "updatedDesc";
}
