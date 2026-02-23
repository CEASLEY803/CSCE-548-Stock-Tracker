# Cloud Hosting Guide - Stock Portfolio Tracker API

## ⚠️ IMPORTANT: Professor likely wants CLOUD hosting, not just localhost!

This guide shows you how to deploy your REST API to a real cloud platform.

---

## Option 1: Railway.app (RECOMMENDED - Easiest with Database)

**Why Railway:**
- ✅ Free tier available
- ✅ Supports MySQL
- ✅ Easy GitHub integration
- ✅ Automatic HTTPS
- ✅ No credit card required for trial

### Steps:

1. **Sign up at Railway.app**
   - Go to https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy MySQL"
   - Note the connection details

3. **Update Database Connection**
   - Railway will give you MySQL credentials
   - Update `service_layer.py` startup to use environment variables:

```python
import os

@app.on_event("startup")
async def startup_event():
    DatabaseConnection.initialize_pool(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'stock_tracker'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'Stock2024!'),
        pool_size=10
    )
```

4. **Deploy API Service**
   - In Railway, click "New Service" → "GitHub Repo"
   - Connect your GitHub repo
   - Railway will auto-detect Python and deploy

5. **Set Environment Variables**
   In Railway dashboard, add:
   - `DB_HOST` = (from MySQL service)
   - `DB_USER` = (from MySQL service)
   - `DB_PASSWORD` = (from MySQL service)
   - `DB_NAME` = stock_tracker

6. **Import Database**
   - Use Railway's MySQL console
   - Run your `schema.sql` and `populate_data.sql`

7. **Access Your API**
   - Railway gives you a URL like: `https://stock-tracker-api-production.up.railway.app`
   - API Docs: `https://your-url.railway.app/docs`

**Cost:** FREE for 500 hours/month

---

## Option 2: Render.com (Good Alternative)

**Why Render:**
- ✅ Free tier
- ✅ Easy deployment
- ✅ Good documentation

### Steps:

1. **Sign up at Render.com**
   - Go to https://render.com
   - Sign in with GitHub

2. **Create PostgreSQL Database** (Free tier)
   - Click "New +" → "PostgreSQL"
   - Note the connection string
   - **Note:** You'll need to convert from MySQL to PostgreSQL

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn service_layer:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Same as Railway (DB_HOST, DB_USER, etc.)

**Cost:** FREE

---

## Option 3: PythonAnywhere (Simplest - Keep MySQL Local)

**Why PythonAnywhere:**
- ✅ Completely free tier
- ✅ MySQL included
- ✅ No credit card needed
- ✅ Simple setup

### Steps:

1. **Sign up at PythonAnywhere.com**
   - Create free account

2. **Upload Your Code**
   - Use "Files" tab to upload all .py files

3. **Create MySQL Database**
   - "Databases" tab → Create MySQL database
   - Import schema.sql and populate_data.sql

4. **Configure Web App**
   - "Web" tab → "Add new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set WSGI file to use uvicorn

5. **Access**
   - Your URL: `https://yourusername.pythonanywhere.com`

**Cost:** FREE (with limitations)

---

## Option 4: Heroku (Classic Choice)

**Requires credit card** (for verification, still free tier)

### Setup Files Already Created:

Create `Procfile`:
```
web: uvicorn service_layer:app --host 0.0.0.0 --port $PORT
```

Create `runtime.txt`:
```
python-3.11.0
```

### Deploy:
```bash
heroku create stock-tracker-api
heroku addons:create cleardb:ignite  # Free MySQL
git push heroku main
```

**Cost:** FREE with credit card on file

---

## What to Include in Your Submission

### For Any Platform You Choose:

1. **Live API URL**
   - Include in README
   - Example: `https://stock-tracker-api.railway.app`

2. **API Documentation URL**
   - Your URL + `/docs`
   - Example: `https://stock-tracker-api.railway.app/docs`

3. **Screenshots:**
   - Screenshot of live API docs (showing your cloud URL)
   - Screenshot of successful API call to cloud service
   - Screenshot of deployment dashboard

4. **Comments in Code:**
   Add to top of `service_layer.py`:
   ```python
   """
   HOSTING PLATFORM: Railway.app
   LIVE API URL: https://stock-tracker-api-production.up.railway.app
   API DOCS: https://stock-tracker-api-production.up.railway.app/docs

   Deployment Steps:
   1. Signed up at Railway.app
   2. Created MySQL database service
   3. Deployed API service from GitHub
   4. Configured environment variables
   5. Imported database schema

   The service is accessible 24/7 at the URL above.
   """
   ```

---

## My Recommendation

**For this assignment:** Use **Railway.app**

**Reasons:**
1. Free tier is generous
2. MySQL support built-in
3. GitHub integration (easy updates)
4. Automatic HTTPS
5. No credit card required
6. Takes ~15 minutes to set up

**Alternative if Railway doesn't work:** PythonAnywhere (simpler but more limited)

---

## Testing Your Cloud Deployment

Once deployed, test with:

```python
import requests

# Replace with your cloud URL
API_URL = "https://your-app.railway.app"

# Test health endpoint
response = requests.get(f"{API_URL}/health")
print(response.json())

# Test getting stocks
response = requests.get(f"{API_URL}/api/v1/stocks")
print(f"Found {response.json()['count']} stocks")
```

---

## Need Help?

Each platform has good docs:
- Railway: https://docs.railway.app
- Render: https://render.com/docs
- PythonAnywhere: https://help.pythonanywhere.com
- Heroku: https://devcenter.heroku.com

---

## What If You Run Out of Time?

**Minimum acceptable:**
1. Document that you ATTEMPTED cloud deployment
2. Show screenshots of trying
3. Have localhost working perfectly
4. Explain what blocked you

But seriously, try Railway.app first - it's designed for this!
