package com.yash.bugtracker.repository;

import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.enums.Role;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserAccountRepository extends JpaRepository<UserAccount, Long> {

    Optional<UserAccount> findByEmailIgnoreCase(String email);

    @EntityGraph(attributePaths = {"projectMemberships", "projectMemberships.project"})
    Optional<UserAccount> findWithProjectMembershipsById(Long id);

    boolean existsByEmailIgnoreCase(String email);

    List<UserAccount> findAllByOrderByFullNameAsc();

    List<UserAccount> findAllByActiveTrueOrderByFullNameAsc();

    List<UserAccount> findAllByRoleAndActiveTrueOrderByFullNameAsc(Role role);

    long countByRoleAndActiveTrue(Role role);
}
