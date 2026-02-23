"""
Stock Portfolio Tracker - API Client (Console Application)
This client calls the REST API service layer to perform operations.

IMPORTANT: The service_layer.py server must be running before using this client!
Start server with: uvicorn service_layer:app --reload

This demonstrates the complete architecture:
Console Client → REST API → Business Layer → Data Access Layer → Database
"""

import requests
import sys
from tabulate import tabulate
from decimal import Decimal


class StockTrackerAPIClient:
    """Client for interacting with Stock Portfolio Tracker REST API."""

    def __init__(self, base_url="http://localhost:8000"):
        """
        Initialize API client.

        Args:
            base_url: Base URL of the API server (default: http://localhost:8000)
        """
        self.base_url = base_url
        self.api_v1 = f"{base_url}/api/v1"

    def check_connection(self):
        """Check if API server is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    # ==================== User Operations ====================

    def get_all_users(self):
        """Get all users from API."""
        response = requests.get(f"{self.api_v1}/users")
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id):
        """Get specific user."""
        response = requests.get(f"{self.api_v1}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, username, email, password, first_name, last_name, initial_balance=10000.00):
        """Create a new user."""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "initial_balance": initial_balance
        }
        response = requests.post(f"{self.api_v1}/users", json=data)
        response.raise_for_status()
        return response.json()

    def update_user_balance(self, user_id, amount, operation="add"):
        """Update user balance."""
        data = {
            "amount": amount,
            "operation": operation
        }
        response = requests.put(f"{self.api_v1}/users/{user_id}/balance", json=data)
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id):
        """Delete a user."""
        response = requests.delete(f"{self.api_v1}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    # ==================== Stock Operations ====================

    def get_all_stocks(self):
        """Get all stocks from API."""
        response = requests.get(f"{self.api_v1}/stocks")
        response.raise_for_status()
        return response.json()

    def get_stock(self, stock_id):
        """Get specific stock."""
        response = requests.get(f"{self.api_v1}/stocks/{stock_id}")
        response.raise_for_status()
        return response.json()

    def search_stock_by_ticker(self, ticker):
        """Search stock by ticker symbol."""
        response = requests.get(f"{self.api_v1}/stocks/ticker/{ticker}")
        response.raise_for_status()
        return response.json()

    def get_stocks_by_sector(self, sector):
        """Get stocks in a specific sector."""
        response = requests.get(f"{self.api_v1}/stocks/sector/{sector}")
        response.raise_for_status()
        return response.json()

    def create_stock(self, ticker, company_name, current_price, market_cap, sector, industry=None):
        """Create a new stock."""
        data = {
            "ticker_symbol": ticker,
            "company_name": company_name,
            "current_price": current_price,
            "market_cap": market_cap,
            "sector": sector,
            "industry": industry
        }
        response = requests.post(f"{self.api_v1}/stocks", json=data)
        response.raise_for_status()
        return response.json()

    def update_stock_price(self, stock_id, new_price):
        """Update stock price."""
        data = {"new_price": new_price}
        response = requests.put(f"{self.api_v1}/stocks/{stock_id}/price", json=data)
        response.raise_for_status()
        return response.json()

    def delete_stock(self, stock_id):
        """Delete a stock."""
        response = requests.delete(f"{self.api_v1}/stocks/{stock_id}")
        response.raise_for_status()
        return response.json()

    # ==================== Portfolio Operations ====================

    def get_all_portfolios(self):
        """Get all portfolios."""
        response = requests.get(f"{self.api_v1}/portfolios")
        response.raise_for_status()
        return response.json()

    def get_portfolio(self, portfolio_id):
        """Get specific portfolio."""
        response = requests.get(f"{self.api_v1}/portfolios/{portfolio_id}")
        response.raise_for_status()
        return response.json()

    def get_user_portfolios(self, user_id):
        """Get all portfolios for a user."""
        response = requests.get(f"{self.api_v1}/users/{user_id}/portfolios")
        response.raise_for_status()
        return response.json()

    def create_portfolio(self, user_id, portfolio_name, description=None):
        """Create a new portfolio."""
        data = {
            "user_id": user_id,
            "portfolio_name": portfolio_name,
            "description": description
        }
        response = requests.post(f"{self.api_v1}/portfolios", json=data)
        response.raise_for_status()
        return response.json()

    def delete_portfolio(self, portfolio_id):
        """Delete a portfolio."""
        response = requests.delete(f"{self.api_v1}/portfolios/{portfolio_id}")
        response.raise_for_status()
        return response.json()

    # ==================== Transaction Operations ====================

    def get_all_transactions(self):
        """Get all transactions."""
        response = requests.get(f"{self.api_v1}/transactions")
        response.raise_for_status()
        return response.json()

    def get_user_transactions(self, user_id):
        """Get all transactions for a user."""
        response = requests.get(f"{self.api_v1}/users/{user_id}/transactions")
        response.raise_for_status()
        return response.json()

    def create_transaction(self, user_id, stock_id, portfolio_id, transaction_type, quantity, price_per_share, notes=None):
        """Create a new transaction."""
        data = {
            "user_id": user_id,
            "stock_id": stock_id,
            "portfolio_id": portfolio_id,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "price_per_share": price_per_share,
            "notes": notes
        }
        response = requests.post(f"{self.api_v1}/transactions", json=data)
        response.raise_for_status()
        return response.json()

    def delete_transaction(self, transaction_id):
        """Delete a transaction."""
        response = requests.delete(f"{self.api_v1}/transactions/{transaction_id}")
        response.raise_for_status()
        return response.json()

    # ==================== Watchlist Operations ====================

    def get_user_watchlist(self, user_id):
        """Get user's watchlist."""
        response = requests.get(f"{self.api_v1}/users/{user_id}/watchlist")
        response.raise_for_status()
        return response.json()

    def add_to_watchlist(self, user_id, stock_id, target_price=None, notes=None, alert_enabled=False):
        """Add stock to watchlist."""
        data = {
            "user_id": user_id,
            "stock_id": stock_id,
            "target_price": target_price,
            "notes": notes,
            "alert_enabled": alert_enabled
        }
        response = requests.post(f"{self.api_v1}/watchlist", json=data)
        response.raise_for_status()
        return response.json()

    def check_price_alerts(self, user_id):
        """Check for price alerts."""
        response = requests.get(f"{self.api_v1}/users/{user_id}/watchlist/alerts")
        response.raise_for_status()
        return response.json()


class APIClientConsole:
    """Interactive console interface for the API client."""

    def __init__(self):
        self.client = StockTrackerAPIClient()
        self.running = True

    def display_header(self):
        """Display application header."""
        print("=" * 70)
        print(" " * 15 + "STOCK PORTFOLIO TRACKER")
        print(" " * 18 + "API Client Console")
        print(" " * 18 + "(Service Layer v2.0)")
        print("=" * 70)

    def display_menu(self):
        """Display main menu."""
        print("\n" + "-" * 70)
        print("MAIN MENU - API Client")
        print("-" * 70)
        print("1.  View All Stocks (via API)")
        print("2.  View User Transactions (via API)")
        print("3.  View User Portfolios (via API)")
        print("4.  Search Stock by Ticker (via API)")
        print("5.  Test Full CRUD Operations")
        print("6.  View All Users (via API)")
        print("0.  Exit")
        print("-" * 70)

    def view_all_stocks(self):
        """Display all stocks via API."""
        print("\n" + "=" * 70)
        print(" " * 20 + "ALL STOCKS (via REST API)")
        print("=" * 70 + "\n")

        try:
            result = self.client.get_all_stocks()
            stocks = result.get('stocks', [])

            if not stocks:
                print("No stocks found.")
                return

            headers = ["ID", "Ticker", "Company", "Price", "Sector"]
            table_data = []

            for stock in stocks:
                table_data.append([
                    stock['stock_id'],
                    stock['ticker_symbol'],
                    stock['company_name'][:30],
                    f"${stock['current_price']:.2f}",
                    stock['sector']
                ])

            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print(f"\nTotal Stocks: {result.get('count', 0)}")
            print("✓ Data retrieved via REST API")

        except requests.exceptions.RequestException as e:
            print(f"✗ API Error: {e}")

    def view_user_transactions(self):
        """Display user transactions via API."""
        print("\n" + "=" * 70)
        print(" " * 18 + "USER TRANSACTIONS (via REST API)")
        print("=" * 70 + "\n")

        try:
            user_id = int(input("Enter User ID: "))

            result = self.client.get_user_transactions(user_id)
            transactions = result.get('transactions', [])

            if not transactions:
                print("No transactions found for this user.")
                return

            headers = ["ID", "Type", "Ticker", "Qty", "Price", "Total"]
            table_data = []

            for txn in transactions:
                table_data.append([
                    txn['transaction_id'],
                    txn['transaction_type'],
                    txn['ticker_symbol'],
                    txn['quantity'],
                    f"${txn['price_per_share']:.2f}",
                    f"${txn['total_amount']:.2f}"
                ])

            print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
            print(f"\nTotal Transactions: {result.get('count', 0)}")
            print("✓ Data retrieved via REST API")

        except ValueError:
            print("Invalid User ID")
        except requests.exceptions.RequestException as e:
            print(f"✗ API Error: {e}")

    def test_full_crud(self):
        """Test complete CRUD cycle via API."""
        print("\n" + "=" * 70)
        print(" " * 15 + "TESTING FULL CRUD OPERATIONS")
        print(" " * 20 + "(via REST API)")
        print("=" * 70 + "\n")

        try:
            # CREATE
            print("Step 1: CREATE - Adding new stock...")
            create_result = self.client.create_stock(
                ticker="TEST",
                company_name="Test Company Inc.",
                current_price=100.50,
                market_cap=5000000000,
                sector="Technology",
                industry="Software"
            )
            print(f"✓ Created: {create_result}")
            stock_id = create_result.get('stock_id')

            input("\nPress Enter to continue to READ...")

            # READ
            print("\nStep 2: READ - Fetching the stock...")
            stock = self.client.get_stock(stock_id)
            print(f"✓ Retrieved: {stock['ticker_symbol']} - {stock['company_name']}")
            print(f"  Current Price: ${stock['current_price']}")

            input("\nPress Enter to continue to UPDATE...")

            # UPDATE
            print("\nStep 3: UPDATE - Updating stock price...")
            update_result = self.client.update_stock_price(stock_id, 105.75)
            print(f"✓ Updated: Price changed from ${update_result['old_price']} to ${update_result['new_price']}")

            input("\nPress Enter to continue to DELETE...")

            # DELETE
            print("\nStep 4: DELETE - Removing the stock...")
            delete_result = self.client.delete_stock(stock_id)
            print(f"✓ Deleted: {delete_result['message']}")

            print("\n" + "=" * 70)
            print("CRUD TEST COMPLETED SUCCESSFULLY!")
            print("All operations were performed via REST API")
            print("=" * 70)

        except requests.exceptions.RequestException as e:
            print(f"\n✗ API Error: {e}")
            if hasattr(e.response, 'text'):
                print(f"Details: {e.response.text}")

    def run(self):
        """Run the main application loop."""
        self.display_header()

        # Check API connection
        print("\nChecking API server connection...")
        if not self.client.check_connection():
            print("✗ Cannot connect to API server!")
            print("\nPlease start the server first:")
            print("  py -m uvicorn service_layer:app --reload")
            print("\nThen run this client again.")
            return

        print("✓ Connected to API server at http://localhost:8000")
        print("✓ API Documentation: http://localhost:8000/docs")

        while self.running:
            self.display_menu()

            try:
                choice = input("\nEnter your choice: ").strip()

                if choice == '1':
                    self.view_all_stocks()
                elif choice == '2':
                    self.view_user_transactions()
                elif choice == '3':
                    try:
                        user_id = int(input("Enter User ID: "))
                        result = self.client.get_user_portfolios(user_id)
                        print(f"\n{result}")
                        print("✓ Data retrieved via REST API")
                    except (ValueError, requests.exceptions.RequestException) as e:
                        print(f"Error: {e}")
                elif choice == '4':
                    ticker = input("Enter Ticker Symbol: ").upper()
                    try:
                        stock = self.client.search_stock_by_ticker(ticker)
                        print(f"\n{stock}")
                        print("✓ Data retrieved via REST API")
                    except requests.exceptions.RequestException as e:
                        print(f"Stock not found: {e}")
                elif choice == '5':
                    self.test_full_crud()
                elif choice == '6':
                    result = self.client.get_all_users()
                    print(f"\nFound {result.get('count', 0)} users")
                    print("✓ Data retrieved via REST API")
                elif choice == '0':
                    print("\n" + "=" * 70)
                    print(" " * 20 + "Thank you for using")
                    print(" " * 15 + "Stock Portfolio Tracker API Client!")
                    print("=" * 70 + "\n")
                    self.running = False
                else:
                    print("\n✗ Invalid choice")

                if self.running:
                    input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.running = False
            except Exception as e:
                print(f"\n✗ Error: {e}")
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    app = APIClientConsole()
    app.run()


if __name__ == "__main__":
    main()
