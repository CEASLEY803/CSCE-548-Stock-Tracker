# How to Import SQL Files into Railway MySQL

## Option 1: Railway Web Console (EASIEST)

### Step 1: Access MySQL Console
1. Go to your Railway project dashboard
2. Click on your **MySQL service**
3. Click the **"Data"** tab
4. Click **"Query"** button (SQL editor icon)

### Step 2: Copy and Paste Schema
1. Open your local `sql/schema.sql` file
2. Copy **ALL** the contents
3. Paste into Railway's query editor
4. Click **"Execute"** or press Ctrl+Enter

Wait for it to complete (you'll see success message)

### Step 3: Copy and Paste Data
1. Open your local `sql/populate_data.sql` file
2. Copy **ALL** the contents
3. Paste into Railway's query editor
4. Click **"Execute"** or press Ctrl+Enter

### Step 4: Verify
In the query editor, run:
```sql
SHOW TABLES;
```

You should see: Users, Stocks, Portfolios, Transactions, Watchlists

Then run:
```sql
SELECT COUNT(*) FROM Users;
SELECT COUNT(*) FROM Stocks;
```

Should show 10 users and 15 stocks.

---

## Option 2: MySQL Workbench (If Railway Console Doesn't Work)

### Step 1: Get Connection Details
1. In Railway, click your MySQL service
2. Click **"Connect"** tab
3. Copy these values:
   - **Host** (e.g., `containers-us-west-123.railway.app`)
   - **Port** (usually `6543` or similar)
   - **Database** (usually `railway`)
   - **Username** (usually `root`)
   - **Password** (click to reveal)

### Step 2: Download MySQL Workbench
- Go to https://dev.mysql.com/downloads/workbench/
- Download and install (free)

### Step 3: Connect to Railway
1. Open MySQL Workbench
2. Click **"+" next to "MySQL Connections"**
3. Fill in:
   - Connection Name: `Railway Stock Tracker`
   - Hostname: (paste from Railway)
   - Port: (paste from Railway)
   - Username: (paste from Railway)
4. Click **"Store in Keychain"** and enter password
5. Click **"Test Connection"**
6. If successful, click **"OK"**

### Step 4: Import Files
1. Double-click your new connection
2. Click **"File"** → **"Run SQL Script"**
3. Navigate to `sql/schema.sql`
4. Click **"Run"**
5. Wait for completion
6. Repeat for `sql/populate_data.sql`

### Step 5: Verify
Run this query:
```sql
SELECT 'Users' AS TableName, COUNT(*) AS RowCount FROM Users
UNION ALL SELECT 'Stocks', COUNT(*) FROM Stocks
UNION ALL SELECT 'Portfolios', COUNT(*) FROM Portfolios
UNION ALL SELECT 'Transactions', COUNT(*) FROM Transactions
UNION ALL SELECT 'Watchlists', COUNT(*) FROM Watchlists;
```

Should show 62 total rows.

---

## Option 3: Command Line (For Advanced Users)

### Step 1: Install MySQL Client
```powershell
# If not already installed
winget install Oracle.MySQL
```

### Step 2: Get Railway Connection String
1. In Railway, click MySQL service
2. Click **"Connect"** tab
3. Copy the **MySQL Command** (looks like this):
```
mysql -h containers-us-west-123.railway.app -u root -p railway --port=6543
```

### Step 3: Import Schema
```powershell
# Navigate to your project
cd "C:\Users\Butte\Documents\Stock_Tracker\CSCE-548-Stock-Tracker"

# Import schema (replace with your Railway connection details)
mysql -h YOUR_HOST -u root -pYOUR_PASSWORD railway --port=YOUR_PORT < sql/schema.sql

# Import data
mysql -h YOUR_HOST -u root -pYOUR_PASSWORD railway --port=YOUR_PORT < sql/populate_data.sql
```

**Note:** Replace YOUR_HOST, YOUR_PASSWORD, YOUR_PORT with values from Railway!

---

## Troubleshooting

### "Access Denied"
- Double-check password (copy-paste from Railway)
- Make sure you're using the correct username (usually `root`)

### "Unknown Database"
- Railway database might be named `railway` not `stock_tracker`
- Change line in `schema.sql`: comment out any `CREATE DATABASE` lines
- Or specify database in connection: `USE railway;` at top of schema.sql

### "Table already exists"
- Tables from previous import
- Fix: In Railway console, run `DROP DATABASE railway; CREATE DATABASE railway;`
- Then re-import

### Files too large / timeout
- Import schema first, then data
- Or break populate_data.sql into smaller chunks

---

## After Importing

### Update Your API Service

Railway will need to know the database credentials:

1. In Railway, go to your **API service** (not MySQL)
2. Click **"Variables"** tab
3. Add these variables:
   - `DB_HOST` = (from MySQL service "Connect" tab)
   - `DB_NAME` = `railway` (or whatever Railway uses)
   - `DB_USER` = `root`
   - `DB_PASSWORD` = (from MySQL service)
   - `DB_PORT` = (the port number)

4. Your API will automatically restart and connect!

---

## Quick Verification Script

After importing, test your Railway database with this Python script:

```python
# test_railway_db.py
import os
import mysql.connector

# Get Railway credentials from environment or paste here
config = {
    'host': 'YOUR_RAILWAY_HOST',
    'port': YOUR_PORT,
    'user': 'root',
    'password': 'YOUR_PASSWORD',
    'database': 'railway'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"✓ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")

    # Check row counts
    cursor.execute("""
        SELECT 'Users', COUNT(*) FROM Users
        UNION ALL SELECT 'Stocks', COUNT(*) FROM Stocks
        UNION ALL SELECT 'Portfolios', COUNT(*) FROM Portfolios
        UNION ALL SELECT 'Transactions', COUNT(*) FROM Transactions
        UNION ALL SELECT 'Watchlists', COUNT(*) FROM Watchlists
    """)

    print("\nRow Counts:")
    total = 0
    for name, count in cursor.fetchall():
        print(f"  {name}: {count}")
        total += count

    print(f"\n✓ Total: {total} rows")
    print("✓ Database import successful!")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"✗ Error: {e}")
```

Run with: `py test_railway_db.py`

---

## Alternative: Auto-Import on Startup

If Railway console is difficult, you can make your API auto-create tables on first run:

Add to `service_layer.py` startup:

```python
@app.on_event("startup")
async def startup_event():
    """Initialize database and import schema if needed."""
    try:
        DatabaseConnection.initialize_pool(...)

        # Check if tables exist
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # If no tables, import schema
        if len(tables) == 0:
            print("No tables found, importing schema...")
            with open('sql/schema.sql', 'r') as f:
                schema = f.read()
                for statement in schema.split(';'):
                    if statement.strip():
                        cursor.execute(statement)

            with open('sql/populate_data.sql', 'r') as f:
                data = f.read()
                for statement in data.split(';'):
                    if statement.strip():
                        cursor.execute(statement)

            conn.commit()
            print("✓ Schema and data imported!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ Error: {e}")
```

But **Option 1 (Railway Console) is recommended!**
