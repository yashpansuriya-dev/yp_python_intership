package com.yash.bugtracker.controller;

import com.yash.bugtracker.entity.BugAttachment;
import com.yash.bugtracker.service.BugService;
import com.yash.bugtracker.service.CurrentUserService;
import com.yash.bugtracker.service.FileStorageService;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
@RequiredArgsConstructor
public class AttachmentController {

    private final BugService bugService;
    private final FileStorageService fileStorageService;
    private final CurrentUserService currentUserService;

    @GetMapping("/attachments/{id}")
    public ResponseEntity<Resource> downloadAttachment(@PathVariable Long id) {
        BugAttachment attachment = bugService.getAttachmentForUser(id, currentUserService.getCurrentUser());
        Resource resource = fileStorageService.loadAsResource(attachment);

        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType(
                        attachment.getContentType() == null ? MediaType.APPLICATION_OCTET_STREAM_VALUE : attachment.getContentType()
                ))
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + attachment.getOriginalFilename() + "\"")
                .body(resource);
    }
}
