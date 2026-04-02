package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.ProjectMembership;
import com.yash.bugtracker.entity.UserAccount;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProjectMembershipRepository extends JpaRepository<ProjectMembership, Long> {

    List<ProjectMembership> findByUserOrderByProject_NameAsc(UserAccount user);

    List<ProjectMembership> findByProjectOrderByUser_FullNameAsc(Project project);

    List<ProjectMembership> findByUser(UserAccount user);

    Optional<ProjectMembership> findByProjectAndUser(Project project, UserAccount user);

    boolean existsByProjectAndUser(Project project, UserAccount user);

    long countByProject(Project project);
}
