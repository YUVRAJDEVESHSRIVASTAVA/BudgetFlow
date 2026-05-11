# Data Model

## User

The project uses a custom user model in `apps.accounts.models.User`.

| Field | Purpose |
| --- | --- |
| `username` | Primary login identifier for most users |
| `email` | Unique email address, also usable for login |
| `first_name` / `last_name` | Profile display fields |
| `is_staff` / `is_superuser` | Admin access control |
| `last_login` | Updated when login events are recorded |

## AuthEvent

`AuthEvent` stores login and logout activity for auditing.

| Field | Purpose |
| --- | --- |
| `user` | User who triggered the event |
| `event_type` | `login` or `logout` |
| `identifier` | Username or email used during login |
| `ip_address` | Client IP address |
| `user_agent` | Browser or client string |
| `created_at` | Event timestamp |

## Category

Categories are owned by a single user.

| Field | Purpose |
| --- | --- |
| `user` | Owner of the category |
| `name` | Category label |
| `color` | Display color used in the UI |
| `budget_limit` | Optional budget threshold |
| `created_at` / `updated_at` | Timestamps |

The model enforces a unique category name per user.

## Expense

Expenses are also owned by a user and can be attached to a category.

| Field | Purpose |
| --- | --- |
| `user` | Owner of the expense |
| `category` | Optional category link |
| `title` | Expense name |
| `amount` | Decimal amount |
| `spent_on` | Date the expense happened |
| `description` | Optional notes |
| `created_at` / `updated_at` | Timestamps |

## Relationships

- A user has many categories.
- A user has many expenses.
- A user has many auth events.
- A category can have many expenses.
