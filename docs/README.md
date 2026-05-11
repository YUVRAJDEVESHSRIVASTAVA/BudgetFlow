# BudgetFlow Documentation

BudgetFlow is a Django and REST-based expense tracker with JWT authentication, user-owned categories and expenses, a dashboard summary, and an admin traffic view for login and logout auditing.

This folder is the long-form guide for the project. If you want the short version, start with the root [README](../README.md). If you want to explain the app to someone else, read the docs in this order:

1. [Project Overview](overview.md)
2. [Setup Guide](setup.md)
3. [Architecture](architecture.md)
4. [Data Model](data-model.md)
5. [API Reference](api-reference.md)
6. [How It Was Built](build-notes.md)
7. [Screenshots](screenshots/README.md)

## Where The Code Lives

| Area | Path | What It Contains |
| --- | --- | --- |
| Backend | `backend/` | Django project, apps, migrations, admin, and management commands |
| Frontend | `frontend/` | HTML templates, CSS, and vanilla JavaScript |
| Database | `backend/db.sqlite3` | Local SQLite database |
| Docs | `docs/` | This documentation hub |

## One-Line Explanation

BudgetFlow lets a signed-in user track categories and expenses, while the admin can inspect who logged in, who logged out, and when those events happened.
