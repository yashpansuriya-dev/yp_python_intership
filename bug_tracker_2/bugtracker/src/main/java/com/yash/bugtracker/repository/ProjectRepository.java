package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.Project;
import com.yash.bugtracker.entity.UserAccount;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.EntityGraph;

public interface ProjectRepository extends JpaRepository<Project, Long> {

    List<Project> findAllByOrderByNameAsc();

    @EntityGraph(attributePaths = {"manager", "memberships", "memberships.user"})
    Optional<Project> findWithManagerAndMembershipsById(Long id);

    boolean existsByCodeIgnoreCase(String code);

    List<Project> findByManager(UserAccount manager);
}
