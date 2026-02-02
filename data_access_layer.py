"""
Stock Portfolio Tracker - Data Access Layer (DAL)
This module provides CRUD operations for all database entities.

Requirements: pip install mysql-connector-python
Alternative: pip install psycopg2 (for PostgreSQL)
"""

import mysql.connector
from mysql.connector import Error, pooling
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from decimal import Decimal


class DatabaseConnection:
    """
    Singleton database connection manager with connection pooling.
    Handles database connections efficiently.
    """
    _connection_pool = None

    @classmethod
    def initialize_pool(cls, host='localhost', database='stock_tracker',
                       user='root', password='', pool_size=5):
        """Initialize the connection pool."""
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="stock_tracker_pool",
                pool_size=pool_size,
                host=host,
                database=database,
                user=user,
                password=password,
                autocommit=False
            )
            print(f"✓ Connection pool initialized successfully")
        except Error as e:
            print(f"✗ Error initializing connection pool: {e}")
            raise

    @classmethod
    def get_connection(cls):
        """Get a connection from the pool."""
        if cls._connection_pool is None:
            raise Exception("Connection pool not initialized. Call initialize_pool() first.")
        return cls._connection_pool.get_connection()


class UserDAO:
    """Data Access Object for Users table - Full CRUD operations."""

    @staticmethod
    def create(username: str, email: str, password_hash: str,
               first_name: str, last_name: str, account_balance: Decimal = Decimal('10000.00')) -> Optional[int]:
        """
        Create a new user.
        Returns: user_id if successful, None otherwise
        """
        query = """
            INSERT INTO Users (username, email, password_hash, first_name, last_name, account_balance)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (username, email, password_hash, first_name, last_name, account_balance))
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            print(f"✓ User created successfully with ID: {user_id}")
            return user_id
        except Error as e:
            print(f"✗ Error creating user: {e}")
            if conn:
                conn.rollback()
            return None

    @staticmethod
    def read_by_id(user_id: int) -> Optional[Dict]:
        """Read a user by ID."""
        query = "SELECT * FROM Users WHERE user_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Error as e:
            print(f"✗ Error reading user: {e}")
            return None

    @staticmethod
    def read_all() -> List[Dict]:
        """Read all users."""
        query = "SELECT * FROM Users ORDER BY created_at DESC"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return users
        except Error as e:
            print(f"✗ Error reading users: {e}")
            return []

    @staticmethod
    def update(user_id: int, **kwargs) -> bool:
        """
        Update user information.
        kwargs can include: username, email, first_name, last_name, account_balance
        """
        allowed_fields = ['username', 'email', 'first_name', 'last_name', 'account_balance', 'last_login']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_fields:
            print("✗ No valid fields to update")
            return False

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE Users SET {set_clause} WHERE user_id = %s"
        values = list(update_fields.values()) + [user_id]

        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ User {user_id} updated successfully")
                return True
            else:
                print(f"✗ No user found with ID {user_id}")
                return False
        except Error as e:
            print(f"✗ Error updating user: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def delete(user_id: int) -> bool:
        """Delete a user by ID (cascades to related records)."""
        query = "DELETE FROM Users WHERE user_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ User {user_id} deleted successfully")
                return True
            else:
                print(f"✗ No user found with ID {user_id}")
                return False
        except Error as e:
            print(f"✗ Error deleting user: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def find_by_username(username: str) -> Optional[Dict]:
        """Find a user by username."""
        query = "SELECT * FROM Users WHERE username = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Error as e:
            print(f"✗ Error finding user: {e}")
            return None


class StockDAO:
    """Data Access Object for Stocks table - Full CRUD operations."""

    @staticmethod
    def create(ticker_symbol: str, company_name: str, current_price: Decimal,
               market_cap: int, sector: str, industry: str = None) -> Optional[int]:
        """Create a new stock."""
        query = """
            INSERT INTO Stocks (ticker_symbol, company_name, current_price, market_cap, sector, industry)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (ticker_symbol.upper(), company_name, current_price,
                                 market_cap, sector, industry))
            conn.commit()
            stock_id = cursor.lastrowid
            cursor.close()
            conn.close()
            print(f"✓ Stock {ticker_symbol} created successfully with ID: {stock_id}")
            return stock_id
        except Error as e:
            print(f"✗ Error creating stock: {e}")
            if conn:
                conn.rollback()
            return None

    @staticmethod
    def read_by_id(stock_id: int) -> Optional[Dict]:
        """Read a stock by ID."""
        query = "SELECT * FROM Stocks WHERE stock_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (stock_id,))
            stock = cursor.fetchone()
            cursor.close()
            conn.close()
            return stock
        except Error as e:
            print(f"✗ Error reading stock: {e}")
            return None

    @staticmethod
    def read_all() -> List[Dict]:
        """Read all stocks."""
        query = "SELECT * FROM Stocks ORDER BY ticker_symbol"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            stocks = cursor.fetchall()
            cursor.close()
            conn.close()
            return stocks
        except Error as e:
            print(f"✗ Error reading stocks: {e}")
            return []

    @staticmethod
    def update(stock_id: int, **kwargs) -> bool:
        """Update stock information."""
        allowed_fields = ['ticker_symbol', 'company_name', 'current_price',
                         'market_cap', 'sector', 'industry']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_fields:
            print("✗ No valid fields to update")
            return False

        # Uppercase ticker symbol if present
        if 'ticker_symbol' in update_fields:
            update_fields['ticker_symbol'] = update_fields['ticker_symbol'].upper()

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE Stocks SET {set_clause} WHERE stock_id = %s"
        values = list(update_fields.values()) + [stock_id]

        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Stock {stock_id} updated successfully")
                return True
            else:
                print(f"✗ No stock found with ID {stock_id}")
                return False
        except Error as e:
            print(f"✗ Error updating stock: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def delete(stock_id: int) -> bool:
        """Delete a stock by ID."""
        query = "DELETE FROM Stocks WHERE stock_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (stock_id,))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Stock {stock_id} deleted successfully")
                return True
            else:
                print(f"✗ No stock found with ID {stock_id}")
                return False
        except Error as e:
            print(f"✗ Error deleting stock: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def find_by_ticker(ticker_symbol: str) -> Optional[Dict]:
        """Find a stock by ticker symbol."""
        query = "SELECT * FROM Stocks WHERE ticker_symbol = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (ticker_symbol.upper(),))
            stock = cursor.fetchone()
            cursor.close()
            conn.close()
            return stock
        except Error as e:
            print(f"✗ Error finding stock: {e}")
            return None

    @staticmethod
    def find_by_sector(sector: str) -> List[Dict]:
        """Find all stocks in a specific sector."""
        query = "SELECT * FROM Stocks WHERE sector = %s ORDER BY ticker_symbol"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (sector,))
            stocks = cursor.fetchall()
            cursor.close()
            conn.close()
            return stocks
        except Error as e:
            print(f"✗ Error finding stocks by sector: {e}")
            return []


class PortfolioDAO:
    """Data Access Object for Portfolios table - Full CRUD operations."""

    @staticmethod
    def create(user_id: int, portfolio_name: str, description: str = None,
               total_value: Decimal = Decimal('0.00')) -> Optional[int]:
        """Create a new portfolio."""
        query = """
            INSERT INTO Portfolios (user_id, portfolio_name, description, total_value)
            VALUES (%s, %s, %s, %s)
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (user_id, portfolio_name, description, total_value))
            conn.commit()
            portfolio_id = cursor.lastrowid
            cursor.close()
            conn.close()
            print(f"✓ Portfolio '{portfolio_name}' created successfully with ID: {portfolio_id}")
            return portfolio_id
        except Error as e:
            print(f"✗ Error creating portfolio: {e}")
            if conn:
                conn.rollback()
            return None

    @staticmethod
    def read_by_id(portfolio_id: int) -> Optional[Dict]:
        """Read a portfolio by ID."""
        query = "SELECT * FROM Portfolios WHERE portfolio_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (portfolio_id,))
            portfolio = cursor.fetchone()
            cursor.close()
            conn.close()
            return portfolio
        except Error as e:
            print(f"✗ Error reading portfolio: {e}")
            return None

    @staticmethod
    def read_all() -> List[Dict]:
        """Read all portfolios."""
        query = "SELECT * FROM Portfolios ORDER BY created_at DESC"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            portfolios = cursor.fetchall()
            cursor.close()
            conn.close()
            return portfolios
        except Error as e:
            print(f"✗ Error reading portfolios: {e}")
            return []

    @staticmethod
    def update(portfolio_id: int, **kwargs) -> bool:
        """Update portfolio information."""
        allowed_fields = ['portfolio_name', 'description', 'total_value', 'is_active']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_fields:
            print("✗ No valid fields to update")
            return False

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE Portfolios SET {set_clause} WHERE portfolio_id = %s"
        values = list(update_fields.values()) + [portfolio_id]

        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Portfolio {portfolio_id} updated successfully")
                return True
            else:
                print(f"✗ No portfolio found with ID {portfolio_id}")
                return False
        except Error as e:
            print(f"✗ Error updating portfolio: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def delete(portfolio_id: int) -> bool:
        """Delete a portfolio by ID."""
        query = "DELETE FROM Portfolios WHERE portfolio_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (portfolio_id,))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Portfolio {portfolio_id} deleted successfully")
                return True
            else:
                print(f"✗ No portfolio found with ID {portfolio_id}")
                return False
        except Error as e:
            print(f"✗ Error deleting portfolio: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def find_by_user(user_id: int) -> List[Dict]:
        """Find all portfolios for a specific user."""
        query = "SELECT * FROM Portfolios WHERE user_id = %s ORDER BY created_at DESC"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            portfolios = cursor.fetchall()
            cursor.close()
            conn.close()
            return portfolios
        except Error as e:
            print(f"✗ Error finding portfolios: {e}")
            return []


class TransactionDAO:
    """Data Access Object for Transactions table - Full CRUD operations."""

    @staticmethod
    def create(user_id: int, stock_id: int, portfolio_id: int, transaction_type: str,
               quantity: int, price_per_share: Decimal, notes: str = None) -> Optional[int]:
        """Create a new transaction."""
        total_amount = quantity * price_per_share
        query = """
            INSERT INTO Transactions
            (user_id, stock_id, portfolio_id, transaction_type, quantity, price_per_share, total_amount, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (user_id, stock_id, portfolio_id, transaction_type.upper(),
                                 quantity, price_per_share, total_amount, notes))
            conn.commit()
            transaction_id = cursor.lastrowid
            cursor.close()
            conn.close()
            print(f"✓ Transaction created successfully with ID: {transaction_id}")
            return transaction_id
        except Error as e:
            print(f"✗ Error creating transaction: {e}")
            if conn:
                conn.rollback()
            return None

    @staticmethod
    def read_by_id(transaction_id: int) -> Optional[Dict]:
        """Read a transaction by ID."""
        query = "SELECT * FROM Transactions WHERE transaction_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (transaction_id,))
            transaction = cursor.fetchone()
            cursor.close()
            conn.close()
            return transaction
        except Error as e:
            print(f"✗ Error reading transaction: {e}")
            return None

    @staticmethod
    def read_all() -> List[Dict]:
        """Read all transactions."""
        query = "SELECT * FROM Transactions ORDER BY transaction_date DESC"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            transactions = cursor.fetchall()
            cursor.close()
            conn.close()
            return transactions
        except Error as e:
            print(f"✗ Error reading transactions: {e}")
            return []

    @staticmethod
    def update(transaction_id: int, **kwargs) -> bool:
        """Update transaction information (limited fields for data integrity)."""
        allowed_fields = ['notes']  # Only notes should be editable
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_fields:
            print("✗ No valid fields to update (only notes can be modified)")
            return False

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE Transactions SET {set_clause} WHERE transaction_id = %s"
        values = list(update_fields.values()) + [transaction_id]

        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Transaction {transaction_id} updated successfully")
                return True
            else:
                print(f"✗ No transaction found with ID {transaction_id}")
                return False
        except Error as e:
            print(f"✗ Error updating transaction: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def delete(transaction_id: int) -> bool:
        """Delete a transaction by ID."""
        query = "DELETE FROM Transactions WHERE transaction_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (transaction_id,))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Transaction {transaction_id} deleted successfully")
                return True
            else:
                print(f"✗ No transaction found with ID {transaction_id}")
                return False
        except Error as e:
            print(f"✗ Error deleting transaction: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def find_by_user(user_id: int) -> List[Dict]:
        """Find all transactions for a specific user."""
        query = """
            SELECT t.*, s.ticker_symbol, s.company_name, p.portfolio_name
            FROM Transactions t
            JOIN Stocks s ON t.stock_id = s.stock_id
            JOIN Portfolios p ON t.portfolio_id = p.portfolio_id
            WHERE t.user_id = %s
            ORDER BY t.transaction_date DESC
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            transactions = cursor.fetchall()
            cursor.close()
            conn.close()
            return transactions
        except Error as e:
            print(f"✗ Error finding transactions: {e}")
            return []

    @staticmethod
    def find_by_stock(stock_id: int) -> List[Dict]:
        """Find all transactions for a specific stock."""
        query = """
            SELECT t.*, u.username, p.portfolio_name
            FROM Transactions t
            JOIN Users u ON t.user_id = u.user_id
            JOIN Portfolios p ON t.portfolio_id = p.portfolio_id
            WHERE t.stock_id = %s
            ORDER BY t.transaction_date DESC
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (stock_id,))
            transactions = cursor.fetchall()
            cursor.close()
            conn.close()
            return transactions
        except Error as e:
            print(f"✗ Error finding transactions: {e}")
            return []


class WatchlistDAO:
    """Data Access Object for Watchlists table - Full CRUD operations."""

    @staticmethod
    def create(user_id: int, stock_id: int, target_price: Decimal = None,
               notes: str = None, alert_enabled: bool = False) -> Optional[int]:
        """Add a stock to user's watchlist."""
        query = """
            INSERT INTO Watchlists (user_id, stock_id, target_price, notes, alert_enabled)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (user_id, stock_id, target_price, notes, alert_enabled))
            conn.commit()
            watchlist_id = cursor.lastrowid
            cursor.close()
            conn.close()
            print(f"✓ Stock added to watchlist with ID: {watchlist_id}")
            return watchlist_id
        except Error as e:
            print(f"✗ Error adding to watchlist: {e}")
            if conn:
                conn.rollback()
            return None

    @staticmethod
    def read_by_id(watchlist_id: int) -> Optional[Dict]:
        """Read a watchlist entry by ID."""
        query = "SELECT * FROM Watchlists WHERE watchlist_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (watchlist_id,))
            watchlist = cursor.fetchone()
            cursor.close()
            conn.close()
            return watchlist
        except Error as e:
            print(f"✗ Error reading watchlist: {e}")
            return None

    @staticmethod
    def read_all() -> List[Dict]:
        """Read all watchlist entries."""
        query = "SELECT * FROM Watchlists ORDER BY added_date DESC"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            watchlists = cursor.fetchall()
            cursor.close()
            conn.close()
            return watchlists
        except Error as e:
            print(f"✗ Error reading watchlists: {e}")
            return []

    @staticmethod
    def update(watchlist_id: int, **kwargs) -> bool:
        """Update watchlist entry."""
        allowed_fields = ['target_price', 'notes', 'alert_enabled']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_fields:
            print("✗ No valid fields to update")
            return False

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE Watchlists SET {set_clause} WHERE watchlist_id = %s"
        values = list(update_fields.values()) + [watchlist_id]

        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Watchlist entry {watchlist_id} updated successfully")
                return True
            else:
                print(f"✗ No watchlist entry found with ID {watchlist_id}")
                return False
        except Error as e:
            print(f"✗ Error updating watchlist: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def delete(watchlist_id: int) -> bool:
        """Delete a watchlist entry by ID."""
        query = "DELETE FROM Watchlists WHERE watchlist_id = %s"
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (watchlist_id,))
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()

            if affected_rows > 0:
                print(f"✓ Watchlist entry {watchlist_id} deleted successfully")
                return True
            else:
                print(f"✗ No watchlist entry found with ID {watchlist_id}")
                return False
        except Error as e:
            print(f"✗ Error deleting watchlist entry: {e}")
            if conn:
                conn.rollback()
            return False

    @staticmethod
    def find_by_user(user_id: int) -> List[Dict]:
        """Find all watchlist entries for a specific user."""
        query = """
            SELECT w.*, s.ticker_symbol, s.company_name, s.current_price, s.sector
            FROM Watchlists w
            JOIN Stocks s ON w.stock_id = s.stock_id
            WHERE w.user_id = %s
            ORDER BY w.added_date DESC
        """
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (user_id,))
            watchlist = cursor.fetchall()
            cursor.close()
            conn.close()
            return watchlist
        except Error as e:
            print(f"✗ Error finding watchlist: {e}")
            return []


# Example usage and testing
if __name__ == "__main__":
    # Initialize connection pool
    DatabaseConnection.initialize_pool(
        host='localhost',
        database='stock_tracker',
        user='root',
        password='your_password_here',
        pool_size=5
    )

    print("\n" + "="*50)
    print("Testing CRUD Operations")
    print("="*50)

    # Test User CRUD
    print("\n--- Testing UserDAO ---")
    users = UserDAO.read_all()
    print(f"Total users: {len(users)}")

    # Test Stock CRUD
    print("\n--- Testing StockDAO ---")
    stocks = StockDAO.read_all()
    print(f"Total stocks: {len(stocks)}")

    # Test finding stock by ticker
    apple = StockDAO.find_by_ticker('AAPL')
    if apple:
        print(f"Found: {apple['company_name']} - ${apple['current_price']}")

    print("\n" + "="*50)
    print("DAL Module Loaded Successfully")
    print("="*50)
