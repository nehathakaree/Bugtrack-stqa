# BugTrack — Bug Tracking and Test Case Management System

BugTrack is an academic Software Testing and Quality Assurance project built with Python Flask and MySQL. It includes registration/login, a dashboard, test-case management and execution, defect reporting and status tracking, and test execution metrics.

## Tech stack
- Python 3.10+
- Flask and Flask-SQLAlchemy
- MySQL 8+ (PyMySQL driver)
- HTML, CSS, Bootstrap 5, Jinja
- pytest

## Setup
1. Install Python 3.10+ and MySQL 8+.
2. In MySQL Workbench or the MySQL CLI, run `schema.sql`. Change the example password before using it.
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell: .venv\Scripts\Activate.ps1
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Set environment variables. PowerShell example:
   ```powershell
   $env:DATABASE_URL="mysql+pymysql://bugtrack_user:YOUR_PASSWORD@localhost/bugtrack"
   $env:SECRET_KEY="replace-with-a-long-random-secret"
   ```
5. Create the tables and start the app:
   ```bash
   flask --app app init-db
   python app.py
   ```
6. Open http://127.0.0.1:5000 and register a user.

## Features
- Password-hashed account registration and login
- Dashboard with test and bug counts
- Create/search test cases and record Pass, Fail, Blocked or Not Run
- Report defects with severity and priority
- Track bug status through Open, In Progress, Fixed, Retest and Closed
- Test execution summary and pass rate

## Testing
Run `pytest -q`. The manual test specifications are in `docs/MANUAL_TEST_CASES.md`; record actual results and screenshots when you execute them. Do not claim manual tests passed before running them.

## Project report
See `docs/PROJECT_REPORT.md`.

## Notes
This is a student/demo project, not production-hardened. Add CSRF protection, rate limiting, stronger role/authorization controls, audit logs, migrations and secure deployment configuration before production use. Do not expose Flask's development server publicly.
