# Quick Render Deployment - 5 Steps

## ⚡ TL;DR - Deploy in 5 Minutes

### Step 1: Generate Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Save this key.

### Step 2: Push to GitHub
```bash
git add .
git commit -m "Add Render deployment config"
git push origin main
```

### Step 3: Go to Render.com
1. Sign up at [render.com](https://render.com) with GitHub
2. Click **"New +"** → **"Blueprint"**
3. Select your repository

### Step 4: Set Environment Variable
- **DJANGO_SECRET_KEY:** Paste the key from Step 1
- Let other variables auto-fill

### Step 5: Click Deploy
- Wait 5-10 minutes
- Done! Your app is live at `https://<your-domain>.onrender.com`

---

## 🔗 Admin Login
- URL: `https://<your-domain>/admin/`
- Username: `trafficadmin`
- Password: `password123`

---

## 📚 Full Guide
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions and troubleshooting.

---

## ✅ What's Included

✓ PostgreSQL database (auto-created)  
✓ Static files served with WhiteNoise  
✓ HTTPS enabled  
✓ Demo data seeded automatically  
✓ Auto-restart on code push  

---

## 🆘 Troubleshooting

**Page not found?**
- Check logs in Render Dashboard → Logs tab
- Ensure `SECRET_KEY` is set

**Static files broken (no CSS)?**
- Wait for deployment to complete
- Hard refresh browser (Ctrl+Shift+R)

**Database error?**
- Check PostgreSQL is running (green status)
- Click "Manual Deploy" to restart

---

See [DEPLOYMENT.md](DEPLOYMENT.md) for more help!
