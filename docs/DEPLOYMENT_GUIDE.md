# Stock Portfolio Tracker - Deployment Guide

**Project:** CSCE 548 - Complete N-Tier Application
**Author:** [Your Name]
**Last Updated:** March 15, 2026
**GitHub Repository:** https://github.com/CEASLEY803/CSCE-548-Stock-Tracker

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Local Development Setup](#local-development-setup)
5. [Production Deployment](#production-deployment)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)
8. [AI Tool Documentation](#ai-tool-documentation)

---

## Overview

This is a complete **4-tier stock portfolio tracking application** built using AI assistance (Claude Code). The application demonstrates full CRUD operations across all layers.

**Live Deployments:**
- **Web Client:** https://ceasley803.github.io/CSCE-548-Stock-Tracker/web_client/
- **REST API:** https://csce-548-stock-tracker-production.up.railway.app
- **API Documentation:** https://csce-548-stock-tracker-production.up.railway.app/docs
- **Database:** Railway MySQL (Private)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER (Tier 1)                    │
│  web_client/index.html + app.js                             │
│  Hosted on: GitHub Pages                                    │
│  Technologies: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5  │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/REST API Calls
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER (Tier 2)                   │
│  service_layer.py                                           │
│  Hosted on: Railway.app                                     │
│  Technologies: FastAPI, Python 3.11+, Uvicorn               │
└────────────────────┬────────────────────────────────────────┘
                     │ Function Calls
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LAYER (Tier 3)                   │
│  business_layer.py                                          │
│  Technologies: Python 3.11+, Business Logic Classes         │
└────────────────────┬────────────────────────────────────────┘
                     │ DAO Method Calls
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER (Tier 4)                     │
│  data_access_layer.py                                       │
│  Technologies: Python 3.11+, mysql-connector-python         │
└────────────────────┬────────────────────────────────────────┘
                     │ SQL Queries
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                        DATABASE                             │
│  MySQL 8.0+                                                 │
│  Hosted on: Railway.app                                     │
│  5 Tables: Users, Stocks, Portfolios, Transactions,         │
│            Watchlists                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

### **Required Software:**

1. **Git** (2.30+)
   - Download: https://git-scm.com/downloads
   - Verify: `git --version`

2. **Python** (3.11+)
   - Download: https://www.python.org/downloads/
   - Verify: `python --version` or `py --version`

3. **pip** (Python package manager)
   - Included with Python
   - Verify: `pip --version`

4. **Text Editor / IDE**
   - VSCode (recommended): https://code.visualstudio.com/
   - Or any code editor

5. **Web Browser**
   - Chrome, Firefox, Edge, or Safari

### **Optional Software (for local database):**

6. **MySQL Server** (8.0+)
   - Download: https://dev.mysql.com/downloads/mysql/
   - Only needed if running database locally

7. **MySQL Workbench** (for database management)
   - Download: https://dev.mysql.com/downloads/workbench/
   - Useful for viewing database records

### **Accounts Needed for Deployment:**

8. **GitHub Account**
   - Sign up: https://github.com/join

9. **Railway Account** (for hosting API + Database)
   - Sign up: https://railway.app/
   - Free tier available

---

## Local Development Setup

Follow these steps to run the complete application on your local machine.

### **Step 1: Clone the Repository**

```bash
# Open terminal/command prompt
cd C:\Users\YourName\Documents  # or your preferred location

# Clone the repository
git clone https://github.com/CEASLEY803/CSCE-548-Stock-Tracker.git

# Navigate into the project
cd CSCE-548-Stock-Tracker
```

### **Step 2: Install Python Dependencies**

```bash
# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `mysql-connector-python` - MySQL database driver
- `python-dotenv` - Environment variable management

### **Step 3: Set Up Database**

#### **Option A: Use Railway (Cloud) Database** (Recommended)

The application is already configured to use the deployed Railway database. No setup needed!

#### **Option B: Set Up Local MySQL Database**

If you want to run your own local MySQL instance:

1. **Install and start MySQL Server**

2. **Create the database:**
   ```bash
   mysql -u root -p
   ```

3. **Run these commands in MySQL:**
   ```sql
   CREATE DATABASE stock_tracker;
   USE stock_tracker;
   SOURCE sql/schema.sql;
   SOURCE sql/populate_data.sql;
   ```

4. **Update connection in `data_access_layer.py`:**
   ```python
   # Find the DatabaseConnection class
   # Update with your local credentials:
   MYSQL_HOST = 'localhost'
   MYSQL_PORT = 3306
   MYSQL_USER = 'root'
   MYSQL_PASSWORD = 'your_password'
   MYSQL_DATABASE = 'stock_tracker'
   ```

### **Step 4: Run the API Server Locally**

```bash
# Start the FastAPI server
uvicorn service_layer:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify it works:**
- Open browser: http://localhost:8000
- View API docs: http://localhost:8000/docs
- Test health check: http://localhost:8000/health

### **Step 5: Run the Web Client Locally**

#### **Option A: Simple File Open**
```bash
# Windows
start web_client\index.html

# Mac/Linux
open web_client/index.html
```

#### **Option B: Local Web Server** (Recommended)
```bash
# Using Python's built-in web server
cd web_client
python -m http.server 8080
```

Then open: http://localhost:8080

**Important:** If running locally, you need to update the API URL in `web_client/app.js`:
```javascript
// Change this line:
const API_BASE_URL = 'https://csce-548-stock-tracker-production.up.railway.app';

// To this:
const API_BASE_URL = 'http://localhost:8000';
```

### **Step 6: Test Locally**

1. Open web client in browser
2. Verify "Connected" status badge shows green
3. Test CRUD operations:
   - Click "Add New Stock" - Create a stock
   - Click pencil icon - Update stock price
   - Click eye icon - View stock details
   - Click trash icon - Delete stock

---

## Production Deployment

### **Backend Deployment (Railway.app)**

#### **Step 1: Create Railway Account**
1. Go to https://railway.app
2. Click "Start a New Project"
3. Login with GitHub

#### **Step 2: Deploy MySQL Database**
1. Click "New Project"
2. Select "Provision MySQL"
3. Wait for database to be created
4. Note the connection details (available in "Variables" tab)

#### **Step 3: Import Database Schema**
1. Click on MySQL service
2. Click "Data" tab
3. Click "Query"
4. Copy and paste contents of `sql/schema.sql`
5. Click "Execute"
6. Repeat for `sql/populate_data.sql`

**Verify:**
- Run: `SELECT COUNT(*) FROM Stocks;` - Should show 15+ rows

#### **Step 4: Deploy API Service**
1. In Railway, click "New Service"
2. Select "GitHub Repo"
3. Choose your forked repository
4. Railway will auto-detect Python

#### **Step 5: Configure Environment Variables**
1. Click on the API service
2. Go to "Variables" tab
3. Add variable:
   ```
   MYSQL_URL = ${{MySQL.MYSQL_URL}}
   ```
   (Railway will automatically link to your MySQL service)

#### **Step 6: Configure Build Settings**
1. Go to "Settings" tab
2. Set "Start Command":
   ```
   uvicorn service_layer:app --host 0.0.0.0 --port $PORT
   ```
3. Railway will automatically deploy on every git push

#### **Step 7: Generate Public URL**
1. Go to "Settings" tab
2. Scroll to "Networking"
3. Click "Generate Domain"
4. Save your API URL (e.g., `https://your-app.up.railway.app`)

**Verify deployment:**
- Visit: `https://your-app.up.railway.app/health`
- Visit: `https://your-app.up.railway.app/docs`

### **Frontend Deployment (GitHub Pages)**

#### **Step 1: Update API URL**
1. Edit `web_client/app.js`
2. Change `API_BASE_URL` to your Railway URL:
   ```javascript
   const API_BASE_URL = 'https://your-app.up.railway.app';
   ```
3. Commit and push changes

#### **Step 2: Enable GitHub Pages**
1. Go to your GitHub repository
2. Click "Settings" tab
3. Scroll to "Pages" section
4. Under "Source":
   - Select branch: `main`
   - Select folder: `/ (root)`
5. Click "Save"

#### **Step 3: Wait for Deployment**
- GitHub will automatically deploy
- Takes 1-2 minutes
- You'll see a green checkmark when done

#### **Step 4: Get Your URL**
- Your site will be at: `https://yourusername.github.io/CSCE-548-Stock-Tracker/web_client/`

**Verify deployment:**
- Open the URL in browser
- Check that "Connected" badge is green
- Test all CRUD operations

---

## Testing

### **Health Check Tests**

```bash
# Test API health
curl https://your-app.up.railway.app/health

# Expected response:
{"status": "healthy", "database": "connected"}
```

### **API Endpoint Tests**

```bash
# Get all stocks
curl https://your-app.up.railway.app/api/v1/stocks

# Get single stock
curl https://your-app.up.railway.app/api/v1/stocks/1

# Create stock (POST)
curl -X POST https://your-app.up.railway.app/api/v1/stocks \
  -H "Content-Type: application/json" \
  -d '{
    "ticker_symbol": "TEST",
    "company_name": "Test Company",
    "current_price": 100.50,
    "market_cap": 1000000000,
    "sector": "Technology",
    "industry": "Software"
  }'
```

### **Database Tests**

Connect to Railway MySQL and run:

```sql
-- Verify all tables exist
SHOW TABLES;

-- Count records in each table
SELECT 'Stocks' as table_name, COUNT(*) as count FROM Stocks
UNION ALL
SELECT 'Users', COUNT(*) FROM Users
UNION ALL
SELECT 'Portfolios', COUNT(*) FROM Portfolios
UNION ALL
SELECT 'Transactions', COUNT(*) FROM Transactions
UNION ALL
SELECT 'Watchlists', COUNT(*) FROM Watchlists;

-- Test a CREATE operation
INSERT INTO Stocks (ticker_symbol, company_name, current_price, market_cap, sector)
VALUES ('TEST', 'Test Corp', 50.00, 5000000000, 'Technology');

-- Verify it was created
SELECT * FROM Stocks WHERE ticker_symbol = 'TEST';

-- Test an UPDATE operation
UPDATE Stocks SET current_price = 55.00 WHERE ticker_symbol = 'TEST';

-- Test a DELETE operation
DELETE FROM Stocks WHERE ticker_symbol = 'TEST';
```

---

## Troubleshooting

### **Problem: API shows "Connection Failed"**

**Solutions:**
1. Check Railway service is running (green status)
2. Verify Railway public domain is active
3. Check CORS is enabled in `service_layer.py`
4. Verify `API_BASE_URL` in `app.js` matches Railway URL

### **Problem: Database connection errors**

**Solutions:**
1. Verify `MYSQL_URL` environment variable is set in Railway
2. Check MySQL service is running in Railway
3. Test database connection:
   ```python
   python -c "from data_access_layer import DatabaseConnection; print(DatabaseConnection.test_connection())"
   ```

### **Problem: CRUD operations fail**

**Solutions:**
1. Open browser DevTools (F12)
2. Check Console tab for JavaScript errors
3. Check Network tab for failed API requests
4. Verify API documentation shows correct endpoints: `/docs`

### **Problem: GitHub Pages shows 404**

**Solutions:**
1. Wait 2-3 minutes after enabling Pages
2. Verify branch and folder settings are correct
3. Check that `index.html` exists in specified folder
4. Force refresh: Ctrl + Shift + R

### **Problem: Local development port already in use**

**Solutions:**
```bash
# Use a different port
uvicorn service_layer:app --reload --port 8001

# Or kill the process using the port (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## AI Tool Documentation

### **AI Tool Used:** Claude Code (Anthropic Sonnet 4.5)

### **Prompts Used:**

#### **Project 1: Data Layer**
```
Create a Python data access layer for a stock portfolio tracker with:
- 5 MySQL tables (Users, Stocks, Portfolios, Transactions, Watchlists)
- DAO pattern with full CRUD operations
- Connection pooling
- Error handling and validation
```

#### **Project 2: Business & Service Layers**
```
Create a business layer and REST API service layer for the stock portfolio tracker:
- Business layer with validation and business rules
- FastAPI service layer exposing all business methods as REST endpoints
- Full CRUD operations
- Proper error handling and HTTP status codes
- API documentation with Swagger/OpenAPI
```

#### **Project 3: Web Client**
```
Create a web client that consumes the REST API:
- All GET methods for all 5 tables
- Professional UI with Bootstrap 5
- Search and filter functionality
- Responsive design
```

#### **Project 4: Complete CRUD**
```
Implement full CRUD operations in the web client:
- CREATE (POST) modals with forms for all 5 entities
- UPDATE (PUT) functionality for stocks and users
- DELETE operations with confirmation
- Form validation and error handling
- Success/error feedback messages
```

### **Changes Made to AI-Generated Code:**

1. **CORS Configuration** (service_layer.py)
   - AI didn't initially include CORS middleware
   - Added manually to allow GitHub Pages to access Railway API

2. **Watchlist GET All Endpoint** (service_layer.py)
   - AI initially had watchlist GET only by user ID
   - Added `GET /api/v1/watchlist` endpoint for all records

3. **CREATE/UPDATE Implementation** (app.js)
   - AI initially generated stubs for CREATE/UPDATE functions
   - Required explicit prompt to implement full modal forms

4. **Environment Variable Handling** (data_access_layer.py)
   - Updated to use Railway's `MYSQL_URL` environment variable
   - AI had hardcoded connection strings

### **AI Tool Effectiveness:**

| Aspect | Rating | Notes |
|--------|--------|-------|
| Code Generation Speed | 10/10 | Generated 2000+ lines in minutes |
| Code Quality | 9/10 | Professional, clean, well-structured |
| Completeness | 8/10 | Required explicit prompts for some features |
| Error Handling | 10/10 | Comprehensive try/catch blocks |
| Best Practices | 10/10 | Modern patterns, async/await, type hints |
| Documentation | 9/10 | Good comments, could be more detailed |
| **Overall** | **9.2/10** | Highly effective tool |

**Time Savings:** Estimated 85-90% reduction in development time compared to manual coding.

**Recommendation:** Highly recommended for rapid prototyping and CRUD applications.

---

## Success Indicators

Your deployment is successful if:

- ✅ API health endpoint returns `{"status": "healthy"}`
- ✅ API docs are accessible at `/docs`
- ✅ Web client shows green "Connected" badge
- ✅ Can create, read, update, and delete records via web client
- ✅ Database shows corresponding changes
- ✅ No console errors in browser DevTools

---

## Additional Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Railway Documentation:** https://docs.railway.app/
- **GitHub Pages Documentation:** https://docs.github.com/en/pages
- **MySQL Documentation:** https://dev.mysql.com/doc/
- **Bootstrap 5 Documentation:** https://getbootstrap.com/docs/5.3/

---

## Support & Contact

- **GitHub Issues:** https://github.com/CEASLEY803/CSCE-548-Stock-Tracker/issues
- **Course:** CSCE 548
- **Instructor:** [Instructor Name]

---

**Last Updated:** March 15, 2026
**Version:** 4.0 (Complete N-Tier Application)
