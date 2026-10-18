# BugTrack — Bug Tracking and Test Case Management System

## Abstract
BugTrack is a web application for Software Testing and Quality Assurance. It supports test-case creation, execution tracking, defect reporting, lifecycle updates and basic quality metrics.

## 1. Introduction
Tracking test cases and defects in separate documents can cause duplicated work and unclear progress. BugTrack brings these activities into a single web workspace.

## 2. Problem Statement
A lightweight system is needed to record test scenarios, execution outcomes and defects. It should help testers monitor defect status and summarize test progress.

## 3. Objectives
- Create and manage test cases.
- Record Pass, Fail, Blocked and Not Run outcomes.
- Report defects with reproduction steps, severity and priority.
- Track bugs through their lifecycle.
- Calculate test totals and pass rate.
- Validate features using automated and manual tests.

## 4. Technologies
Python, Flask, Flask-SQLAlchemy, MySQL, HTML, CSS, Bootstrap 5 and pytest.

## 5. Architecture
Browser requests are handled by Flask routes; SQLAlchemy models persist data in MySQL; Jinja templates render the UI. User records store password hashes. Test cases and bugs link to their creator.

## 6. Modules
Authentication, dashboard, test-case management, test execution, defect tracking and reports.

## 7. Testing
The manual test specifications are in MANUAL_TEST_CASES.md. Execute them and record actual results; do not report unexecuted tests as passed.

Pass rate = (passed tests / total tests) × 100. Empty reports return 0% to avoid division by zero.

## 8. Limitations and security
Passwords are hashed and records are scoped to their creator. This academic version does not include team assignments, attachments, notifications or admin UI. Before production use, add CSRF protection, rate limiting, stronger authorization, audit logs, migrations and deployment hardening.

## 9. Conclusion and future scope
BugTrack demonstrates centralized test-case and defect management. Future work could add team roles, exportable reports, browser automation, CI integration, audit history and notifications.

## References
- Flask: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- MySQL: https://dev.mysql.com/doc/
- pytest: https://docs.pytest.org/
- Bootstrap: https://getbootstrap.com/docs/
