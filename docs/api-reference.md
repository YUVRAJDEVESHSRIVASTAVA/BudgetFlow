# API Reference

All protected endpoints expect a Bearer token in the `Authorization` header.

```http
Authorization: Bearer <access-token>
```

## Authentication

| Endpoint | Method | Auth | Purpose |
| --- | --- | --- | --- |
| `/api/auth/register/` | POST | No | Create a new user and return tokens |
| `/api/auth/login/` | POST | No | Log in with username or email |
| `/api/auth/logout/` | POST | Yes | Record a logout event |
| `/api/auth/refresh/` | POST | No | Refresh the access token |
| `/api/auth/me/` | GET | Yes | Return the current user profile |
| `/api/auth/me/` | PATCH | Yes | Update the current user profile |

### Register Payload

```json
{
  "username": "asha_patel",
  "email": "asha.patel@example.com",
  "first_name": "Asha",
  "last_name": "Patel",
  "password": "DemoUser@1234",
  "confirm_password": "DemoUser@1234"
}
```

### Login Payload

```json
{
  "identifier": "asha_patel",
  "password": "DemoUser@1234"
}
```

## Categories

| Endpoint | Method | Auth | Purpose |
| --- | --- | --- | --- |
| `/api/categories/` | GET | Yes | List the current user's categories |
| `/api/categories/` | POST | Yes | Create a category |
| `/api/categories/{id}/` | GET | Yes | Read one category |
| `/api/categories/{id}/` | PATCH | Yes | Update a category |
| `/api/categories/{id}/` | DELETE | Yes | Delete a category |

## Expenses

| Endpoint | Method | Auth | Purpose |
| --- | --- | --- | --- |
| `/api/expenses/` | GET | Yes | List the current user's expenses |
| `/api/expenses/` | POST | Yes | Create an expense |
| `/api/expenses/{id}/` | GET | Yes | Read one expense |
| `/api/expenses/{id}/` | PATCH | Yes | Update an expense |
| `/api/expenses/{id}/` | DELETE | Yes | Delete an expense |

The expense list supports these query parameters:

- `search`
- `category`
- `start_date`
- `end_date`
- `ordering`

Example:

```text
/api/expenses/?search=coffee&ordering=-spent_on
```

## Summary

| Endpoint | Method | Auth | Purpose |
| --- | --- | --- | --- |
| `/api/summary/` | GET | Yes | Return dashboard totals, averages, category breakdowns, and recent expenses |

The summary response includes:

- `total_spent`
- `monthly_total`
- `monthly_average`
- `expense_count`
- `monthly_expense_count`
- `budget_total`
- `need_to_pay_amount`
- `need_to_pay_label`
- `category_breakdown`
- `recent_expenses`
