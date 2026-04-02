package com.yash.bugtracker.service;

import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.exception.NotFoundException;
import com.yash.bugtracker.repository.UserAccountRepository;
import com.yash.bugtracker.security.AppUserDetails;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CurrentUserService {

    private final UserAccountRepository userAccountRepository;

    public UserAccount getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated()
                || authentication instanceof AnonymousAuthenticationToken) {
            throw new NotFoundException("Authenticated user not found.");
        }

        Object principal = authentication.getPrincipal();
        if (principal instanceof AppUserDetails userDetails) {
            return userAccountRepository.findById(userDetails.getId())
                    .orElseThrow(() -> new NotFoundException("Authenticated user no longer exists."));
        }
        return userAccountRepository.findByEmailIgnoreCase(authentication.getName())
                .orElseThrow(() -> new NotFoundException("Authenticated user no longer exists."));
    }
}
