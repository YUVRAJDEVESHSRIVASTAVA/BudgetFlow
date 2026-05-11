# Project Overview

BudgetFlow is a browser-based personal finance tracker built with Django, Django REST Framework, SimpleJWT, and a vanilla HTML/CSS/JavaScript frontend. The app is designed to be simple enough for a demo, but it still shows the full loop of authentication, data entry, reporting, and admin monitoring.

## What The App Does

- Users register and log in with JWT tokens.
- Each user owns their categories and expenses.
- The dashboard shows totals, monthly numbers, category breakdowns, and a need-to-pay alert when spending goes over budget.
- Admin users can view auth traffic and recent login and logout activity.

## Why It Exists

The project was built to demonstrate a small but complete expense tracker that is easy to explain:

- it has authentication,
- it persists data,
- it has a dashboard,
- it has admin visibility,
- and it includes demo data and screenshots for presentation.

## Main Parts

- Django backend for the API and admin
- Frontend templates and JavaScript for the browser UI
- SQLite for local storage
- AuthEvent records for auditing sign in and sign out activity
