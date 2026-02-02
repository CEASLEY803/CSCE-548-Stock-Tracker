# Stock Portfolio Tracker

A comprehensive database-driven stock portfolio tracking system with a Python Data Access Layer and interactive console interface.

## Project Overview

This project demonstrates professional database design and implementation for a stock portfolio tracking system. It includes:

- **Robust SQL Schema**: 5 normalized tables with 6 foreign key relationships
- **Data Validation**: Comprehensive constraints ensuring data integrity
- **Python DAL**: Full CRUD operations for all entities
- **Console UI**: Interactive menu-driven interface for database operations
- **Test Data**: 62 rows of realistic stock market data

## Database Architecture

### Tables (5)

1. **Users**: User account information with balance tracking
2. **Stocks**: Stock information including ticker, price, and market data
3. **Portfolios**: User portfolios with value tracking
4. **Transactions**: Buy/sell transaction records
5. **Watchlists**: Stocks users are monitoring

### Foreign Key Relationships (6)

1. `Portfolios.user_id` → `Users.user_id`
2. `Transactions.user_id` → `Users.user_id`
3. `Transactions.stock_id` → `Stocks.stock_id`
4. `Transactions.portfolio_id` → `Portfolios.portfolio_id`
5. `Watchlists.user_id` → `Users.user_id`
6. `Watchlists.stock_id` → `Stocks.stock_id`

### Data Validation Constraints

- Stock prices must be positive (CHECK constraint)
- Account balances cannot be negative
- Email format validation
- Ticker symbols must be uppercase
- Unique constraints on username and email
- Transaction quantities must be positive

## Project Structure

```
CSCE-548-Stock-Tracker/
├── sql/
│   ├── schema.sql              # Database schema (5 tables)
│   └── populate_data.sql       # Test data (62 rows)
├── scripts/
│   ├── setup_database.bat      # Windows database setup script
│   └── create_pdf.py           # Screenshot PDF generator
├── docs/
│   └── Stock_Tracker_Screenshots.pdf  # Project screenshots
├── data_access_layer.py        # Python DAL with CRUD operations
├── console_frontend.py         # Interactive console UI
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0+ or MariaDB 10.5+
- pip (Python package installer)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Setup MySQL Database

1. **Start MySQL Server**

```bash
# Windows
net start MySQL80

# Linux/Mac
sudo systemctl start mysql
```

2. **Create Database**

```bash
mysql -u root -p
```

```sql
CREATE DATABASE stock_tracker;
USE stock_tracker;
```

3. **Import Schema**

```bash
mysql -u root -p stock_tracker < schema.sql
```

4. **Populate Test Data**

```bash
mysql -u root -p stock_tracker < populate_data.sql
```

### Step 3: Verify Installation

```sql
-- Check row counts
SELECT 'Users' AS TableName, COUNT(*) AS RowCount FROM Users
UNION ALL SELECT 'Stocks', COUNT(*) FROM Stocks
UNION ALL SELECT 'Portfolios', COUNT(*) FROM Portfolios
UNION ALL SELECT 'Transactions', COUNT(*) FROM Transactions
UNION ALL SELECT 'Watchlists', COUNT(*) FROM Watchlists;
```

Expected output: 62 total rows (10 + 15 + 12 + 15 + 10)

## Usage

### Running the Console Application

```bash
python console_frontend.py
```

### Console Features

1. **View All Stocks**: Display all stocks with prices and market data
2. **View User Transactions**: See transaction history for any user
3. **View User Portfolios**: Display portfolios and their values
4. **View User Watchlist**: Show stocks a user is monitoring
5. **Search by Ticker**: Find specific stocks quickly
6. **View by Sector**: Browse stocks by market sector
7. **Create Transaction**: Add new buy/sell transactions
8. **Add to Watchlist**: Monitor stocks of interest

### Sample Console Session

```
=============================================
           STOCK PORTFOLIO TRACKER
              Console Application
=============================================

Database Host (default: localhost): localhost
Database Name (default: stock_tracker): stock_tracker
Database User (default: root): root
Database Password: ****

✓ Database connection established!

MAIN MENU
---------------------------------------------
1.  View All Stocks
2.  View User Transactions
3.  View User Portfolios
...

Enter your choice: 1

=============================================
                   ALL STOCKS
=============================================

+----+--------+----------------------+----------+-----------+--------------+
| ID | Ticker | Company              | Price    | Market Cap| Sector       |
+----+--------+----------------------+----------+-----------+--------------+
| 1  | AAPL   | Apple Inc.           | $178.25  | $2,800... | Technology   |
| 2  | MSFT   | Microsoft Corp.      | $425.50  | $3,200... | Technology   |
...
```

## Python Data Access Layer (DAL)

### Architecture

The DAL provides a clean separation between business logic and database operations using the DAO (Data Access Object) pattern.

### Classes

- **DatabaseConnection**: Singleton connection pool manager
- **UserDAO**: User CRUD operations
- **StockDAO**: Stock CRUD operations
- **PortfolioDAO**: Portfolio CRUD operations
- **TransactionDAO**: Transaction CRUD operations
- **WatchlistDAO**: Watchlist CRUD operations

### CRUD Operations Example

```python
from data_access_layer import DatabaseConnection, StockDAO, UserDAO
from decimal import Decimal

# Initialize connection pool
DatabaseConnection.initialize_pool(
    host='localhost',
    database='stock_tracker',
    user='root',
    password='your_password'
)

# READ: Get all stocks
stocks = StockDAO.read_all()
for stock in stocks:
    print(f"{stock['ticker_symbol']}: ${stock['current_price']}")

# READ: Find specific stock
apple = StockDAO.find_by_ticker('AAPL')
print(f"Apple: ${apple['current_price']}")

# CREATE: Add new stock
new_id = StockDAO.create(
    ticker_symbol='TSLA',
    company_name='Tesla Inc.',
    current_price=Decimal('250.00'),
    market_cap=800000000000,
    sector='Consumer Cyclical',
    industry='Auto Manufacturers'
)

# UPDATE: Update stock price
StockDAO.update(new_id, current_price=Decimal('255.00'))

# DELETE: Remove stock
StockDAO.delete(new_id)

# Complex Query: Get user transactions
transactions = TransactionDAO.find_by_user(user_id=1)
for txn in transactions:
    print(f"{txn['transaction_type']}: {txn['ticker_symbol']} "
          f"x{txn['quantity']} @ ${txn['price_per_share']}")
```

## Database Schema Details

### Users Table
- Primary Key: `user_id`
- Unique: `username`, `email`
- Validation: email format, positive balance

### Stocks Table
- Primary Key: `stock_id`
- Unique: `ticker_symbol`
- Validation: positive price, uppercase ticker

### Portfolios Table
- Primary Key: `portfolio_id`
- Foreign Key: `user_id` → Users
- Unique: (user_id, portfolio_name)

### Transactions Table
- Primary Key: `transaction_id`
- Foreign Keys: `user_id` → Users, `stock_id` → Stocks, `portfolio_id` → Portfolios
- Validation: positive quantity, positive price

### Watchlists Table
- Primary Key: `watchlist_id`
- Foreign Keys: `user_id` → Users, `stock_id` → Stocks
- Unique: (user_id, stock_id)

## Test Data Overview

The database includes 62 rows of realistic test data:

- **10 Users**: Various investors with different account balances
- **15 Stocks**: Major companies (AAPL, MSFT, GOOGL, TSLA, etc.)
- **12 Portfolios**: Diverse investment strategies
- **15 Transactions**: Buy/sell activities across portfolios
- **10 Watchlist Entries**: Stocks being monitored

## Advanced Features

### Connection Pooling
The DAL uses MySQL connection pooling for efficient database access:
- Pool size: 5 connections
- Automatic connection management
- Thread-safe operations

### Data Integrity
- Foreign key constraints with CASCADE/RESTRICT
- CHECK constraints for data validation
- Unique constraints preventing duplicates
- Transaction support with rollback

### Error Handling
- Comprehensive error messages
- Transaction rollback on failures
- Input validation before database operations

## Alternative: PostgreSQL Support

To use PostgreSQL instead of MySQL:

1. Install psycopg2:
```bash
pip install psycopg2-binary
```

2. Modify [schema.sql](schema.sql):
- Change `AUTO_INCREMENT` to `SERIAL`
- Change `ENUM` to `CHECK` constraints
- Adjust `ON UPDATE CURRENT_TIMESTAMP` syntax

3. Update [data_access_layer.py](data_access_layer.py):
```python
import psycopg2
from psycopg2 import pool

# Update DatabaseConnection class for PostgreSQL
```

## Troubleshooting

### Connection Issues
```
Error: Can't connect to MySQL server
Solution: Verify MySQL is running and credentials are correct
```

### Import Errors
```
Error: No module named 'mysql.connector'
Solution: pip install mysql-connector-python
```

### Schema Errors
```
Error: Table already exists
Solution: DROP existing tables before importing schema
```

## Future Enhancements

- RESTful API using Flask/FastAPI
- Web-based dashboard with real-time charts
- Integration with live stock market APIs
- Advanced portfolio analytics and reporting
- User authentication and authorization
- Stock price alerts and notifications
- Multi-currency support
- Export to CSV/Excel functionality

## License

This project is for educational purposes (CSCE-548 course).

## Author

Database Architecture & Implementation for CSCE-548 Stock Tracker Project