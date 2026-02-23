"""
Stock Portfolio Tracker - Business Layer
Provides business logic and validation on top of the Data Access Layer.

This layer enforces business rules, validates data, and provides
higher-level operations for the service layer.
"""

from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Optional
import re

# Import Data Access Layer
from data_access_layer import (
    UserDAO,
    StockDAO,
    PortfolioDAO,
    TransactionDAO,
    WatchlistDAO
)


class BusinessRuleException(Exception):
    """Custom exception for business rule violations."""
    pass


class UserBusinessLogic:
    """Business logic for User operations."""

    @staticmethod
    def create_user(username: str, email: str, password: str,
                   first_name: str, last_name: str,
                   initial_balance: Decimal = Decimal('10000.00')) -> Dict:
        """
        Create a new user with validation.

        Business Rules:
        - Username must be alphanumeric and 3-50 characters
        - Email must be valid format
        - Password must be at least 8 characters
        - Initial balance must be >= 0
        """
        # Validate username
        if not username or len(username) < 3 or len(username) > 50:
            raise BusinessRuleException("Username must be 3-50 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise BusinessRuleException("Username must be alphanumeric")

        # Validate email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise BusinessRuleException("Invalid email format")

        # Validate password
        if len(password) < 8:
            raise BusinessRuleException("Password must be at least 8 characters")

        # Hash password (simple hash for demo - use bcrypt in production)
        password_hash = f"$2b$12${hash(password)}"

        # Validate balance
        if initial_balance < 0:
            raise BusinessRuleException("Initial balance cannot be negative")

        # Create user
        user_id = UserDAO.create(username, email, password_hash,
                                first_name, last_name, initial_balance)

        if user_id:
            return {
                'success': True,
                'user_id': user_id,
                'message': f'User {username} created successfully'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to create user - username or email may already exist'
            }

    @staticmethod
    def get_user(user_id: int) -> Optional[Dict]:
        """Get user by ID."""
        user = UserDAO.read_by_id(user_id)
        if user:
            # Remove sensitive data
            user.pop('password_hash', None)
            return user
        return None

    @staticmethod
    def get_all_users() -> List[Dict]:
        """Get all users (without passwords)."""
        users = UserDAO.read_all()
        for user in users:
            user.pop('password_hash', None)
        return users

    @staticmethod
    def update_user_balance(user_id: int, amount: Decimal, operation: str = 'add') -> Dict:
        """
        Update user account balance.

        Business Rules:
        - Balance cannot go negative
        - Amount must be positive
        """
        if amount <= 0:
            raise BusinessRuleException("Amount must be positive")

        user = UserDAO.read_by_id(user_id)
        if not user:
            raise BusinessRuleException(f"User {user_id} not found")

        current_balance = user['account_balance']

        if operation == 'add':
            new_balance = current_balance + amount
        elif operation == 'subtract':
            new_balance = current_balance - amount
            if new_balance < 0:
                raise BusinessRuleException("Insufficient funds")
        else:
            raise BusinessRuleException("Invalid operation. Use 'add' or 'subtract'")

        success = UserDAO.update(user_id, account_balance=new_balance)

        return {
            'success': success,
            'previous_balance': float(current_balance),
            'new_balance': float(new_balance),
            'message': f'Balance updated successfully'
        }

    @staticmethod
    def delete_user(user_id: int) -> Dict:
        """Delete a user."""
        success = UserDAO.delete(user_id)
        return {
            'success': success,
            'message': 'User deleted successfully' if success else 'User not found'
        }


class StockBusinessLogic:
    """Business logic for Stock operations."""

    @staticmethod
    def create_stock(ticker: str, company_name: str, current_price: Decimal,
                    market_cap: int, sector: str, industry: str = None) -> Dict:
        """
        Create a new stock with validation.

        Business Rules:
        - Ticker must be 1-10 uppercase letters
        - Price must be positive
        - Market cap must be positive
        """
        # Validate ticker
        ticker = ticker.upper().strip()
        if not re.match(r'^[A-Z]{1,10}$', ticker):
            raise BusinessRuleException("Ticker must be 1-10 uppercase letters")

        # Validate price
        if current_price <= 0:
            raise BusinessRuleException("Stock price must be positive")

        # Validate market cap
        if market_cap <= 0:
            raise BusinessRuleException("Market cap must be positive")

        stock_id = StockDAO.create(ticker, company_name, current_price,
                                  market_cap, sector, industry)

        if stock_id:
            return {
                'success': True,
                'stock_id': stock_id,
                'message': f'Stock {ticker} created successfully'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to create stock - ticker may already exist'
            }

    @staticmethod
    def get_stock(stock_id: int) -> Optional[Dict]:
        """Get stock by ID."""
        return StockDAO.read_by_id(stock_id)

    @staticmethod
    def get_all_stocks() -> List[Dict]:
        """Get all stocks."""
        return StockDAO.read_all()

    @staticmethod
    def search_stock_by_ticker(ticker: str) -> Optional[Dict]:
        """Search for a stock by ticker symbol."""
        return StockDAO.find_by_ticker(ticker.upper())

    @staticmethod
    def get_stocks_by_sector(sector: str) -> List[Dict]:
        """Get all stocks in a sector."""
        return StockDAO.find_by_sector(sector)

    @staticmethod
    def update_stock_price(stock_id: int, new_price: Decimal) -> Dict:
        """
        Update stock price.

        Business Rules:
        - Price must be positive
        - Price change > 20% triggers warning
        """
        if new_price <= 0:
            raise BusinessRuleException("Stock price must be positive")

        stock = StockDAO.read_by_id(stock_id)
        if not stock:
            raise BusinessRuleException(f"Stock {stock_id} not found")

        old_price = stock['current_price']
        price_change = abs(new_price - old_price) / old_price * 100

        success = StockDAO.update(stock_id, current_price=new_price)

        warning = None
        if price_change > 20:
            warning = f"Large price change detected: {price_change:.2f}%"

        return {
            'success': success,
            'old_price': float(old_price),
            'new_price': float(new_price),
            'price_change_percent': float(price_change),
            'warning': warning,
            'message': 'Stock price updated successfully'
        }

    @staticmethod
    def delete_stock(stock_id: int) -> Dict:
        """Delete a stock."""
        success = StockDAO.delete(stock_id)
        return {
            'success': success,
            'message': 'Stock deleted successfully' if success else 'Stock not found or has dependencies'
        }


class PortfolioBusinessLogic:
    """Business logic for Portfolio operations."""

    @staticmethod
    def create_portfolio(user_id: int, portfolio_name: str,
                        description: str = None) -> Dict:
        """
        Create a new portfolio.

        Business Rules:
        - User must exist
        - Portfolio name required
        - User can't have duplicate portfolio names
        """
        # Verify user exists
        user = UserDAO.read_by_id(user_id)
        if not user:
            raise BusinessRuleException(f"User {user_id} not found")

        # Validate portfolio name
        if not portfolio_name or len(portfolio_name.strip()) == 0:
            raise BusinessRuleException("Portfolio name is required")

        portfolio_id = PortfolioDAO.create(user_id, portfolio_name, description)

        if portfolio_id:
            return {
                'success': True,
                'portfolio_id': portfolio_id,
                'message': f'Portfolio "{portfolio_name}" created successfully'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to create portfolio - name may already exist for this user'
            }

    @staticmethod
    def get_portfolio(portfolio_id: int) -> Optional[Dict]:
        """Get portfolio by ID."""
        return PortfolioDAO.read_by_id(portfolio_id)

    @staticmethod
    def get_all_portfolios() -> List[Dict]:
        """Get all portfolios."""
        return PortfolioDAO.read_all()

    @staticmethod
    def get_user_portfolios(user_id: int) -> List[Dict]:
        """Get all portfolios for a user."""
        return PortfolioDAO.find_by_user(user_id)

    @staticmethod
    def update_portfolio_value(portfolio_id: int, new_value: Decimal) -> Dict:
        """Update portfolio total value."""
        if new_value < 0:
            raise BusinessRuleException("Portfolio value cannot be negative")

        success = PortfolioDAO.update(portfolio_id, total_value=new_value)

        return {
            'success': success,
            'new_value': float(new_value),
            'message': 'Portfolio value updated successfully'
        }

    @staticmethod
    def delete_portfolio(portfolio_id: int) -> Dict:
        """Delete a portfolio."""
        success = PortfolioDAO.delete(portfolio_id)
        return {
            'success': success,
            'message': 'Portfolio deleted successfully' if success else 'Portfolio not found'
        }


class TransactionBusinessLogic:
    """Business logic for Transaction operations."""

    @staticmethod
    def create_transaction(user_id: int, stock_id: int, portfolio_id: int,
                          transaction_type: str, quantity: int,
                          price_per_share: Decimal, notes: str = None) -> Dict:
        """
        Create a new transaction with comprehensive validation.

        Business Rules:
        - BUY: User must have sufficient balance
        - SELL: Portfolio must have sufficient shares (not enforced in this demo)
        - Quantity must be positive
        - Price must be positive
        """
        # Validate transaction type
        transaction_type = transaction_type.upper()
        if transaction_type not in ['BUY', 'SELL']:
            raise BusinessRuleException("Transaction type must be BUY or SELL")

        # Validate quantity and price
        if quantity <= 0:
            raise BusinessRuleException("Quantity must be positive")
        if price_per_share <= 0:
            raise BusinessRuleException("Price per share must be positive")

        # Verify entities exist
        user = UserDAO.read_by_id(user_id)
        if not user:
            raise BusinessRuleException(f"User {user_id} not found")

        stock = StockDAO.read_by_id(stock_id)
        if not stock:
            raise BusinessRuleException(f"Stock {stock_id} not found")

        portfolio = PortfolioDAO.read_by_id(portfolio_id)
        if not portfolio:
            raise BusinessRuleException(f"Portfolio {portfolio_id} not found")

        # Verify portfolio belongs to user
        if portfolio['user_id'] != user_id:
            raise BusinessRuleException("Portfolio does not belong to this user")

        # Calculate total
        total_amount = quantity * price_per_share

        # Business rule: Check user balance for BUY transactions
        if transaction_type == 'BUY':
            if user['account_balance'] < total_amount:
                raise BusinessRuleException(
                    f"Insufficient funds. Need ${total_amount:.2f}, have ${user['account_balance']:.2f}"
                )

        # Create transaction
        transaction_id = TransactionDAO.create(
            user_id, stock_id, portfolio_id, transaction_type,
            quantity, price_per_share, notes
        )

        if transaction_id:
            # Update user balance
            if transaction_type == 'BUY':
                UserDAO.update(user_id, account_balance=user['account_balance'] - total_amount)
            else:  # SELL
                UserDAO.update(user_id, account_balance=user['account_balance'] + total_amount)

            return {
                'success': True,
                'transaction_id': transaction_id,
                'total_amount': float(total_amount),
                'new_balance': float(user['account_balance'] + (total_amount if transaction_type == 'SELL' else -total_amount)),
                'message': f'{transaction_type} transaction created successfully'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to create transaction'
            }

    @staticmethod
    def get_transaction(transaction_id: int) -> Optional[Dict]:
        """Get transaction by ID."""
        return TransactionDAO.read_by_id(transaction_id)

    @staticmethod
    def get_all_transactions() -> List[Dict]:
        """Get all transactions."""
        return TransactionDAO.read_all()

    @staticmethod
    def get_user_transactions(user_id: int) -> List[Dict]:
        """Get all transactions for a user."""
        return TransactionDAO.find_by_user(user_id)

    @staticmethod
    def get_stock_transactions(stock_id: int) -> List[Dict]:
        """Get all transactions for a stock."""
        return TransactionDAO.find_by_stock(stock_id)

    @staticmethod
    def delete_transaction(transaction_id: int) -> Dict:
        """
        Delete a transaction.
        Note: In production, you'd reverse the balance changes
        """
        success = TransactionDAO.delete(transaction_id)
        return {
            'success': success,
            'message': 'Transaction deleted successfully' if success else 'Transaction not found'
        }


class WatchlistBusinessLogic:
    """Business logic for Watchlist operations."""

    @staticmethod
    def add_to_watchlist(user_id: int, stock_id: int, target_price: Decimal = None,
                        notes: str = None, alert_enabled: bool = False) -> Dict:
        """
        Add stock to user's watchlist.

        Business Rules:
        - User and stock must exist
        - Target price must be positive if provided
        - No duplicate entries
        """
        # Verify user and stock exist
        user = UserDAO.read_by_id(user_id)
        if not user:
            raise BusinessRuleException(f"User {user_id} not found")

        stock = StockDAO.read_by_id(stock_id)
        if not stock:
            raise BusinessRuleException(f"Stock {stock_id} not found")

        # Validate target price
        if target_price is not None and target_price <= 0:
            raise BusinessRuleException("Target price must be positive")

        watchlist_id = WatchlistDAO.create(user_id, stock_id, target_price, notes, alert_enabled)

        if watchlist_id:
            return {
                'success': True,
                'watchlist_id': watchlist_id,
                'message': f'Added {stock["ticker_symbol"]} to watchlist'
            }
        else:
            return {
                'success': False,
                'message': 'Failed to add to watchlist - may already be watching this stock'
            }

    @staticmethod
    def get_watchlist_item(watchlist_id: int) -> Optional[Dict]:
        """Get watchlist item by ID."""
        return WatchlistDAO.read_by_id(watchlist_id)

    @staticmethod
    def get_user_watchlist(user_id: int) -> List[Dict]:
        """Get user's complete watchlist."""
        return WatchlistDAO.find_by_user(user_id)

    @staticmethod
    def update_target_price(watchlist_id: int, target_price: Decimal) -> Dict:
        """Update target price for a watchlist item."""
        if target_price <= 0:
            raise BusinessRuleException("Target price must be positive")

        success = WatchlistDAO.update(watchlist_id, target_price=target_price)

        return {
            'success': success,
            'message': 'Target price updated successfully'
        }

    @staticmethod
    def remove_from_watchlist(watchlist_id: int) -> Dict:
        """Remove item from watchlist."""
        success = WatchlistDAO.delete(watchlist_id)
        return {
            'success': success,
            'message': 'Removed from watchlist' if success else 'Watchlist item not found'
        }

    @staticmethod
    def check_price_alerts(user_id: int) -> List[Dict]:
        """
        Check which watched stocks have reached their target price.

        Business Rule: Alert if current price <= target price
        """
        watchlist = WatchlistDAO.find_by_user(user_id)
        alerts = []

        for item in watchlist:
            if item['alert_enabled'] and item['target_price']:
                if item['current_price'] <= item['target_price']:
                    alerts.append({
                        'ticker': item['ticker_symbol'],
                        'company': item['company_name'],
                        'current_price': float(item['current_price']),
                        'target_price': float(item['target_price']),
                        'message': f"{item['ticker_symbol']} has reached target price!"
                    })

        return alerts


# Example usage and testing
if __name__ == "__main__":
    from data_access_layer import DatabaseConnection

    # Initialize database connection
    DatabaseConnection.initialize_pool(
        host='localhost',
        database='stock_tracker',
        user='root',
        password='Stock2024!',
        pool_size=5
    )

    print("=" * 60)
    print("Business Layer - Testing")
    print("=" * 60)

    # Test getting all stocks
    print("\n--- Get All Stocks ---")
    stocks = StockBusinessLogic.get_all_stocks()
    print(f"Found {len(stocks)} stocks")

    # Test getting user
    print("\n--- Get User ---")
    user = UserBusinessLogic.get_user(1)
    if user:
        print(f"User: {user['username']}, Balance: ${user['account_balance']}")

    print("\n" + "=" * 60)
    print("Business Layer Module Loaded Successfully")
    print("=" * 60)
