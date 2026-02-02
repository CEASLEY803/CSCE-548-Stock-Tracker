"""
Stock Portfolio Tracker - Console-Based Front End
Interactive command-line interface for database operations.

Requirements: pip install mysql-connector-python tabulate
"""

import sys
from decimal import Decimal
from datetime import datetime
from tabulate import tabulate
from data_access_layer import (
    DatabaseConnection,
    UserDAO,
    StockDAO,
    PortfolioDAO,
    TransactionDAO,
    WatchlistDAO
)


class StockTrackerConsole:
    """Main console application for Stock Portfolio Tracker."""

    def __init__(self):
        """Initialize the console application."""
        self.current_user_id = None
        self.running = True

    def clear_screen(self):
        """Clear the console screen."""
        print("\n" * 2)

    def display_header(self):
        """Display application header."""
        print("=" * 70)
        print(" " * 15 + "STOCK PORTFOLIO TRACKER")
        print(" " * 20 + "Console Application")
        print("=" * 70)

    def display_menu(self):
        """Display main menu options."""
        print("\n" + "-" * 70)
        print("MAIN MENU")
        print("-" * 70)
        print("1.  View All Stocks")
        print("2.  View User Transactions")
        print("3.  View User Portfolios")
        print("4.  View User Watchlist")
        print("5.  Search Stock by Ticker")
        print("6.  View Stocks by Sector")
        print("7.  View All Users")
        print("8.  View Stock Details")
        print("9.  Create New Transaction")
        print("10. Add Stock to Watchlist")
        print("0.  Exit")
        print("-" * 70)

    def view_all_stocks(self):
        """Display all stocks in a formatted table."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 25 + "ALL STOCKS")
        print("=" * 70 + "\n")

        stocks = StockDAO.read_all()

        if not stocks:
            print("No stocks found in the database.")
            return

        # Prepare data for tabulation
        headers = ["ID", "Ticker", "Company", "Price", "Market Cap", "Sector"]
        table_data = []

        for stock in stocks:
            market_cap = f"${stock['market_cap']:,}" if stock['market_cap'] else "N/A"
            table_data.append([
                stock['stock_id'],
                stock['ticker_symbol'],
                stock['company_name'][:30],  # Truncate long names
                f"${stock['current_price']:.2f}",
                market_cap,
                stock['sector']
            ])

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal Stocks: {len(stocks)}")

    def view_user_transactions(self):
        """Display transactions for a specific user."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 22 + "USER TRANSACTIONS")
        print("=" * 70 + "\n")

        # Get user ID
        try:
            user_id = int(input("Enter User ID (or 0 to cancel): "))
            if user_id == 0:
                return
        except ValueError:
            print("Invalid User ID. Please enter a number.")
            return

        # Verify user exists
        user = UserDAO.read_by_id(user_id)
        if not user:
            print(f"No user found with ID {user_id}")
            return

        print(f"\nTransactions for: {user['first_name']} {user['last_name']} (@{user['username']})")
        print("-" * 70)

        transactions = TransactionDAO.find_by_user(user_id)

        if not transactions:
            print("No transactions found for this user.")
            return

        # Prepare data for tabulation
        headers = ["ID", "Type", "Ticker", "Qty", "Price", "Total", "Date", "Portfolio"]
        table_data = []

        for txn in transactions:
            table_data.append([
                txn['transaction_id'],
                txn['transaction_type'],
                txn['ticker_symbol'],
                txn['quantity'],
                f"${txn['price_per_share']:.2f}",
                f"${txn['total_amount']:.2f}",
                txn['transaction_date'].strftime('%Y-%m-%d'),
                txn['portfolio_name'][:15]
            ])

        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal Transactions: {len(transactions)}")

        # Calculate summary
        buy_total = sum(txn['total_amount'] for txn in transactions if txn['transaction_type'] == 'BUY')
        sell_total = sum(txn['total_amount'] for txn in transactions if txn['transaction_type'] == 'SELL')

        print(f"\nSummary:")
        print(f"  Total Purchases: ${buy_total:.2f}")
        print(f"  Total Sales:     ${sell_total:.2f}")
        print(f"  Net Investment:  ${buy_total - sell_total:.2f}")

    def view_user_portfolios(self):
        """Display portfolios for a specific user."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 23 + "USER PORTFOLIOS")
        print("=" * 70 + "\n")

        # Get user ID
        try:
            user_id = int(input("Enter User ID (or 0 to cancel): "))
            if user_id == 0:
                return
        except ValueError:
            print("Invalid User ID. Please enter a number.")
            return

        # Verify user exists
        user = UserDAO.read_by_id(user_id)
        if not user:
            print(f"No user found with ID {user_id}")
            return

        print(f"\nPortfolios for: {user['first_name']} {user['last_name']} (@{user['username']})")
        print(f"Account Balance: ${user['account_balance']:.2f}")
        print("-" * 70)

        portfolios = PortfolioDAO.find_by_user(user_id)

        if not portfolios:
            print("No portfolios found for this user.")
            return

        # Prepare data for tabulation
        headers = ["ID", "Name", "Total Value", "Status", "Created"]
        table_data = []

        for portfolio in portfolios:
            status = "Active" if portfolio['is_active'] else "Inactive"
            table_data.append([
                portfolio['portfolio_id'],
                portfolio['portfolio_name'],
                f"${portfolio['total_value']:.2f}",
                status,
                portfolio['created_at'].strftime('%Y-%m-%d')
            ])

        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal Portfolios: {len(portfolios)}")

        total_value = sum(p['total_value'] for p in portfolios)
        print(f"Combined Portfolio Value: ${total_value:.2f}")

    def view_user_watchlist(self):
        """Display watchlist for a specific user."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 24 + "USER WATCHLIST")
        print("=" * 70 + "\n")

        # Get user ID
        try:
            user_id = int(input("Enter User ID (or 0 to cancel): "))
            if user_id == 0:
                return
        except ValueError:
            print("Invalid User ID. Please enter a number.")
            return

        # Verify user exists
        user = UserDAO.read_by_id(user_id)
        if not user:
            print(f"No user found with ID {user_id}")
            return

        print(f"\nWatchlist for: {user['first_name']} {user['last_name']} (@{user['username']})")
        print("-" * 70)

        watchlist = WatchlistDAO.find_by_user(user_id)

        if not watchlist:
            print("Watchlist is empty.")
            return

        # Prepare data for tabulation
        headers = ["ID", "Ticker", "Company", "Current", "Target", "Alert", "Added"]
        table_data = []

        for item in watchlist:
            target = f"${item['target_price']:.2f}" if item['target_price'] else "N/A"
            alert = "Yes" if item['alert_enabled'] else "No"
            table_data.append([
                item['watchlist_id'],
                item['ticker_symbol'],
                item['company_name'][:25],
                f"${item['current_price']:.2f}",
                target,
                alert,
                item['added_date'].strftime('%Y-%m-%d')
            ])

        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal Stocks Watched: {len(watchlist)}")

    def search_stock_by_ticker(self):
        """Search for a stock by ticker symbol."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 22 + "SEARCH STOCK BY TICKER")
        print("=" * 70 + "\n")

        ticker = input("Enter Ticker Symbol (or press Enter to cancel): ").strip().upper()
        if not ticker:
            return

        stock = StockDAO.find_by_ticker(ticker)

        if not stock:
            print(f"\nNo stock found with ticker symbol: {ticker}")
            return

        print(f"\n{'Stock Details':^70}")
        print("-" * 70)
        print(f"Ticker Symbol:   {stock['ticker_symbol']}")
        print(f"Company Name:    {stock['company_name']}")
        print(f"Current Price:   ${stock['current_price']:.2f}")
        print(f"Market Cap:      ${stock['market_cap']:,}" if stock['market_cap'] else "N/A")
        print(f"Sector:          {stock['sector']}")
        print(f"Industry:        {stock['industry']}" if stock['industry'] else "N/A")
        print(f"Last Updated:    {stock['last_updated']}")
        print("-" * 70)

    def view_stocks_by_sector(self):
        """View all stocks in a specific sector."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 22 + "STOCKS BY SECTOR")
        print("=" * 70 + "\n")

        # Get all unique sectors first
        all_stocks = StockDAO.read_all()
        sectors = sorted(set(stock['sector'] for stock in all_stocks))

        print("Available Sectors:")
        for i, sector in enumerate(sectors, 1):
            print(f"  {i}. {sector}")

        try:
            choice = int(input(f"\nSelect sector (1-{len(sectors)}, or 0 to cancel): "))
            if choice == 0:
                return
            if choice < 1 or choice > len(sectors):
                print("Invalid selection.")
                return

            selected_sector = sectors[choice - 1]
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        print(f"\n{'Stocks in ' + selected_sector + ' Sector':^70}")
        print("=" * 70)

        stocks = StockDAO.find_by_sector(selected_sector)

        if not stocks:
            print(f"No stocks found in {selected_sector} sector.")
            return

        # Prepare data for tabulation
        headers = ["Ticker", "Company", "Price", "Industry"]
        table_data = []

        for stock in stocks:
            table_data.append([
                stock['ticker_symbol'],
                stock['company_name'][:35],
                f"${stock['current_price']:.2f}",
                stock['industry'] if stock['industry'] else "N/A"
            ])

        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal Stocks in {selected_sector}: {len(stocks)}")

    def view_all_users(self):
        """Display all users."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 27 + "ALL USERS")
        print("=" * 70 + "\n")

        users = UserDAO.read_all()

        if not users:
            print("No users found in the database.")
            return

        # Prepare data for tabulation
        headers = ["ID", "Username", "Name", "Email", "Balance", "Created"]
        table_data = []

        for user in users:
            table_data.append([
                user['user_id'],
                user['username'],
                f"{user['first_name']} {user['last_name']}",
                user['email'],
                f"${user['account_balance']:.2f}",
                user['created_at'].strftime('%Y-%m-%d')
            ])

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
        print(f"\nTotal Users: {len(users)}")

    def view_stock_details(self):
        """View detailed information about a specific stock."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 24 + "STOCK DETAILS")
        print("=" * 70 + "\n")

        try:
            stock_id = int(input("Enter Stock ID (or 0 to cancel): "))
            if stock_id == 0:
                return
        except ValueError:
            print("Invalid Stock ID. Please enter a number.")
            return

        stock = StockDAO.read_by_id(stock_id)

        if not stock:
            print(f"No stock found with ID {stock_id}")
            return

        print(f"\n{'Stock Information':^70}")
        print("=" * 70)
        print(f"Stock ID:        {stock['stock_id']}")
        print(f"Ticker Symbol:   {stock['ticker_symbol']}")
        print(f"Company Name:    {stock['company_name']}")
        print(f"Current Price:   ${stock['current_price']:.2f}")
        print(f"Market Cap:      ${stock['market_cap']:,}" if stock['market_cap'] else "N/A")
        print(f"Sector:          {stock['sector']}")
        print(f"Industry:        {stock['industry']}" if stock['industry'] else "N/A")
        print(f"Last Updated:    {stock['last_updated']}")
        print("=" * 70)

        # Show related transactions
        transactions = TransactionDAO.find_by_stock(stock_id)
        print(f"\nRecent Transactions: {len(transactions)}")

        if transactions:
            headers = ["Type", "User", "Qty", "Price", "Total", "Date"]
            table_data = []

            for txn in transactions[:5]:  # Show last 5
                table_data.append([
                    txn['transaction_type'],
                    txn['username'],
                    txn['quantity'],
                    f"${txn['price_per_share']:.2f}",
                    f"${txn['total_amount']:.2f}",
                    txn['transaction_date'].strftime('%Y-%m-%d')
                ])

            print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def create_transaction(self):
        """Create a new transaction (demo functionality)."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 21 + "CREATE NEW TRANSACTION")
        print("=" * 70 + "\n")

        try:
            user_id = int(input("Enter User ID: "))
            stock_id = int(input("Enter Stock ID: "))
            portfolio_id = int(input("Enter Portfolio ID: "))
            txn_type = input("Transaction Type (BUY/SELL): ").upper()
            quantity = int(input("Enter Quantity: "))
            price = Decimal(input("Enter Price per Share: "))
            notes = input("Notes (optional): ").strip()

            if txn_type not in ['BUY', 'SELL']:
                print("Invalid transaction type. Must be BUY or SELL.")
                return

            transaction_id = TransactionDAO.create(
                user_id=user_id,
                stock_id=stock_id,
                portfolio_id=portfolio_id,
                transaction_type=txn_type,
                quantity=quantity,
                price_per_share=price,
                notes=notes if notes else None
            )

            if transaction_id:
                print(f"\n✓ Transaction created successfully!")
                print(f"  Transaction ID: {transaction_id}")
                print(f"  Type: {txn_type}")
                print(f"  Total: ${quantity * price:.2f}")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error creating transaction: {e}")

    def add_to_watchlist(self):
        """Add a stock to user's watchlist (demo functionality)."""
        self.clear_screen()
        print("\n" + "=" * 70)
        print(" " * 20 + "ADD STOCK TO WATCHLIST")
        print("=" * 70 + "\n")

        try:
            user_id = int(input("Enter User ID: "))
            stock_id = int(input("Enter Stock ID: "))
            target_price = input("Target Price (optional, press Enter to skip): ").strip()
            notes = input("Notes (optional): ").strip()
            alert = input("Enable Alert? (y/n): ").lower() == 'y'

            target_price = Decimal(target_price) if target_price else None

            watchlist_id = WatchlistDAO.create(
                user_id=user_id,
                stock_id=stock_id,
                target_price=target_price,
                notes=notes if notes else None,
                alert_enabled=alert
            )

            if watchlist_id:
                print(f"\n✓ Stock added to watchlist successfully!")
                print(f"  Watchlist ID: {watchlist_id}")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error adding to watchlist: {e}")

    def run(self):
        """Run the main application loop."""
        self.display_header()

        # Initialize database connection
        print("\nInitializing database connection...")
        try:
            db_host = input("Database Host (default: localhost): ").strip() or "localhost"
            db_name = input("Database Name (default: stock_tracker): ").strip() or "stock_tracker"
            db_user = input("Database User (default: root): ").strip() or "root"
            db_pass = input("Database Password: ").strip()

            DatabaseConnection.initialize_pool(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_pass,
                pool_size=5
            )
            print("\n✓ Database connection established!")
        except Exception as e:
            print(f"\n✗ Failed to connect to database: {e}")
            print("Please check your database credentials and try again.")
            return

        # Main application loop
        while self.running:
            self.display_menu()

            try:
                choice = input("\nEnter your choice: ").strip()

                if choice == '1':
                    self.view_all_stocks()
                elif choice == '2':
                    self.view_user_transactions()
                elif choice == '3':
                    self.view_user_portfolios()
                elif choice == '4':
                    self.view_user_watchlist()
                elif choice == '5':
                    self.search_stock_by_ticker()
                elif choice == '6':
                    self.view_stocks_by_sector()
                elif choice == '7':
                    self.view_all_users()
                elif choice == '8':
                    self.view_stock_details()
                elif choice == '9':
                    self.create_transaction()
                elif choice == '10':
                    self.add_to_watchlist()
                elif choice == '0':
                    print("\n" + "=" * 70)
                    print(" " * 20 + "Thank you for using")
                    print(" " * 15 + "Stock Portfolio Tracker!")
                    print("=" * 70 + "\n")
                    self.running = False
                else:
                    print("\n✗ Invalid choice. Please select a valid option.")

                if self.running:
                    input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\n\nExiting application...")
                self.running = False
            except Exception as e:
                print(f"\n✗ An error occurred: {e}")
                input("\nPress Enter to continue...")


def main():
    """Main entry point for the application."""
    app = StockTrackerConsole()
    app.run()


if __name__ == "__main__":
    main()
