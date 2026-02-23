# Railway.app Deployment - Quick Setup Guide

## ✅ Updated Code - Now Supports Railway's MYSQL_URL!

Your `service_layer.py` now automatically detects and uses Railway's connection format.

---

## Step-by-Step Deployment

### 1. Sign Up for Railway
- Go to https://railway.app
- Click **"Login"** → Sign in with GitHub
- Authorize Railway to access your repos

---

### 2. Create MySQL Database

1. Click **"New Project"**
2. Select **"Provision MySQL"**
3. Railway creates a MySQL database
4. Note: Database is automatically running!

---

### 3. Import Your Database Schema

**Option A: Railway Console (Easiest)**

1. Click on your **MySQL** service
2. Click **"Data"** tab
3. Click **"Query"** button (top right)
4. Copy ALL contents from `sql/schema.sql`
5. Paste into query editor
6. Click **"Run"** or press Ctrl+Enter
7. Repeat for `sql/populate_data.sql`

**Option B: Using MySQL Client**

Get connection string from Railway:
1. Click MySQL service → **"Connect"** tab
2. Copy the **"MySQL Command"**
3. Run locally:
```powershell
cd "C:\Users\Butte\Documents\Stock_Tracker\CSCE-548-Stock-Tracker"

# Replace with YOUR Railway connection command
mysql -h containers-us-west-xxx.railway.app -u root -pYOUR_PASSWORD railway --port=XXXX < sql/schema.sql
mysql -h containers-us-west-xxx.railway.app -u root -pYOUR_PASSWORD railway --port=XXXX < sql/populate_data.sql
```

---

### 4. Deploy Your API Service

#### Option A: From GitHub (Recommended)

1. **Push your code to GitHub first:**
```powershell
cd "C:\Users\Butte\Documents\Stock_Tracker\CSCE-548-Stock-Tracker"
git add .
git commit -m "Add Railway deployment support"
git push
```

2. **In Railway Dashboard:**
   - Click **"New"** → **"GitHub Repo"**
   - Select your `CSCE-548-Stock-Tracker` repository
   - Railway will auto-detect it's a Python project
   - Click **"Deploy"**

#### Option B: Railway CLI

```powershell
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

---

### 5. Connect API to MySQL

**This is the IMPORTANT part!**

1. In Railway dashboard, click your **API service** (not MySQL)
2. Click **"Variables"** tab
3. Click **"New Variable"**
4. Add this **ONE variable**:
   - **Name:** `MYSQL_URL`
   - **Value:** `${{MySQL.MYSQL_URL}}`

**That's it!** Railway automatically fills in the connection details.

**Alternative (manual):** If `${{MySQL.MYSQL_URL}}` doesn't work, add these separately:
- `DB_HOST` = (copy from MySQL service "Connect" tab)
- `DB_NAME` = `railway`
- `DB_USER` = `root`
- `DB_PASSWORD` = (copy from MySQL service)

---

### 6. Configure Build Settings (if needed)

Railway should auto-detect, but if it doesn't:

1. Click your API service
2. Go to **"Settings"**
3. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn service_layer:app --host 0.0.0.0 --port $PORT`

---

### 7. Get Your Live URL

1. Click your API service
2. Go to **"Settings"** → **"Networking"**
3. Click **"Generate Domain"**
4. Railway gives you a URL like: `https://stock-tracker-production-xxxx.up.railway.app`

**That's your live API!** 🎉

---

### 8. Test Your Deployment

#### Test in Browser:
```
https://your-app-name.up.railway.app/health
https://your-app-name.up.railway.app/docs
```

#### Test with Python:
```python
import requests

API_URL = "https://your-app-name.up.railway.app"

# Health check
response = requests.get(f"{API_URL}/health")
print(response.json())

# Get all stocks
response = requests.get(f"{API_URL}/api/v1/stocks")
print(f"Found {response.json()['count']} stocks")
```

---

### 9. View Logs (Troubleshooting)

If something goes wrong:

1. Click your API service
2. Click **"Deployments"** tab
3. Click the latest deployment
4. Click **"View Logs"**

Look for:
- ✓ Database connection pool initialized
- ✓ Application startup complete

---

## Common Issues

### API won't start
**Check:** Did you set `MYSQL_URL` variable?
- Click API service → Variables
- Should see `MYSQL_URL = ${{MySQL.MYSQL_URL}}`

### Can't connect to database
**Check:** Is MySQL service running?
- Both services should show green status
- MySQL and API both need to be running

### "Table doesn't exist"
**Check:** Did you import schema?
- Go to MySQL → Data → Query
- Run: `SHOW TABLES;`
- Should see: Users, Stocks, Portfolios, Transactions, Watchlists

### Build fails
**Check logs:**
- Likely missing dependencies
- Make sure `requirements.txt` is in root folder
- Check Python version compatibility

---

## Cost

**Railway Free Tier:**
- $5 free credit per month
- ~500 hours of compute
- MySQL included
- **Good for 1 month of this project**

After free tier: ~$5-10/month (can delete when done with class)

---

## Screenshots for Submission

Take these screenshots:

1. **Railway Dashboard** showing both services running (green status)
2. **API Service Variables** showing `MYSQL_URL` configured
3. **Live API Docs** - Your URL + `/docs`
4. **Browser showing API response** - Any endpoint working
5. **Deployment logs** showing successful startup

---

## What to Submit

### In Your Code:

Update top of `service_layer.py` with:
```python
"""
LIVE DEPLOYMENT INFORMATION
===========================
Platform: Railway.app
Live URL: https://stock-tracker-production-xxxx.up.railway.app
API Docs: https://stock-tracker-production-xxxx.up.railway.app/docs

Deployment completed: [DATE]

This service is hosted on Railway.app with:
- MySQL database service (automatically managed)
- API service running FastAPI with uvicorn
- Environment variable MYSQL_URL for database connection
- Automatic HTTPS and domain generation

The service is live and accessible 24/7.
"""
```

### In Your README.md:

Add:
```markdown
## Live Deployment

**API URL:** https://stock-tracker-production-xxxx.up.railway.app
**API Documentation:** https://stock-tracker-production-xxxx.up.railway.app/docs

Platform: Railway.app
Database: MySQL (managed by Railway)
```

---

## Deployment Checklist

- [ ] Railway account created
- [ ] MySQL database provisioned
- [ ] Schema imported (62 rows total)
- [ ] API service deployed from GitHub
- [ ] `MYSQL_URL` environment variable set
- [ ] Domain generated
- [ ] API is accessible at live URL
- [ ] `/docs` endpoint works
- [ ] Tested at least one API call
- [ ] Screenshots taken
- [ ] Code comments updated with live URL
- [ ] README updated with deployment info

---

## Time Required

- Account setup: 2 minutes
- MySQL + schema import: 5 minutes
- API deployment: 5 minutes
- Testing: 3 minutes
- **Total: ~15 minutes**

---

## Need Help?

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **Check Logs:** Railway dashboard → Deployments → View Logs

**Remember:** The code is already updated to work with Railway's `MYSQL_URL` format automatically!
