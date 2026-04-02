package com.yash.bugtracker.service;

import com.yash.bugtracker.config.StorageProperties;
import com.yash.bugtracker.entity.BugAttachment;
import com.yash.bugtracker.entity.BugTicket;
import com.yash.bugtracker.entity.UserAccount;
import com.yash.bugtracker.exception.BusinessException;
import jakarta.annotation.PostConstruct;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

@Service
@RequiredArgsConstructor
public class FileStorageService {

    private static final Set<String> ALLOWED_EXTENSIONS = Set.of(
            "png", "jpg", "jpeg", "gif", "bmp", "webp", "pdf", "txt", "log", "zip", "json", "csv"
    );

    private final StorageProperties storageProperties;
    private Path rootPath;

    @PostConstruct
    public void init() {
        try {
            rootPath = Paths.get(storageProperties.uploadDir()).toAbsolutePath().normalize();
            Files.createDirectories(rootPath);
        } catch (IOException exception) {
            throw new BusinessException("Unable to initialize file storage.");
        }
    }

    public List<BugAttachment> storeAttachments(BugTicket bug, UserAccount actor, MultipartFile[] files) {
        List<BugAttachment> attachments = new ArrayList<>();
        if (files == null) {
            return attachments;
        }

        Path bugDirectory = rootPath.resolve(bug.getTicketId()).normalize();
        try {
            Files.createDirectories(bugDirectory);
        } catch (IOException exception) {
            throw new BusinessException("Unable to create bug attachment directory.");
        }

        for (MultipartFile file : files) {
            if (file == null || file.isEmpty()) {
                continue;
            }
            validateFile(file);

            String originalFilename = StringUtils.cleanPath(file.getOriginalFilename());
            String extension = getExtension(originalFilename);
            String storedFilename = UUID.randomUUID() + "." + extension;
            Path target = bugDirectory.resolve(storedFilename).normalize();

            try (InputStream inputStream = file.getInputStream()) {
                Files.copy(inputStream, target, StandardCopyOption.REPLACE_EXISTING);
            } catch (IOException exception) {
                throw new BusinessException("Failed to store attachment: " + originalFilename);
            }

            BugAttachment attachment = new BugAttachment();
            attachment.setBug(bug);
            attachment.setUploadedBy(actor);
            attachment.setOriginalFilename(originalFilename);
            attachment.setStoredFilename(storedFilename);
            attachment.setFilePath(target.toString());
            attachment.setContentType(file.getContentType());
            attachment.setSize(file.getSize());
            attachments.add(attachment);
        }

        return attachments;
    }

    public Resource loadAsResource(BugAttachment attachment) {
        try {
            Path path = Paths.get(attachment.getFilePath()).normalize();
            Resource resource = new UrlResource(path.toUri());
            if (!resource.exists() || !resource.isReadable()) {
                throw new BusinessException("Attachment file is not available.");
            }
            return resource;
        } catch (Exception exception) {
            throw new BusinessException("Attachment file is not available.");
        }
    }

    private void validateFile(MultipartFile file) {
        String originalFilename = StringUtils.cleanPath(file.getOriginalFilename());
        if (!StringUtils.hasText(originalFilename) || originalFilename.contains("..")) {
            throw new BusinessException("Invalid file name.");
        }

        String extension = getExtension(originalFilename);
        if (!ALLOWED_EXTENSIONS.contains(extension)) {
            throw new BusinessException("Unsupported attachment type. Allowed: screenshots, logs, PDFs, ZIP, JSON, CSV.");
        }
    }

    private String getExtension(String filename) {
        int index = filename.lastIndexOf('.');
        if (index < 0 || index == filename.length() - 1) {
            throw new BusinessException("Files must include an extension.");
        }
        return filename.substring(index + 1).toLowerCase();
    }
}
