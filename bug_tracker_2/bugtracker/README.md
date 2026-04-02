# BugTrackPro

BugTrackPro is a Spring Boot + MySQL bug tracking and developer task analytics system built from the provided SRS and extended into a working semester-project application.

## Features

- Secure login with role-based access for `ADMIN`, `PROJECT_MANAGER`, `DEVELOPER`, and `TESTER`
- Admin-driven user management with role assignment, activation/deactivation, and project mapping
- Project creation, manager assignment, team membership management, and status tracking
- Bug reporting with unique ticket IDs, priority, severity, reproduction notes, and file attachments
- Workflow management across `OPEN`, `IN_PROGRESS`, `RESOLVED`, `REOPENED`, and `CLOSED`
- Assignment rules, comments, activity history, time logging, dashboard analytics, search, filters, and CSV reports
- Archive flow for safe deletion behavior, aligned with the SRS business rules

## Tech Stack

- Java 17
- Spring Boot 4
- Spring MVC
- Spring Security
- Spring Data JPA / Hibernate
- Thymeleaf
- MySQL
- H2 for tests

## Default Demo Accounts

- Admin: `admin@bugtrackpro.local` / `Admin@123`
- Project Manager: `manager@bugtrackpro.local` / `Manager@123`
- Developer: `developer@bugtrackpro.local` / `Developer@123`
- Tester: `tester@bugtrackpro.local` / `Tester@123`

## Run Locally

1. Make sure MySQL is running.
2. Update credentials if needed through environment variables:
   - `BUGTRACKER_DB_URL`
   - `BUGTRACKER_DB_USERNAME`
   - `BUGTRACKER_DB_PASSWORD`
3. Start the app:

```bash
./mvnw spring-boot:run
```

4. Open `http://localhost:8080`

## Notes

- Demo seed data is enabled by default through `app.seed-demo-data=true`.
- File attachments are stored in the local `uploads/` folder.
- Tests use H2 and disable demo seed data automatically.
