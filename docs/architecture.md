# Architecture

## Layers

| Layer | Responsibility | Key Files |
| --- | --- | --- |
| Backend | Auth, expenses, admin, API | `backend/apps/accounts/`, `backend/apps/expenses/`, `backend/expense_tracker/urls.py` |
| Frontend | Browser UI and data fetching | `frontend/*.html`, `frontend/js/*.js` |
| Storage | SQLite database | `backend/db.sqlite3` |

## Request Flow

1. Browser pages call `frontend/js/api.js`.
2. `apiRequest` adds a Bearer token from localStorage.
3. The backend validates the token with SimpleJWT.
4. If the access token expires, the helper calls `/api/auth/refresh/`.
5. The Django view returns JSON.
6. The frontend re-renders the dashboard or form state.

## Auth Flow

- `POST /api/auth/register/` creates a user, returns tokens, and records a login event.
- `POST /api/auth/login/` authenticates by username or email and records a login event.
- `POST /api/auth/logout/` records a logout event.
- `GET /api/auth/me/` returns the current user profile.
- `PATCH /api/auth/me/` updates the current user profile.

## Expense Flow

- Categories and expenses are scoped to the authenticated user.
- The dashboard summary aggregates totals, monthly totals, average spend, category breakdown, and over-budget amounts.
- Search and filter parameters are supported on expenses.

## Admin Flow

- `/admin/traffic/` is mounted through `admin.site.admin_view`.
- The traffic view aggregates login and logout counts, recent events, and per-user activity.

## Why This Structure Works

- The frontend stays thin.
- The API can be tested independently.
- The audit trail lives in the database.
- Demo data can be recreated without manual clicking.
