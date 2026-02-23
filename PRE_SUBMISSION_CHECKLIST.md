# Pre-Submission Checklist - Project 2

## ✅ CRITICAL ITEMS TO VERIFY

### 1. Project 1 Integration ✓ CONFIRMED
- [x] **business_layer.py** imports from **data_access_layer.py** (Project 1)
- [x] **service_layer.py** imports from **business_layer.py**
- [x] Data flows: API → Business → DAL → Database
- [x] **YOUR Project 1 code is being used**

**Verified:** The actual DAO classes from Project 1 are in use!

---

### 2. Cloud Hosting ⚠️ ACTION REQUIRED

**Problem:** Project currently only runs on localhost!

**What the rubric says:**
> "Host those services using a platform of your choosing... This step will take some time to configure and test."

**This means:** Professor likely wants REAL cloud deployment, not just Docker/localhost!

#### **Action Required:**

**Choose ONE platform and deploy:**

1. **Railway.app** (RECOMMENDED - 15 mins)
   - Free tier, no credit card
   - MySQL included
   - See: [CLOUD_HOSTING_GUIDE.md](CLOUD_HOSTING_GUIDE.md)

2. **Render.com** (Good alternative)
   - Free tier available
   - Requires PostgreSQL conversion

3. **PythonAnywhere** (Simplest)
   - Completely free
   - MySQL included

#### **After Deployment:**

- [ ] Get live URL (e.g., `https://stock-tracker.railway.app`)
- [ ] Verify API docs work (URL + `/docs`)
- [ ] Test CRUD operations on live server
- [ ] Take screenshots of live deployment

#### **Update Code Comments:**

Add to top of `service_layer.py`:
```python
"""
LIVE DEPLOYMENT INFORMATION
===========================
Platform: Railway.app
API URL: https://stock-tracker-api-production.up.railway.app
API Docs: https://stock-tracker-api-production.up.railway.app/docs

Deployment Steps Taken:
1. Created Railway account
2. Deployed MySQL database service
3. Connected GitHub repository
4. Configured environment variables (DB_HOST, DB_USER, DB_PASSWORD)
5. Deployed API service
6. Imported database schema

Service is live and accessible 24/7 at the above URL.
"""
```

---

### 3. Business Layer Requirements ✅ DONE

- [x] All CRUD operations from DAL available through business layer
- [x] Business rules implemented:
  - [x] Username validation
  - [x] Email format checking
  - [x] Password strength requirements
  - [x] Price validation (positive numbers)
  - [x] Balance checking for BUY transactions
  - [x] Portfolio ownership verification
  - [x] Price change warnings

---

### 4. Service Layer Requirements ✅ DONE

- [x] All business layer methods exposed as HTTP endpoints
- [x] REST API implemented (FastAPI)
- [x] 30+ endpoints created
- [x] Automatic documentation (`/docs`)
- [x] Error handling with proper HTTP status codes
- [x] Request/Response validation

---

### 5. Testing Requirements ✅ DONE

- [x] Console client that calls API (not direct database)
- [x] Demonstrates full CRUD cycle:
  - [x] CREATE operation
  - [x] READ operation
  - [x] UPDATE operation
  - [x] DELETE operation

**Two ways to test:**
1. `py api_client.py` → Option 5
2. `py test_crud_operations.py` (automated)

---

### 6. Screenshots Required

#### **For Submission:**

- [ ] **API Documentation** - http://localhost:8000/docs (or cloud URL)
- [ ] **CRUD Test Results** - Run `test_crud_operations.py`
- [ ] **CREATE Step** - From api_client or test
- [ ] **READ Step** - Showing data retrieval
- [ ] **UPDATE Step** - Showing data modification
- [ ] **DELETE Step** - Showing data removal
- [ ] **Cloud Deployment** (if deployed):
  - [ ] Live API URL in browser
  - [ ] Cloud platform dashboard
  - [ ] Successful API call to cloud service

---

### 7. GitHub Repository

- [ ] All code pushed to GitHub
- [ ] README.md updated with:
  - [ ] Project 2 description
  - [ ] How to run locally
  - [ ] **Live API URL (if cloud deployed)**
  - [ ] API documentation link
- [ ] Clean commit history
- [ ] No sensitive data (passwords, API keys)

---

### 8. Code Comments

- [x] `service_layer.py` has hosting instructions
- [ ] **UPDATE with actual cloud platform used**
- [ ] **UPDATE with live URL**
- [x] Business layer has business rule explanations
- [x] All major functions documented

---

### 9. Graduate Students Only

If doing graduate credit, also complete:

- [ ] **Overview Document** including:
  - [ ] AI prompts used to generate code
  - [ ] What changes you made to generated output
  - [ ] Analysis of AI tool effectiveness
  - [ ] What AI missed or got wrong
  - [ ] Additional business rules you coded yourself
  - [ ] Detailed hosting/deployment steps taken

---

## Quick Test Before Submission

### Test 1: Local Server
```powershell
# Start server
.\start_api_server.bat

# Should see:
# ✓ Database connection pool initialized
# Uvicorn running on http://0.0.0.0:8000

# Open browser: http://localhost:8000/docs
# Should see Swagger UI with all endpoints
```

### Test 2: CRUD Operations
```powershell
# In new terminal
py test_crud_operations.py

# Should see:
# ✓ PASS: Server Connection
# ✓ PASS: CREATE Stock
# ✓ PASS: READ Stock by ID
# ✓ PASS: UPDATE Stock Price
# ✓ PASS: DELETE Stock
# Success Rate: 100%
```

### Test 3: API Client
```powershell
py api_client.py

# Select option 5
# Should successfully:
# 1. CREATE new stock
# 2. READ the stock
# 3. UPDATE stock price
# 4. DELETE the stock
```

### Test 4: Cloud Deployment (if deployed)
```python
import requests

# Replace with YOUR live URL
response = requests.get("https://your-app.railway.app/api/v1/stocks")
print(response.json())  # Should return stock data
```

---

## Common Issues

### "Cannot connect to API server"
- **Fix:** Make sure server is running (`.\start_api_server.bat`)

### "Access denied for user 'root'"
- **Fix:** Check MySQL is running and password is correct

### "Module not found: business_layer"
- **Fix:** Make sure all .py files are in same directory

### Cloud deployment fails
- **Fix:** Check [CLOUD_HOSTING_GUIDE.md](CLOUD_HOSTING_GUIDE.md)
- Try a different platform if one doesn't work

---

## Submission Checklist

Before submitting:

- [ ] ✅ Project 1 DAL is integrated and working
- [ ] ⚠️ **Services are hosted on cloud platform** (not just localhost!)
- [ ] ✅ Business layer has all CRUD operations
- [ ] ✅ Service layer exposes all business methods
- [ ] ✅ Console client calls API (not database)
- [ ] ✅ Full CRUD cycle demonstrated
- [ ] Screenshots taken and combined into PDF
- [ ] GitHub repo is public and accessible
- [ ] Code has comments about hosting platform
- [ ] README updated with live URL
- [ ] (Grad students) Overview document written

---

## Time Estimate

- **If deploying to cloud:** Add 30-60 minutes
- **Total for cloud setup:** 15-30 minutes (Railway)
- **Screenshots:** 15 minutes
- **Documentation updates:** 10 minutes

**Don't skip the cloud deployment!** The rubric specifically mentions hosting and says it "will take some time to configure and test."

---

## Need Help?

1. Read [CLOUD_HOSTING_GUIDE.md](CLOUD_HOSTING_GUIDE.md)
2. Railway.app has great docs: https://docs.railway.app
3. Test locally first to make sure everything works
4. Then deploy to cloud

**Remember:** Localhost/Docker is NOT cloud hosting!
