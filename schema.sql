-- ============================================
-- Stock Portfolio Tracker Database Schema
-- Database: MySQL/PostgreSQL Compatible
-- ============================================

-- Drop tables if they exist (in reverse order due to foreign keys)
DROP TABLE IF EXISTS Watchlists;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Portfolios;
DROP TABLE IF EXISTS Stocks;
DROP TABLE IF EXISTS Users;

-- ============================================
-- Table: Users
-- Description: Stores user account information
-- ============================================
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    account_balance DECIMAL(15, 2) DEFAULT 10000.00 CHECK (account_balance >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    CONSTRAINT chk_email_format CHECK (email LIKE '%@%.%')
);

-- ============================================
-- Table: Stocks
-- Description: Stores stock information
-- ============================================
CREATE TABLE Stocks (
    stock_id INT AUTO_INCREMENT PRIMARY KEY,
    ticker_symbol VARCHAR(10) NOT NULL UNIQUE,
    company_name VARCHAR(100) NOT NULL,
    current_price DECIMAL(10, 2) NOT NULL CHECK (current_price > 0),
    market_cap BIGINT CHECK (market_cap > 0),
    sector VARCHAR(50) NOT NULL,
    industry VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT chk_ticker_uppercase CHECK (ticker_symbol = UPPER(ticker_symbol))
);

-- ============================================
-- Table: Portfolios
-- Description: Stores user portfolio information
-- ============================================
CREATE TABLE Portfolios (
    portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    portfolio_name VARCHAR(100) NOT NULL,
    description TEXT,
    total_value DECIMAL(15, 2) DEFAULT 0.00 CHECK (total_value >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_portfolio_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT unique_user_portfolio UNIQUE (user_id, portfolio_name)
);

-- ============================================
-- Table: Transactions
-- Description: Stores buy/sell transaction records
-- ============================================
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_id INT NOT NULL,
    portfolio_id INT NOT NULL,
    transaction_type ENUM('BUY', 'SELL') NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price_per_share DECIMAL(10, 2) NOT NULL CHECK (price_per_share > 0),
    total_amount DECIMAL(15, 2) NOT NULL CHECK (total_amount > 0),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    CONSTRAINT fk_transaction_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_transaction_stock FOREIGN KEY (stock_id)
        REFERENCES Stocks(stock_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_transaction_portfolio FOREIGN KEY (portfolio_id)
        REFERENCES Portfolios(portfolio_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_user_transactions (user_id, transaction_date)
);

-- ============================================
-- Table: Watchlists
-- Description: Stores stocks users are watching
-- ============================================
CREATE TABLE Watchlists (
    watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stock_id INT NOT NULL,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    target_price DECIMAL(10, 2) CHECK (target_price > 0),
    notes TEXT,
    alert_enabled BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_watchlist_user FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_watchlist_stock FOREIGN KEY (stock_id)
        REFERENCES Stocks(stock_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT unique_user_stock_watch UNIQUE (user_id, stock_id)
);

-- ============================================
-- Create Indexes for Performance
-- ============================================
CREATE INDEX idx_users_username ON Users(username);
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_stocks_ticker ON Stocks(ticker_symbol);
CREATE INDEX idx_stocks_sector ON Stocks(sector);
CREATE INDEX idx_portfolios_user ON Portfolios(user_id);
CREATE INDEX idx_watchlists_user ON Watchlists(user_id);

-- ============================================
-- Summary of Foreign Key Relationships:
-- 1. Portfolios.user_id -> Users.user_id
-- 2. Transactions.user_id -> Users.user_id
-- 3. Transactions.stock_id -> Stocks.stock_id
-- 4. Transactions.portfolio_id -> Portfolios.portfolio_id
-- 5. Watchlists.user_id -> Users.user_id
-- 6. Watchlists.stock_id -> Stocks.stock_id
--
-- Total: 6 Foreign Key Relationships
-- ============================================
