package com.yash.bugtracker.repository.specification;

import com.yash.bugtracker.dto.BugSearchCriteria;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.ProjectMembership;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.Role;
import jakarta.persistence.criteria.Join;
import jakarta.persistence.criteria.Predicate;
import java.util.ArrayList;
import java.util.List;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.util.StringUtils;

public final class BugTicketSpecifications {

    private BugTicketSpecifications() {
    }

    public static Specification<BugTicket> notArchived() {
        return (root, query, cb) -> cb.isFalse(root.get("archived"));
    }

    public static Specification<BugTicket> accessibleTo(UserAccount user) {
        return (root, query, cb) -> {
            if (user.getRole() == Role.ADMIN) {
                return cb.conjunction();
            }
            query.distinct(true);
            Join<BugTicket, Project> projectJoin = root.join("project");
            Join<Project, ProjectMembership> membershipJoin = projectJoin.join("memberships");
            return cb.equal(membershipJoin.get("user"), user);
        };
    }

    public static Specification<BugTicket> matches(BugSearchCriteria criteria, UserAccount user) {
        return (root, query, cb) -> {
            List<Predicate> predicates = new ArrayList<>();

            if (StringUtils.hasText(criteria.getKeyword())) {
                String search = "%" + criteria.getKeyword().trim().toLowerCase() + "%";
                predicates.add(
                        cb.or(
                                cb.like(cb.lower(root.get("ticketId")), search),
                                cb.like(cb.lower(root.get("title")), search),
                                cb.like(cb.lower(root.get("description")), search)
                        )
                );
            }

            if (criteria.getProjectId() != null) {
                predicates.add(cb.equal(root.get("project").get("id"), criteria.getProjectId()));
            }
            if (criteria.getStatus() != null) {
                predicates.add(cb.equal(root.get("status"), criteria.getStatus()));
            }
            if (criteria.getPriority() != null) {
                predicates.add(cb.equal(root.get("priority"), criteria.getPriority()));
            }
            if (criteria.getSeverity() != null) {
                predicates.add(cb.equal(root.get("severity"), criteria.getSeverity()));
            }
            if (criteria.getAssigneeId() != null) {
                predicates.add(cb.equal(root.get("assignee").get("id"), criteria.getAssigneeId()));
            }

            if ("new".equalsIgnoreCase(criteria.getViewMode())) {
                predicates.add(cb.isNull(root.get("assignee")));
            } else if ("mine".equalsIgnoreCase(criteria.getViewMode())) {
                predicates.add(cb.equal(root.get("assignee"), user));
            } else if ("reported".equalsIgnoreCase(criteria.getViewMode())) {
                predicates.add(cb.equal(root.get("reporter"), user));
            }

            return cb.and(predicates.toArray(Predicate[]::new));
        };
    }
}
