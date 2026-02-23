"""
Stock Portfolio Tracker - Service Layer (REST API)
Exposes business layer functionality as REST API endpoints using FastAPI.

HOSTING INSTRUCTIONS:
=====================
Local Development:
    1. Install dependencies: pip install fastapi uvicorn pydantic
    2. Run server: uvicorn service_layer:app --reload --host 0.0.0.0 --port 8000
    3. Access API docs: http://localhost:8000/docs
    4. Test endpoints: http://localhost:8000/api/v1/...

Production Deployment Options:
    Option 1 - Docker:
        - Build: docker build -t stock-tracker-api .
        - Run: docker run -p 8000:8000 stock-tracker-api

    Option 2 - Heroku:
        - Create Procfile: web: uvicorn service_layer:app --host 0.0.0.0 --port $PORT
        - Deploy: git push heroku main

    Option 3 - AWS/Azure:
        - Use Elastic Beanstalk or App Service
        - Configure with requirements.txt and startup command

API Documentation: Available at /docs (Swagger UI) and /redoc (ReDoc)
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import os

# Import Business Layer
from business_layer import (
    UserBusinessLogic,
    StockBusinessLogic,
    PortfolioBusinessLogic,
    TransactionBusinessLogic,
    WatchlistBusinessLogic,
    BusinessRuleException
)
from data_access_layer import DatabaseConnection

# Initialize FastAPI app
app = FastAPI(
    title="Stock Portfolio Tracker API",
    description="REST API for managing stock portfolios with full CRUD operations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==================== Pydantic Models (Request/Response Schemas) ====================

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    initial_balance: Optional[Decimal] = Field(default=Decimal('10000.00'), ge=0)


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    account_balance: Decimal
    created_at: datetime


class StockCreate(BaseModel):
    ticker_symbol: str = Field(..., min_length=1, max_length=10)
    company_name: str = Field(..., min_length=1, max_length=100)
    current_price: Decimal = Field(..., gt=0)
    market_cap: int = Field(..., gt=0)
    sector: str = Field(..., min_length=1, max_length=50)
    industry: Optional[str] = Field(None, max_length=50)


class StockPriceUpdate(BaseModel):
    new_price: Decimal = Field(..., gt=0)


class PortfolioCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    portfolio_name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class TransactionCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    stock_id: int = Field(..., gt=0)
    portfolio_id: int = Field(..., gt=0)
    transaction_type: str = Field(..., pattern="^(BUY|SELL)$")
    quantity: int = Field(..., gt=0)
    price_per_share: Decimal = Field(..., gt=0)
    notes: Optional[str] = None


class WatchlistCreate(BaseModel):
    user_id: int = Field(..., gt=0)
    stock_id: int = Field(..., gt=0)
    target_price: Optional[Decimal] = Field(None, gt=0)
    notes: Optional[str] = None
    alert_enabled: bool = False


class BalanceUpdate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    operation: str = Field(..., pattern="^(add|subtract)$")


# ==================== Startup/Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """
    Initialize database connection pool on startup.

    Supports multiple deployment methods:

    1. Railway.app (RECOMMENDED):
       - Set environment variable: MYSQL_URL = ${{ MySQL.MYSQL_URL }}
       - Railway auto-fills connection details

    2. Individual environment variables:
       - DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

    3. Local development:
       - Uses default localhost settings
    """
    try:
        # Check for Railway-style MYSQL_URL first
        mysql_url = os.getenv('MYSQL_URL')

        if mysql_url:
            # Parse Railway connection URL: mysql://user:password@host:port/database
            import re
            match = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', mysql_url)
            if match:
                user, password, host, port, database = match.groups()
                db_config = {
                    'host': host,
                    'database': database,
                    'user': user,
                    'password': password,
                    'pool_size': 10
                }
                print("✓ Using Railway MySQL connection")
            else:
                raise ValueError("Invalid MYSQL_URL format")
        else:
            # Use individual environment variables or defaults (local dev)
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'database': os.getenv('DB_NAME', 'stock_tracker'),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', 'Stock2024!'),
                'pool_size': 10
            }
            print("✓ Using local/custom database configuration")

        DatabaseConnection.initialize_pool(**db_config)
        print(f"✓ Database connection pool initialized")
        print(f"  Host: {db_config['host']}")
        print(f"  Database: {db_config['database']}")

    except Exception as e:
        print(f"✗ Failed to initialize database: {e}")
        print(f"  Check your database connection settings")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    print("✓ API shutting down")


# ==================== Health Check ====================

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Stock Portfolio Tracker API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }


# ==================== User Endpoints ====================

@app.post("/api/v1/users", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: UserCreate):
    """Create a new user account."""
    try:
        result = UserBusinessLogic.create_user(
            username=user.username,
            email=user.email,
            password=user.password,
            first_name=user.first_name,
            last_name=user.last_name,
            initial_balance=user.initial_balance
        )
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except BusinessRuleException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/users/{user_id}", tags=["Users"])
async def get_user(user_id: int):
    """Get user by ID."""
    user = UserBusinessLogic.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@app.get("/api/v1/users", tags=["Users"])
async def get_all_users():
    """Get all users."""
    users = UserBusinessLogic.get_all_users()
    return {"users": users, "count": len(users)}


@app.put("/api/v1/users/{user_id}/balance", tags=["Users"])
async def update_user_balance(user_id: int, balance_update: BalanceUpdate):
    """Update user account balance."""
    try:
        result = UserBusinessLogic.update_user_balance(
            user_id=user_id,
            amount=balance_update.amount,
            operation=balance_update.operation
        )
        return result
    except BusinessRuleException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/v1/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int):
    """Delete a user."""
    result = UserBusinessLogic.delete_user(user_id)
    if not result['success']:
        raise HTTPException(status_code=404, detail=result['message'])
    return result


# ==================== Stock Endpoints ====================

@app.post("/api/v1/stocks", status_code=status.HTTP_201_CREATED, tags=["Stocks"])
async def create_stock(stock: StockCreate):
    """Create a new stock."""
    try:
        result = StockBusinessLogic.create_stock(
            ticker=stock.ticker_symbol,
            company_name=stock.company_name,
            current_price=stock.current_price,
            market_cap=stock.market_cap,
            sector=stock.sector,
            industry=stock.industry
        )
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except BusinessRuleException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/stocks/{stock_id}", tags=["Stocks"])
async def get_stock(stock_id: int):
    """Get stock by ID."""
    stock = StockBusinessLogic.get_stock(stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {stock_id} not found")
    return stock


@app.get("/api/v1/stocks", tags=["Stocks"])
async def get_all_stocks():
    """Get all stocks."""
    stocks = StockBusinessLogic.get_all_stocks()
    return {"stocks": stocks, "count": len(stocks)}


@app.get("/api/v1/stocks/ticker/{ticker}", tags=["Stocks"])
async def search_stock_by_ticker(ticker: str):
    """Search for stock by ticker symbol."""
    stock = StockBusinessLogic.search_stock_by_ticker(ticker)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock with ticker {ticker} not found")
    return stock


@app.get("/api/v1/stocks/sector/{sector}", tags=["Stocks"])
async def get_stocks_by_sector(sector: str):
    """Get all stocks in a specific sector."""
    stocks = StockBusinessLogic.get_stocks_by_sector(sector)
    return {"sector": sector, "stocks": stocks, "count": len(stocks)}


@app.put("/api/v1/stocks/{stock_id}/price", tags=["Stocks"])
async def update_stock_price(stock_id: int, price_update: StockPriceUpdate):
    """Update stock price."""
    try:
        result = StockBusinessLogic.update_stock_price(stock_id, price_update.new_price)
        return result
    except BusinessRuleException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/api/v1/stocks/{stock_id}", tags=["Stocks"])
async def delete_stock(stock_id: int):
    """Delete a stock."""
    result = StockBusinessLogic.delete_stock(stock_id)
    if not result['success']:
        raise HTTPException(status_code=404, detail=result['message'])
    return result


# ==================== Portfolio Endpoints ====================

@app.post("/api/v1/portfolios", status_code=status.HTTP_201_CREATED, tags=["Portfolios"])
async def create_portfolio(portfolio: PortfolioCreate):
    """Create a new portfolio."""
    try:
        result = PortfolioBusinessLogic.create_portfolio(
            user_id=portfolio.user_id,
            portfolio_name=portfolio.portfolio_name,
            description=portfolio.description
        )
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except BusinessRuleException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/portfolios/{portfolio_id}", tags=["Portfolios"])
async def get_portfolio(portfolio_id: int):
    """Get portfolio by ID."""
    portfolio = PortfolioBusinessLogic.get_portfolio(portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail=f"Portfolio {portfolio_id} not found")
    return portfolio


@app.get("/api/v1/portfolios", tags=["Portfolios"])
async def get_all_portfolios():
    """Get all portfolios."""
    portfolios = PortfolioBusinessLogic.get_all_portfolios()
    return {"portfolios": portfolios, "count": len(portfolios)}


@app.get("/api/v1/users/{user_id}/portfolios", tags=["Portfolios"])
async def get_user_portfolios(user_id: int):
    """Get all portfolios for a user."""
    portfolios = PortfolioBusinessLogic.get_user_portfolios(user_id)
    return {"user_id": user_id, "portfolios": portfolios, "count": len(portfolios)}


@app.delete("/api/v1/portfolios/{portfolio_id}", tags=["Portfolios"])
async def delete_portfolio(portfolio_id: int):
    """Delete a portfolio."""
    result = PortfolioBusinessLogic.delete_portfolio(portfolio_id)
    if not result['success']:
        raise HTTPException(status_code=404, detail=result['message'])
    return result


# ==================== Transaction Endpoints ====================

@app.post("/api/v1/transactions", status_code=status.HTTP_201_CREATED, tags=["Transactions"])
async def create_transaction(transaction: TransactionCreate):
    """Create a new transaction (BUY or SELL)."""
    try:
        result = TransactionBusinessLogic.create_transaction(
            user_id=transaction.user_id,
            stock_id=transaction.stock_id,
            portfolio_id=transaction.portfolio_id,
            transaction_type=transaction.transaction_type,
            quantity=transaction.quantity,
            price_per_share=transaction.price_per_share,
            notes=transaction.notes
        )
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except BusinessRuleException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/transactions/{transaction_id}", tags=["Transactions"])
async def get_transaction(transaction_id: int):
    """Get transaction by ID."""
    transaction = TransactionBusinessLogic.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")
    return transaction


@app.get("/api/v1/transactions", tags=["Transactions"])
async def get_all_transactions():
    """Get all transactions."""
    transactions = TransactionBusinessLogic.get_all_transactions()
    return {"transactions": transactions, "count": len(transactions)}


@app.get("/api/v1/users/{user_id}/transactions", tags=["Transactions"])
async def get_user_transactions(user_id: int):
    """Get all transactions for a user."""
    transactions = TransactionBusinessLogic.get_user_transactions(user_id)
    return {"user_id": user_id, "transactions": transactions, "count": len(transactions)}


@app.get("/api/v1/stocks/{stock_id}/transactions", tags=["Transactions"])
async def get_stock_transactions(stock_id: int):
    """Get all transactions for a stock."""
    transactions = TransactionBusinessLogic.get_stock_transactions(stock_id)
    return {"stock_id": stock_id, "transactions": transactions, "count": len(transactions)}


@app.delete("/api/v1/transactions/{transaction_id}", tags=["Transactions"])
async def delete_transaction(transaction_id: int):
    """Delete a transaction."""
    result = TransactionBusinessLogic.delete_transaction(transaction_id)
    if not result['success']:
        raise HTTPException(status_code=404, detail=result['message'])
    return result


# ==================== Watchlist Endpoints ====================

@app.post("/api/v1/watchlist", status_code=status.HTTP_201_CREATED, tags=["Watchlist"])
async def add_to_watchlist(watchlist_item: WatchlistCreate):
    """Add a stock to user's watchlist."""
    try:
        result = WatchlistBusinessLogic.add_to_watchlist(
            user_id=watchlist_item.user_id,
            stock_id=watchlist_item.stock_id,
            target_price=watchlist_item.target_price,
            notes=watchlist_item.notes,
            alert_enabled=watchlist_item.alert_enabled
        )
        if result['success']:
            return result
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except BusinessRuleException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/users/{user_id}/watchlist", tags=["Watchlist"])
async def get_user_watchlist(user_id: int):
    """Get user's complete watchlist."""
    watchlist = WatchlistBusinessLogic.get_user_watchlist(user_id)
    return {"user_id": user_id, "watchlist": watchlist, "count": len(watchlist)}


@app.get("/api/v1/users/{user_id}/watchlist/alerts", tags=["Watchlist"])
async def check_price_alerts(user_id: int):
    """Check for price alerts on user's watchlist."""
    alerts = WatchlistBusinessLogic.check_price_alerts(user_id)
    return {"user_id": user_id, "alerts": alerts, "count": len(alerts)}


@app.delete("/api/v1/watchlist/{watchlist_id}", tags=["Watchlist"])
async def remove_from_watchlist(watchlist_id: int):
    """Remove item from watchlist."""
    result = WatchlistBusinessLogic.remove_from_watchlist(watchlist_id)
    if not result['success']:
        raise HTTPException(status_code=404, detail=result['message'])
    return result


# ==================== Error Handlers ====================

@app.exception_handler(BusinessRuleException)
async def business_rule_exception_handler(request, exc):
    """Handle business rule violations."""
    return JSONResponse(
        status_code=400,
        content={"error": "Business Rule Violation", "detail": str(exc)}
    )


# ==================== Main Entry Point ====================

if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print(" " * 20 + "Stock Portfolio Tracker API")
    print(" " * 25 + "Service Layer v2.0")
    print("=" * 70)
    print("\nStarting server...")
    print("API Documentation: http://localhost:8000/docs")
    print("Alternative Docs: http://localhost:8000/redoc")
    print("\nPress CTRL+C to stop the server")
    print("=" * 70 + "\n")

    uvicorn.run(
        "service_layer:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
