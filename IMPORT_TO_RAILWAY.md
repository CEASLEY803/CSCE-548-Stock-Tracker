# Import Database to Railway - Command Line Method

## ⚠️ Railway UI Note
The "Query" button is not available in the current Railway interface.
Use this command-line method instead.

---

## Step 1: Get Railway MySQL Connection Details

1. In Railway dashboard, click your **MySQL** service
2. Click **"Connect"** tab
3. You'll see connection details:

Copy these values (click the copy icon):
- **MYSQL_PUBLIC_URL** - or -
- **Host** (e.g., `containers-us-west-123.railway.app`)
- **Port** (e.g., `6543`)
- **Username** (usually `root`)
- **Password** (click to reveal)
- **Database** (usually `railway`)

---

## Step 2: Install MySQL Client (if not already installed)

### Check if you have it:
```powershell
mysql --version
```

### If not installed, use the full path from your existing installation:
```powershell
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --version
```

You already have MySQL installed from Project 1! ✅

---

## Step 3: Import Schema Using Command Line

### Method A: Using Full MySQL URL (Easiest)

Railway provides a full connection URL. Use it like this:

```powershell
# Navigate to your project
cd "C:\Users\Butte\Documents\Stock_Tracker\CSCE-548-Stock-Tracker"

# Import schema using the MYSQL_PUBLIC_URL from Railway
# Replace MYSQL_PUBLIC_URL with the actual URL from Railway
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h HOST -P PORT -u USERNAME -p DATABASE < sql\schema.sql
```

**Example with actual values:**
```powershell
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h containers-us-west-123.railway.app -P 6543 -u root -p railway < sql\schema.sql
```

When prompted, paste the password from Railway.

### Method B: All in One Command (No Password Prompt)

⚠️ **Warning:** This shows password in command history

```powershell
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h HOST -P PORT -u root -pYOUR_PASSWORD railway < sql\schema.sql
```

**Note:** No space between `-p` and the password!

---

## Step 4: Import Data

Same command, just with the data file:

```powershell
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h HOST -P PORT -u root -p railway < sql\populate_data.sql
```

Enter password when prompted.

---

## Step 5: Verify Import

Connect to Railway MySQL and check:

```powershell
# Connect to Railway MySQL
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h HOST -P PORT -u root -p railway
```

Once connected (you'll see `mysql>`), run:

```sql
SHOW TABLES;
```

You should see:
```
+--------------------+
| Tables_in_railway  |
+--------------------+
| Portfolios         |
| Stocks             |
| Transactions       |
| Users              |
| Watchlists         |
+--------------------+
```

Check row counts:
```sql
SELECT 'Users' AS TableName, COUNT(*) AS RowCount FROM Users
UNION ALL SELECT 'Stocks', COUNT(*) FROM Stocks
UNION ALL SELECT 'Portfolios', COUNT(*) FROM Portfolios
UNION ALL SELECT 'Transactions', COUNT(*) FROM Transactions
UNION ALL SELECT 'Watchlists', COUNT(*) FROM Watchlists;
```

Should show **62 total rows**.

Type `exit` to disconnect.

---

## Complete Example (Replace with YOUR Railway values)

```powershell
# 1. Navigate to project
cd "C:\Users\Butte\Documents\Stock_Tracker\CSCE-548-Stock-Tracker"

# 2. Set your Railway connection info as variables (easier)
$RAILWAY_HOST = "containers-us-west-123.railway.app"
$RAILWAY_PORT = "6543"
$RAILWAY_USER = "root"
$RAILWAY_PASS = "your-password-from-railway"
$RAILWAY_DB = "railway"

# 3. Import schema
& "C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h $RAILWAY_HOST -P $RAILWAY_PORT -u $RAILWAY_USER -p$RAILWAY_PASS $RAILWAY_DB < sql\schema.sql

# 4. Import data
& "C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h $RAILWAY_HOST -P $RAILWAY_PORT -u $RAILWAY_USER -p$RAILWAY_PASS $RAILWAY_DB < sql\populate_data.sql

# 5. Verify
& "C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h $RAILWAY_HOST -P $RAILWAY_PORT -u $RAILWAY_USER -p$RAILWAY_PASS $RAILWAY_DB -e "SHOW TABLES;"
```

---

## Troubleshooting

### "Can't connect to MySQL server"
- Check the host and port are correct from Railway
- Make sure Railway MySQL service is running (green in dashboard)
- Try adding `--protocol=TCP` flag

### "Access denied"
- Double-check password (copy-paste from Railway)
- Make sure using correct username (usually `root`)

### "Unknown database"
- Railway database might be named `railway` not `stock_tracker`
- Use whatever database name Railway shows

### Connection timeout
- Railway might have IP restrictions
- Try from Railway's web terminal instead (see below)

---

## Alternative: Railway CLI Method

If direct connection doesn't work, use Railway CLI:

### 1. Install Railway CLI:
```powershell
npm install -g @railway/cli
# Or use: iwr https://railway.app/install.ps1 | iex
```

### 2. Login:
```powershell
railway login
```

### 3. Link to your project:
```powershell
cd "C:\Users\Butte\Documents\Stock_Tracker\CSCE-548-Stock-Tracker"
railway link
```

### 4. Connect to MySQL:
```powershell
railway connect MySQL
```

This opens a MySQL shell connected to Railway!

### 5. Import files:
In the Railway MySQL shell:
```sql
source sql/schema.sql;
source sql/populate_data.sql;
SHOW TABLES;
```

---

## Quick Script for Windows

Save this as `import_to_railway.bat`:

```batch
@echo off
echo Railway Database Import Script
echo ================================
echo.

REM Set these from your Railway MySQL service
set MYSQL_HOST=containers-us-west-123.railway.app
set MYSQL_PORT=6543
set MYSQL_USER=root
set MYSQL_DB=railway

set /p MYSQL_PASS="Enter Railway MySQL Password: "

echo.
echo Importing schema...
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h %MYSQL_HOST% -P %MYSQL_PORT% -u %MYSQL_USER% -p%MYSQL_PASS% %MYSQL_DB% < sql\schema.sql

if errorlevel 1 (
    echo Error importing schema!
    pause
    exit /b 1
)

echo Schema imported successfully!
echo.
echo Importing data...
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h %MYSQL_HOST% -P %MYSQL_PORT% -u %MYSQL_USER% -p%MYSQL_PASS% %MYSQL_DB% < sql\populate_data.sql

if errorlevel 1 (
    echo Error importing data!
    pause
    exit /b 1
)

echo Data imported successfully!
echo.
echo Verifying...
"C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe" --protocol=TCP -h %MYSQL_HOST% -P %MYSQL_PORT% -u %MYSQL_USER% -p%MYSQL_PASS% %MYSQL_DB% -e "SHOW TABLES; SELECT COUNT(*) AS Users FROM Users; SELECT COUNT(*) AS Stocks FROM Stocks;"

echo.
echo ================================
echo Import Complete!
echo ================================
pause
```

Then just run:
```powershell
.\import_to_railway.bat
```

---

## Summary

Since Railway's UI doesn't have the Query button, use:

**Recommended:**
1. Get connection details from Railway
2. Use your local MySQL client (already installed)
3. Run: `mysql -h HOST -P PORT -u root -p railway < sql\schema.sql`
4. Repeat for `populate_data.sql`

**Or use Railway CLI** if you prefer:
1. `railway login`
2. `railway link`
3. `railway connect MySQL`
4. `source sql/schema.sql;`

Both methods work! Choose whichever is easier for you.
