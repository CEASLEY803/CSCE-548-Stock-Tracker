@echo off
REM Stock Portfolio Tracker - Database Setup Script for Windows
REM This script will create the database and import all data

echo ============================================
echo Stock Portfolio Tracker - Database Setup
echo ============================================
echo.

set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 9.6\bin\mysql.exe"

echo Step 1: Creating database...
%MYSQL_PATH% -u root -p -e "CREATE DATABASE IF NOT EXISTS stock_tracker;"
if errorlevel 1 (
    echo Error: Failed to create database. Check your password.
    pause
    exit /b 1
)
echo Database created successfully!
echo.

echo Step 2: Importing schema...
%MYSQL_PATH% -u root -p stock_tracker < ..\sql\schema.sql
if errorlevel 1 (
    echo Error: Failed to import schema.
    pause
    exit /b 1
)
echo Schema imported successfully!
echo.

echo Step 3: Importing test data...
%MYSQL_PATH% -u root -p stock_tracker < ..\sql\populate_data.sql
if errorlevel 1 (
    echo Error: Failed to import data.
    pause
    exit /b 1
)
echo Test data imported successfully!
echo.

echo Step 4: Verifying installation...
%MYSQL_PATH% -u root -p stock_tracker -e "SELECT 'Users' AS TableName, COUNT(*) AS RowCount FROM Users UNION ALL SELECT 'Stocks', COUNT(*) FROM Stocks UNION ALL SELECT 'Portfolios', COUNT(*) FROM Portfolios UNION ALL SELECT 'Transactions', COUNT(*) FROM Transactions UNION ALL SELECT 'Watchlists', COUNT(*) FROM Watchlists;"
echo.

echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo You can now run the application:
echo   python console_frontend.py
echo.
echo When prompted:
echo   Host: localhost
echo   Database: stock_tracker
echo   User: root
echo   Password: [your MySQL root password]
echo.
pause
