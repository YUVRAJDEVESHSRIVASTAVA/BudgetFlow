# Deployment Guide - Render.com

This guide walks you through deploying **ExpenseFlow** to Render.com, a free cloud platform.

---

## Prerequisites

- GitHub account (with this repo pushed)
- Render.com account (sign up at https://render.com)
- Credit/debit card for Render (free tier available, no charges)

---

## Deployment Steps

### Step 1: Push Code to GitHub

Ensure your code is pushed to GitHub:

```bash
git add .
git commit -m "Add Render deployment files"
git push origin main
```

### Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### Step 3: Deploy Using `render.yaml`

Render can automatically deploy from your `render.yaml` file:

#### Option A: Deploy via Dashboard (Easy)
1. Log in to Render Dashboard
2. Click **"New +"** → **"Blueprint"**
3. Select your GitHub repository
4. Render will auto-detect `render.yaml`
5. Review settings and click **"Deploy"**

#### Option B: Manual Setup (If Option A doesn't work)

**Create Web Service:**
1. Click **"New +"** → **"Web Service"**
2. Select your GitHub repository
3. Fill in:
   - **Name:** `expenseflow-api`
   - **Environment:** `Python 3`
   - **Build Command:** `bash ./build.sh`
   - **Start Command:** `cd backend && gunicorn expense_tracker.wsgi:application --bind 0.0.0.0:$PORT`
4. Click **"Create Web Service"**

**Create PostgreSQL Database:**
1. Click **"New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name:** `expenseflow-db`
   - **Database:** `expenseflow`
   - **Region:** Same as web service
   - **Plan:** Free
3. Click **"Create Database"**

### Step 4: Set Environment Variables

In your Render Dashboard:

1. Go to **Web Service** → **Environment**
2. Add these variables:

```
DJANGO_SECRET_KEY=<generate-a-long-random-key-64-chars>
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=<your-render-domain>.onrender.com
DATABASE_URL=<auto-filled-from-postgres-db>
```

**Generate a secure SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Wait for Deployment

- Render will build and deploy automatically
- Check the **Logs** tab for progress
- Deployment takes 5-10 minutes
- Once complete, you'll see a green checkmark ✓

### Step 6: Access Your App

Your app will be available at: `https://<your-service-name>.onrender.com`

**Try these URLs:**
- Home: `https://<your-domain>.onrender.com/`
- Login: `https://<your-domain>.onrender.com/login/`
- Admin: `https://<your-domain>.onrender.com/admin/`
  - Username: `trafficadmin`
  - Password: `password123`

---

## Post-Deployment Verification

### 1. Check Admin Dashboard

```
https://<your-domain>.onrender.com/admin/
```

Log in with demo credentials to verify the app is running.

### 2. View Logs

In Render Dashboard:
1. Select your Web Service
2. Go to **Logs** tab
3. Watch for any errors during requests

### 3. Database Check

In Render Dashboard:
1. Select your PostgreSQL instance
2. Go to **Info** tab
3. Verify **Connection String** is populated

---

## Common Issues & Fixes

### Issue: "Page Not Found" (404)

**Cause:** Static files not collected properly.

**Fix:**
```bash
cd backend
python manage.py collectstatic --noinput
```

Re-deploy on Render.

### Issue: "Internal Server Error" (500)

**Check logs in Render Dashboard:**
1. Go to **Logs** tab
2. Look for error messages
3. Common causes:
   - Missing `SECRET_KEY` environment variable
   - Database not connected
   - Missing migrations

### Issue: Static Files Not Loading (CSS/JS broken)

**Cause:** STATIC_ROOT not set or WhiteNoise not installed.

**Fix:**
1. Verify `whitenoise` is in `backend/requirements.txt`
2. Ensure `settings.py` has `STATIC_ROOT` configured
3. Re-deploy

If you use the root-level Render build, make sure the top-level `requirements.txt` points to `backend/requirements.txt`.

### Issue: Database Connection Failed

**Fix:**
1. Verify DATABASE_URL is set in environment variables
2. Check PostgreSQL instance is running (green status in Render)
3. Manually restart web service: Render Dashboard → Service → **Manual Deploy**

---

## Development Workflow

### Develop Locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Open: `http://localhost:8000/`

### Deploy Changes

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will auto-redeploy when you push to `main` branch.

**To manually trigger deployment:**
1. Render Dashboard → Web Service
2. Click **"Manual Deploy"** button

---

## Upgrading from Free to Paid

If you need more resources:
1. Render Dashboard → Web Service
2. Click **Plan** in settings
3. Upgrade to **Starter** ($7/month) or higher

---

## Monitoring & Logs

### View Real-time Logs

```bash
# Using Render CLI (install from https://render.com/docs/cli)
render logs --service expenseflow-api
```

Or use Dashboard → **Logs** tab.

### Monitor Database

Render Dashboard → PostgreSQL instance → **Info** tab

---

## Backup & Data

### Export Database

```bash
# Using Render Dashboard
1. Go to PostgreSQL instance
2. Click "Connect" dropdown
3. Copy connection string
4. Use `pg_dump` to backup:
   pg_dump <connection-string> > backup.sql
```

### Restore Database

```bash
psql <connection-string> < backup.sql
```

---

## Redeploy or Restart

### Restart Web Service
Render Dashboard → Web Service → **Settings** → **Restart Service**

### Full Redeploy
Render Dashboard → Web Service → **Manual Deploy**

---

## Production Best Practices

✅ **Done in this setup:**
- Django DEBUG set to `false`
- HTTPS enabled automatically
- Static files served via WhiteNoise
- Database migrations automated
- Demo data seeded on first deploy

✅ **Consider adding:**
- Email notifications for errors
- Database backups scheduled
- Custom domain name
- Redis cache for performance
- CORS configuration (currently allows all origins)

---

## Support & Troubleshooting

**Render Support:** https://render.com/docs  
**Django Deployment:** https://docs.djangoproject.com/en/5.0/howto/deployment/  
**This Project:** Check `docs/` folder for architecture details

---

## Next Steps

1. ✅ Deploy to Render (this guide)
2. Add custom domain name (Render Dashboard → Web Service → Settings)
3. Set up automatic backups
4. Configure production email (for password resets)
5. Monitor logs and performance

---

**Happy deploying! 🚀**
