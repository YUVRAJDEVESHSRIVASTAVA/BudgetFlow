# How It Was Built

This page is the short history of how BudgetFlow came together. It is meant to be easy to explain to another person.

## 1. Start With The Data Model

The first step was defining the core records:

- a custom user model,
- categories,
- expenses,
- and auth events.

That gave the project a place to store users, spending, and login history.

## 2. Add Authentication

JWT authentication was added so the browser could log in without server sessions. The auth app exposes register, login, logout, refresh, and me endpoints.

The important design choice was to store login and logout activity in `AuthEvent` instead of only relying on `last_login`.

## 3. Build The Expense APIs

The expenses app adds user-scoped categories and expenses. The summary endpoint was then built on top of those records so the dashboard can show totals, averages, category breakdowns, and over-budget alerts.

## 4. Add The Browser UI

The frontend uses plain HTML, CSS, and JavaScript. It calls the API through a shared helper that:

- stores the JWT session in localStorage,
- attaches the access token to requests,
- refreshes the access token when needed,
- and clears the session on logout.

## 5. Add Admin Observability

An admin traffic dashboard was added under `/admin/traffic/`. It summarizes:

- total users,
- login and logout counts,
- recent auth events,
- and per-user activity.

This is the part that makes the project easy to demo to non-technical users because it shows activity instead of only raw tables.

## 6. Seed Demo Data

The `seed_demo_data` command creates demo users, categories, expenses, and auth events. It also creates a `trafficadmin` account so the admin dashboard can be shown immediately after setup.

## 7. Polish The Presentation

The final pass added screenshots, a stronger README, and this documentation folder so the project is easy to browse in GitHub.

## Short Explanation You Can Tell Someone Else

BudgetFlow is a Django expense tracker where users log in with JWT, track categories and expenses, and see spending totals in a dashboard while admins can review login and logout activity.
