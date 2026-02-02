-- ============================================
-- Stock Portfolio Tracker - Test Data Population
-- Total Rows: 62+ rows across all tables
-- ============================================

-- ============================================
-- Populate Users Table (10 rows)
-- ============================================
INSERT INTO Users (username, email, password_hash, first_name, last_name, account_balance, created_at) VALUES
('johndoe', 'john.doe@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7TrRX3mq7u', 'John', 'Doe', 50000.00, '2024-01-15 10:30:00'),
('janesmit', 'jane.smith@email.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36zq5G7lJ8D.yN4/bQ9Kq3u', 'Jane', 'Smith', 75000.00, '2024-02-20 14:15:00'),
('investorpro', 'mike.johnson@email.com', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Mike', 'Johnson', 120000.00, '2024-01-05 09:00:00'),
('sarahtrade', 'sarah.williams@email.com', '$2b$12$gPJqBj7YBLzz4B1A.CpW3OdYfXh5qEy5YLz8XN6Yx2uJ8pGqKzE7S', 'Sarah', 'Williams', 35000.00, '2024-03-10 11:45:00'),
('davidc', 'david.chen@email.com', '$2b$12$xM1N2pQ3rS4tU5vW6xY7zA8bC9dE0fG1hI2jK3lM4nO5pQ6rS7tU8v', 'David', 'Chen', 92000.00, '2024-02-01 08:20:00'),
('emilybrown', 'emily.brown@email.com', '$2b$12$aA1bB2cC3dD4eE5fF6gG7hH8iI9jJ0kK1lL2mM3nN4oO5pP6qQ7rR8s', 'Emily', 'Brown', 45000.00, '2024-03-25 16:30:00'),
('robertlee', 'robert.lee@email.com', '$2b$12$tT1uU2vV3wW4xX5yY6zZ7aA8bB9cC0dD1eE2fF3gG4hH5iI6jJ7kK8l', 'Robert', 'Lee', 68000.00, '2024-01-20 13:00:00'),
('lisadavis', 'lisa.davis@email.com', '$2b$12$mM1nN2oO3pP4qQ5rR6sS7tT8uU9vV0wW1xX2yY3zZ4aA5bB6cC7dD8e', 'Lisa', 'Davis', 55000.00, '2024-02-28 10:15:00'),
('markwilson', 'mark.wilson@email.com', '$2b$12$fF1gG2hH3iI4jJ5kK6lL7mM8nN9oO0pP1qQ2rR3sS4tT5uU6vV7wW8x', 'Mark', 'Wilson', 81000.00, '2024-03-05 09:45:00'),
('amygarcia', 'amy.garcia@email.com', '$2b$12$yY1zZ2aA3bB4cC5dD6eE7fF8gG9hH0iI1jJ2kK3lL4mM5nN6oO7pP8q', 'Amy', 'Garcia', 43000.00, '2024-03-15 15:20:00');

-- ============================================
-- Populate Stocks Table (15 rows)
-- ============================================
INSERT INTO Stocks (ticker_symbol, company_name, current_price, market_cap, sector, industry, last_updated) VALUES
('AAPL', 'Apple Inc.', 178.25, 2800000000000, 'Technology', 'Consumer Electronics', '2024-03-28 16:00:00'),
('MSFT', 'Microsoft Corporation', 425.50, 3200000000000, 'Technology', 'Software', '2024-03-28 16:00:00'),
('GOOGL', 'Alphabet Inc.', 142.75, 1800000000000, 'Technology', 'Internet Services', '2024-03-28 16:00:00'),
('AMZN', 'Amazon.com Inc.', 178.90, 1850000000000, 'Consumer Cyclical', 'E-commerce', '2024-03-28 16:00:00'),
('TSLA', 'Tesla Inc.', 175.50, 550000000000, 'Consumer Cyclical', 'Auto Manufacturers', '2024-03-28 16:00:00'),
('NVDA', 'NVIDIA Corporation', 875.20, 2200000000000, 'Technology', 'Semiconductors', '2024-03-28 16:00:00'),
('JPM', 'JPMorgan Chase & Co.', 198.75, 570000000000, 'Financial Services', 'Banking', '2024-03-28 16:00:00'),
('V', 'Visa Inc.', 278.30, 580000000000, 'Financial Services', 'Credit Services', '2024-03-28 16:00:00'),
('JNJ', 'Johnson & Johnson', 158.65, 390000000000, 'Healthcare', 'Pharmaceuticals', '2024-03-28 16:00:00'),
('WMT', 'Walmart Inc.', 165.20, 450000000000, 'Consumer Defensive', 'Retail', '2024-03-28 16:00:00'),
('PG', 'Procter & Gamble Co.', 162.85, 385000000000, 'Consumer Defensive', 'Consumer Goods', '2024-03-28 16:00:00'),
('DIS', 'The Walt Disney Company', 112.40, 205000000000, 'Communication Services', 'Entertainment', '2024-03-28 16:00:00'),
('NFLX', 'Netflix Inc.', 598.75, 260000000000, 'Communication Services', 'Streaming', '2024-03-28 16:00:00'),
('BA', 'The Boeing Company', 185.30, 115000000000, 'Industrials', 'Aerospace & Defense', '2024-03-28 16:00:00'),
('XOM', 'Exxon Mobil Corporation', 110.85, 460000000000, 'Energy', 'Oil & Gas', '2024-03-28 16:00:00');

-- ============================================
-- Populate Portfolios Table (12 rows)
-- ============================================
INSERT INTO Portfolios (user_id, portfolio_name, description, total_value, created_at, is_active) VALUES
(1, 'Tech Growth', 'High-growth technology stocks portfolio', 25000.00, '2024-01-15 10:35:00', TRUE),
(1, 'Dividend Income', 'Stable dividend-paying stocks', 15000.00, '2024-01-16 11:00:00', TRUE),
(2, 'Aggressive Growth', 'High-risk, high-reward investments', 45000.00, '2024-02-20 14:30:00', TRUE),
(3, 'Core Holdings', 'Long-term core investment portfolio', 80000.00, '2024-01-05 09:15:00', TRUE),
(3, 'Tech Spec', 'Specialized technology sector plays', 30000.00, '2024-01-10 10:00:00', TRUE),
(4, 'Balanced Portfolio', 'Mix of growth and value stocks', 20000.00, '2024-03-10 12:00:00', TRUE),
(5, 'AI & Innovation', 'Artificial intelligence and innovation stocks', 55000.00, '2024-02-01 08:30:00', TRUE),
(6, 'Blue Chip Stocks', 'Established large-cap companies', 30000.00, '2024-03-25 16:45:00', TRUE),
(7, 'Value Investing', 'Undervalued stocks with growth potential', 42000.00, '2024-01-20 13:15:00', TRUE),
(8, 'Healthcare Focus', 'Healthcare and pharmaceutical stocks', 35000.00, '2024-02-28 10:30:00', TRUE),
(9, 'Financial Sector', 'Banks and financial services', 48000.00, '2024-03-05 10:00:00', TRUE),
(10, 'Starter Portfolio', 'First investment portfolio', 18000.00, '2024-03-15 15:30:00', TRUE);

-- ============================================
-- Populate Transactions Table (15 rows)
-- ============================================
INSERT INTO Transactions (user_id, stock_id, portfolio_id, transaction_type, quantity, price_per_share, total_amount, transaction_date, notes) VALUES
(1, 1, 1, 'BUY', 50, 175.50, 8775.00, '2024-01-15 11:00:00', 'Initial purchase of Apple stock'),
(1, 2, 1, 'BUY', 30, 420.00, 12600.00, '2024-01-16 14:30:00', 'Added Microsoft to tech portfolio'),
(2, 6, 3, 'BUY', 25, 850.00, 21250.00, '2024-02-21 10:15:00', 'NVIDIA investment for AI exposure'),
(2, 5, 3, 'BUY', 100, 170.00, 17000.00, '2024-02-22 09:45:00', 'Tesla long position'),
(3, 1, 4, 'BUY', 200, 172.00, 34400.00, '2024-01-06 10:30:00', 'Large Apple position'),
(3, 2, 5, 'BUY', 75, 415.00, 31125.00, '2024-01-11 13:00:00', 'Microsoft for tech spec portfolio'),
(3, 3, 5, 'BUY', 100, 140.00, 14000.00, '2024-01-12 11:20:00', 'Added Google to holdings'),
(4, 7, 6, 'BUY', 50, 195.00, 9750.00, '2024-03-11 10:45:00', 'JPMorgan Chase investment'),
(5, 6, 7, 'BUY', 40, 860.00, 34400.00, '2024-02-02 09:30:00', 'NVIDIA for AI portfolio'),
(6, 9, 8, 'BUY', 100, 160.00, 16000.00, '2024-03-26 11:15:00', 'Johnson & Johnson blue chip'),
(7, 8, 9, 'BUY', 75, 275.00, 20625.00, '2024-01-21 14:00:00', 'Visa for value portfolio'),
(8, 9, 10, 'BUY', 120, 158.00, 18960.00, '2024-03-01 10:00:00', 'Healthcare sector investment'),
(9, 7, 11, 'BUY', 150, 196.50, 29475.00, '2024-03-06 09:15:00', 'Financial sector exposure'),
(10, 4, 12, 'BUY', 50, 180.00, 9000.00, '2024-03-16 10:30:00', 'Amazon starter position'),
(2, 5, 3, 'SELL', 20, 175.00, 3500.00, '2024-03-20 15:30:00', 'Partial Tesla profit taking');

-- ============================================
-- Populate Watchlists Table (10 rows)
-- ============================================
INSERT INTO Watchlists (user_id, stock_id, added_date, target_price, notes, alert_enabled) VALUES
(1, 3, '2024-01-17 09:00:00', 150.00, 'Waiting for better entry point on Google', TRUE),
(1, 6, '2024-01-18 10:30:00', 800.00, 'Watching NVIDIA for pullback', TRUE),
(2, 9, '2024-02-23 11:00:00', 155.00, 'Interested in healthcare sector', FALSE),
(3, 13, '2024-01-13 14:00:00', 550.00, 'Netflix content strategy looks promising', TRUE),
(4, 4, '2024-03-12 09:30:00', 170.00, 'Amazon cloud growth potential', TRUE),
(5, 14, '2024-02-03 10:00:00', 175.00, 'Boeing recovery play', FALSE),
(6, 15, '2024-03-27 11:30:00', 105.00, 'Energy sector diversification', TRUE),
(7, 12, '2024-01-22 13:30:00', 100.00, 'Disney streaming turnaround', FALSE),
(8, 11, '2024-03-02 09:45:00', 158.00, 'Procter & Gamble dividend stock', TRUE),
(10, 10, '2024-03-17 10:00:00', 160.00, 'Walmart defensive position', FALSE);

-- ============================================
-- Data Population Summary:
-- Users: 10 rows
-- Stocks: 15 rows
-- Portfolios: 12 rows
-- Transactions: 15 rows
-- Watchlists: 10 rows
-- TOTAL: 62 rows
-- ============================================

-- Verify data insertion
SELECT 'Users' AS TableName, COUNT(*) AS RowCount FROM Users
UNION ALL
SELECT 'Stocks', COUNT(*) FROM Stocks
UNION ALL
SELECT 'Portfolios', COUNT(*) FROM Portfolios
UNION ALL
SELECT 'Transactions', COUNT(*) FROM Transactions
UNION ALL
SELECT 'Watchlists', COUNT(*) FROM Watchlists
UNION ALL
SELECT 'TOTAL',
    (SELECT COUNT(*) FROM Users) +
    (SELECT COUNT(*) FROM Stocks) +
    (SELECT COUNT(*) FROM Portfolios) +
    (SELECT COUNT(*) FROM Transactions) +
    (SELECT COUNT(*) FROM Watchlists);
