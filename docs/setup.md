# Setup Guide

## Prerequisites

- Python 3
- A virtual environment
- Access to the project root

## Install And Run

```powershell
# from the project root
python -m venv .venv
.venv\Scripts\Activate.ps1
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Open the app at http://127.0.0.1:8000/.

## Useful Commands

- `python manage.py check`
- `python manage.py test`
- `python manage.py makemigrations`
- `python manage.py migrate`

## Demo Accounts

- Admin user: `trafficadmin`
- Admin password: `TrafficAdmin@1234`
- Demo user password: `DemoUser@1234`
- Demo usernames: `asha_patel`, `imran_khan`, `meera_rao`, `daniel_joseph`, `priya_nair`

## Notes

- The browser stores the session in localStorage under `expenseflow.session`.
- Refresh tokens are used to renew the access token automatically.
- The seed command recreates demo data by removing only the seeded demo users and admin account.
