package com.yash.bugtracker.controller;

import com.yash.bugtracker.exception.BusinessException;
import com.yash.bugtracker.exception.NotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler({BusinessException.class, NotFoundException.class})
    public String handleKnownExceptions(RuntimeException exception, Model model) {
        model.addAttribute("errorTitle", "Request could not be completed");
        model.addAttribute("errorMessage", exception.getMessage());
        return "error";
    }

    @ExceptionHandler(AccessDeniedException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public String handleAccessDenied(AccessDeniedException exception, Model model) {
        model.addAttribute("errorTitle", "Access denied");
        model.addAttribute("errorMessage", "You do not have permission to access this page or action.");
        return "error";
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public String handleUnexpectedExceptions(Exception exception, Model model) {
        log.error("Unhandled application error", exception);
        model.addAttribute("errorTitle", "Unexpected application error");
        model.addAttribute("errorMessage", "Something went wrong while processing your request. Please try again.");
        return "error";
    }
}
