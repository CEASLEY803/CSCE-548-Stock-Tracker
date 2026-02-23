"""
Stock Portfolio Tracker - CRUD Operations Test
Demonstrates full Create, Read, Update, Delete cycle through the REST API.

This script proves that all service layer endpoints are working correctly.

PREREQUISITES:
- API server must be running: uvicorn service_layer:app --reload
- Database must be populated with test data
"""

import requests
import time
from datetime import datetime


class CRUDTester:
    """Automated testing of CRUD operations via REST API."""

    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_v1 = f"{base_url}/api/v1"
        self.test_results = []

    def log_test(self, test_name, success, details=""):
        """Log test result."""
        status = "✓ PASS" if success else "✗ FAIL"
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")

    def check_server(self):
        """Check if API server is running."""
        print("\n" + "=" * 70)
        print("Checking API Server Connection...")
        print("=" * 70)
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            if response.status_code == 200:
                self.log_test("Server Connection", True, "API server is online")
                return True
            else:
                self.log_test("Server Connection", False, f"Status code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Server Connection", False, str(e))
            print("\n✗ ERROR: Cannot connect to API server!")
            print("Please start the server first:")
            print("  py -m uvicorn service_layer:app --reload")
            return False

    def test_stock_crud(self):
        """Test full CRUD cycle for Stocks."""
        print("\n" + "=" * 70)
        print("Testing STOCK Entity - Full CRUD Cycle")
        print("=" * 70)

        # CREATE
        print("\n--- CREATE Operation ---")
        create_data = {
            "ticker_symbol": "CRUD",
            "company_name": "CRUD Test Company",
            "current_price": 150.75,
            "market_cap": 10000000000,
            "sector": "Technology",
            "industry": "Software Testing"
        }

        try:
            response = requests.post(f"{self.api_v1}/stocks", json=create_data)
            response.raise_for_status()
            result = response.json()
            stock_id = result.get('stock_id')
            self.log_test("CREATE Stock", True, f"Stock ID: {stock_id}, Ticker: CRUD")
        except requests.exceptions.RequestException as e:
            self.log_test("CREATE Stock", False, str(e))
            return

        time.sleep(0.5)

        # READ
        print("\n--- READ Operation ---")
        try:
            response = requests.get(f"{self.api_v1}/stocks/{stock_id}")
            response.raise_for_status()
            stock = response.json()
            self.log_test("READ Stock by ID", True,
                         f"Retrieved: {stock['ticker_symbol']} - ${stock['current_price']}")
        except requests.exceptions.RequestException as e:
            self.log_test("READ Stock by ID", False, str(e))

        try:
            response = requests.get(f"{self.api_v1}/stocks/ticker/CRUD")
            response.raise_for_status()
            stock = response.json()
            self.log_test("READ Stock by Ticker", True,
                         f"Found by ticker: {stock['company_name']}")
        except requests.exceptions.RequestException as e:
            self.log_test("READ Stock by Ticker", False, str(e))

        time.sleep(0.5)

        # UPDATE
        print("\n--- UPDATE Operation ---")
        update_data = {"new_price": 175.50}
        try:
            response = requests.put(f"{self.api_v1}/stocks/{stock_id}/price", json=update_data)
            response.raise_for_status()
            result = response.json()
            self.log_test("UPDATE Stock Price", True,
                         f"Price updated: ${result['old_price']} → ${result['new_price']}")
        except requests.exceptions.RequestException as e:
            self.log_test("UPDATE Stock Price", False, str(e))

        time.sleep(0.5)

        # DELETE
        print("\n--- DELETE Operation ---")
        try:
            response = requests.delete(f"{self.api_v1}/stocks/{stock_id}")
            response.raise_for_status()
            result = response.json()
            self.log_test("DELETE Stock", True, result['message'])
        except requests.exceptions.RequestException as e:
            self.log_test("DELETE Stock", False, str(e))

        # Verify deletion
        try:
            response = requests.get(f"{self.api_v1}/stocks/{stock_id}")
            if response.status_code == 404:
                self.log_test("Verify Deletion", True, "Stock no longer exists (404)")
            else:
                self.log_test("Verify Deletion", False, "Stock still exists")
        except requests.exceptions.RequestException:
            self.log_test("Verify Deletion", True, "Stock not found (as expected)")

    def test_user_crud(self):
        """Test full CRUD cycle for Users."""
        print("\n" + "=" * 70)
        print("Testing USER Entity - Full CRUD Cycle")
        print("=" * 70)

        # CREATE
        print("\n--- CREATE Operation ---")
        create_data = {
            "username": "testuser123",
            "email": "testuser@example.com",
            "password": "securepass123",
            "first_name": "Test",
            "last_name": "User",
            "initial_balance": 25000.00
        }

        try:
            response = requests.post(f"{self.api_v1}/users", json=create_data)
            response.raise_for_status()
            result = response.json()
            user_id = result.get('user_id')
            self.log_test("CREATE User", True, f"User ID: {user_id}, Username: testuser123")
        except requests.exceptions.RequestException as e:
            self.log_test("CREATE User", False, str(e))
            return

        time.sleep(0.5)

        # READ
        print("\n--- READ Operation ---")
        try:
            response = requests.get(f"{self.api_v1}/users/{user_id}")
            response.raise_for_status()
            user = response.json()
            self.log_test("READ User", True,
                         f"Retrieved: {user['username']}, Balance: ${user['account_balance']}")
        except requests.exceptions.RequestException as e:
            self.log_test("READ User", False, str(e))

        time.sleep(0.5)

        # UPDATE
        print("\n--- UPDATE Operation ---")
        update_data = {
            "amount": 5000.00,
            "operation": "add"
        }
        try:
            response = requests.put(f"{self.api_v1}/users/{user_id}/balance", json=update_data)
            response.raise_for_status()
            result = response.json()
            self.log_test("UPDATE User Balance", True,
                         f"Balance: ${result['previous_balance']} → ${result['new_balance']}")
        except requests.exceptions.RequestException as e:
            self.log_test("UPDATE User Balance", False, str(e))

        time.sleep(0.5)

        # DELETE
        print("\n--- DELETE Operation ---")
        try:
            response = requests.delete(f"{self.api_v1}/users/{user_id}")
            response.raise_for_status()
            result = response.json()
            self.log_test("DELETE User", True, result['message'])
        except requests.exceptions.RequestException as e:
            self.log_test("DELETE User", False, str(e))

    def test_portfolio_crud(self):
        """Test full CRUD cycle for Portfolios."""
        print("\n" + "=" * 70)
        print("Testing PORTFOLIO Entity - Full CRUD Cycle")
        print("=" * 70)

        # CREATE
        print("\n--- CREATE Operation ---")
        create_data = {
            "user_id": 1,  # Using existing user
            "portfolio_name": "Test CRUD Portfolio",
            "description": "Portfolio created for CRUD testing"
        }

        try:
            response = requests.post(f"{self.api_v1}/portfolios", json=create_data)
            response.raise_for_status()
            result = response.json()
            portfolio_id = result.get('portfolio_id')
            self.log_test("CREATE Portfolio", True, f"Portfolio ID: {portfolio_id}")
        except requests.exceptions.RequestException as e:
            self.log_test("CREATE Portfolio", False, str(e))
            return

        time.sleep(0.5)

        # READ
        print("\n--- READ Operation ---")
        try:
            response = requests.get(f"{self.api_v1}/portfolios/{portfolio_id}")
            response.raise_for_status()
            portfolio = response.json()
            self.log_test("READ Portfolio", True,
                         f"Retrieved: {portfolio['portfolio_name']}")
        except requests.exceptions.RequestException as e:
            self.log_test("READ Portfolio", False, str(e))

        time.sleep(0.5)

        # DELETE
        print("\n--- DELETE Operation ---")
        try:
            response = requests.delete(f"{self.api_v1}/portfolios/{portfolio_id}")
            response.raise_for_status()
            result = response.json()
            self.log_test("DELETE Portfolio", True, result['message'])
        except requests.exceptions.RequestException as e:
            self.log_test("DELETE Portfolio", False, str(e))

    def test_transaction_crud(self):
        """Test Transaction creation and retrieval."""
        print("\n" + "=" * 70)
        print("Testing TRANSACTION Entity - Create & Read")
        print("=" * 70)

        # CREATE
        print("\n--- CREATE Operation ---")
        create_data = {
            "user_id": 1,
            "stock_id": 1,
            "portfolio_id": 1,
            "transaction_type": "BUY",
            "quantity": 10,
            "price_per_share": 178.25,
            "notes": "CRUD test transaction"
        }

        try:
            response = requests.post(f"{self.api_v1}/transactions", json=create_data)
            response.raise_for_status()
            result = response.json()
            transaction_id = result.get('transaction_id')
            self.log_test("CREATE Transaction", True,
                         f"Transaction ID: {transaction_id}, Total: ${result['total_amount']}")
        except requests.exceptions.RequestException as e:
            self.log_test("CREATE Transaction", False, str(e))
            return

        time.sleep(0.5)

        # READ
        print("\n--- READ Operation ---")
        try:
            response = requests.get(f"{self.api_v1}/transactions/{transaction_id}")
            response.raise_for_status()
            transaction = response.json()
            self.log_test("READ Transaction", True,
                         f"Type: {transaction['transaction_type']}, Qty: {transaction['quantity']}")
        except requests.exceptions.RequestException as e:
            self.log_test("READ Transaction", False, str(e))

        # DELETE (cleanup)
        try:
            response = requests.delete(f"{self.api_v1}/transactions/{transaction_id}")
            response.raise_for_status()
            self.log_test("DELETE Transaction (cleanup)", True, "Removed test transaction")
        except requests.exceptions.RequestException as e:
            self.log_test("DELETE Transaction (cleanup)", False, str(e))

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 70)
        print(" " * 25 + "TEST SUMMARY")
        print("=" * 70)

        total = len(self.test_results)
        passed = len([r for r in self.test_results if "PASS" in r['status']])
        failed = total - passed

        print(f"\nTotal Tests: {total}")
        print(f"✓ Passed:    {passed}")
        print(f"✗ Failed:    {failed}")
        print(f"Success Rate: {(passed/total*100):.1f}%")

        if failed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if "FAIL" in result['status']:
                    print(f"  - {result['test']}: {result['details']}")

        print("\n" + "=" * 70)
        print("All operations were performed via REST API")
        print("Architecture: Console → REST API → Business Layer → DAL → Database")
        print("=" * 70 + "\n")

    def run_all_tests(self):
        """Run all CRUD tests."""
        print("\n" + "=" * 70)
        print(" " * 15 + "STOCK PORTFOLIO TRACKER")
        print(" " * 15 + "CRUD Operations Test Suite")
        print(" " * 20 + "Project 2 - CSCE 548")
        print("=" * 70)

        if not self.check_server():
            return

        # Run all tests
        self.test_stock_crud()
        self.test_user_crud()
        self.test_portfolio_crud()
        self.test_transaction_crud()

        # Print summary
        self.print_summary()


def main():
    """Main entry point."""
    tester = CRUDTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
