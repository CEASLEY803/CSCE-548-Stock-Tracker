// Stock Portfolio Tracker - Web Client
// API Configuration
const API_BASE_URL = 'https://csce-548-stock-tracker-production.up.railway.app';
const API_V1 = `${API_BASE_URL}/api/v1`;

// Global data storage
let allStocks = [];
let allUsers = [];
let allPortfolios = [];
let allTransactions = [];
let allWatchlist = [];

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Stock Portfolio Tracker - Web Client Initialized');
    document.getElementById('apiUrl').textContent = API_BASE_URL;
    checkAPIConnection();
    loadInitialData();
});

// API Connection Check
async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            document.getElementById('apiStatusBadge').className = 'badge bg-success';
            document.getElementById('apiStatusBadge').textContent = '✓ Connected';
        } else {
            document.getElementById('apiStatusBadge').className = 'badge bg-danger';
            document.getElementById('apiStatusBadge').textContent = '✗ API Error';
        }
    } catch (error) {
        document.getElementById('apiStatusBadge').className = 'badge bg-danger';
        document.getElementById('apiStatusBadge').textContent = '✗ Connection Failed';
        showAlert('Failed to connect to API server', 'danger');
    }
}

// Load Initial Data
async function loadInitialData() {
    await loadStocks();
    await loadUsers();
    await loadPortfolios();
    await loadTransactions();
    await loadWatchlist();
}

// ==================== STOCKS ====================

async function loadStocks() {
    showLoading('stocks');
    try {
        const response = await fetch(`${API_V1}/stocks`);
        const data = await response.json();
        allStocks = data.stocks || [];

        document.getElementById('stocksCount').textContent = allStocks.length;
        renderStocksTable(allStocks);
        populateSectorFilter();
        hideLoading('stocks');
    } catch (error) {
        showAlert('Error loading stocks: ' + error.message, 'danger');
        hideLoading('stocks');
    }
}

function renderStocksTable(stocks) {
    const tbody = document.getElementById('stocksTable');
    tbody.innerHTML = '';

    stocks.forEach(stock => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${stock.stock_id}</td>
            <td><strong>${stock.ticker_symbol}</strong></td>
            <td>${stock.company_name}</td>
            <td>$${parseFloat(stock.current_price).toFixed(2)}</td>
            <td>$${formatLargeNumber(stock.market_cap)}</td>
            <td><span class="badge bg-info">${stock.sector}</span></td>
            <td class="action-buttons">
                <button class="btn btn-sm btn-outline-primary" onclick="viewStock(${stock.stock_id})">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-warning" onclick="editStock(${stock.stock_id})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteStock(${stock.stock_id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function searchStockByTicker() {
    const ticker = document.getElementById('stockTickerSearch').value.trim().toUpperCase();
    if (!ticker) {
        showAlert('Please enter a ticker symbol', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/stocks/ticker/${ticker}`);
        if (response.ok) {
            const stock = await response.json();
            renderStocksTable([stock]);
            document.getElementById('stocksCount').textContent = '1 (filtered)';
        } else {
            showAlert(`Stock with ticker ${ticker} not found`, 'warning');
        }
    } catch (error) {
        showAlert('Error searching stock: ' + error.message, 'danger');
    }
}

function filterBySector() {
    const sector = document.getElementById('sectorFilter').value;
    if (sector === '') {
        renderStocksTable(allStocks);
        document.getElementById('stocksCount').textContent = allStocks.length;
    } else {
        const filtered = allStocks.filter(s => s.sector === sector);
        renderStocksTable(filtered);
        document.getElementById('stocksCount').textContent = `${filtered.length} (filtered)`;
    }
}

function populateSectorFilter() {
    const sectors = [...new Set(allStocks.map(s => s.sector))];
    const select = document.getElementById('sectorFilter');
    select.innerHTML = '<option value="">All Sectors</option>';
    sectors.forEach(sector => {
        const option = document.createElement('option');
        option.value = sector;
        option.textContent = sector;
        select.appendChild(option);
    });
}

async function viewStock(stockId) {
    try {
        const response = await fetch(`${API_V1}/stocks/${stockId}`);
        const stock = await response.json();

        const modal = createModal('View Stock Details', `
            <div class="row">
                <div class="col-md-6"><strong>Stock ID:</strong> ${stock.stock_id}</div>
                <div class="col-md-6"><strong>Ticker:</strong> ${stock.ticker_symbol}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12"><strong>Company Name:</strong> ${stock.company_name}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6"><strong>Current Price:</strong> $${stock.current_price}</div>
                <div class="col-md-6"><strong>Market Cap:</strong> $${formatLargeNumber(stock.market_cap)}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6"><strong>Sector:</strong> ${stock.sector}</div>
                <div class="col-md-6"><strong>Industry:</strong> ${stock.industry || 'N/A'}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12"><strong>Last Updated:</strong> ${new Date(stock.last_updated).toLocaleString()}</div>
            </div>
        `);
        showModal(modal);
    } catch (error) {
        showAlert('Error viewing stock: ' + error.message, 'danger');
    }
}

async function deleteStock(stockId) {
    if (!confirm('Are you sure you want to delete this stock?')) return;

    try {
        const response = await fetch(`${API_V1}/stocks/${stockId}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showAlert('Stock deleted successfully', 'success');
            await loadStocks();
        } else {
            showAlert('Failed to delete stock: ' + result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting stock: ' + error.message, 'danger');
    }
}

// ==================== USERS ====================

async function loadUsers() {
    showLoading('users');
    try {
        const response = await fetch(`${API_V1}/users`);
        const data = await response.json();
        allUsers = data.users || [];

        document.getElementById('usersCount').textContent = allUsers.length;
        renderUsersTable(allUsers);
        populateUserFilters();
        hideLoading('users');
    } catch (error) {
        showAlert('Error loading users: ' + error.message, 'danger');
        hideLoading('users');
    }
}

function renderUsersTable(users) {
    const tbody = document.getElementById('usersTable');
    tbody.innerHTML = '';

    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.user_id}</td>
            <td><strong>${user.username}</strong></td>
            <td>${user.first_name} ${user.last_name}</td>
            <td>${user.email}</td>
            <td>$${parseFloat(user.account_balance).toFixed(2)}</td>
            <td class="action-buttons">
                <button class="btn btn-sm btn-outline-primary" onclick="viewUser(${user.user_id})">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-warning" onclick="editUserBalance(${user.user_id})">
                    <i class="bi bi-wallet2"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteUser(${user.user_id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function viewUser(userId) {
    try {
        const response = await fetch(`${API_V1}/users/${userId}`);
        const user = await response.json();

        const modal = createModal('View User Details', `
            <div class="row">
                <div class="col-md-6"><strong>User ID:</strong> ${user.user_id}</div>
                <div class="col-md-6"><strong>Username:</strong> ${user.username}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6"><strong>First Name:</strong> ${user.first_name}</div>
                <div class="col-md-6"><strong>Last Name:</strong> ${user.last_name}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12"><strong>Email:</strong> ${user.email}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6"><strong>Account Balance:</strong> $${user.account_balance}</div>
                <div class="col-md-6"><strong>Created:</strong> ${new Date(user.created_at).toLocaleDateString()}</div>
            </div>
        `);
        showModal(modal);
    } catch (error) {
        showAlert('Error viewing user: ' + error.message, 'danger');
    }
}

async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This will also delete all their portfolios and transactions.')) return;

    try {
        const response = await fetch(`${API_V1}/users/${userId}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showAlert('User deleted successfully', 'success');
            await loadUsers();
            await loadPortfolios();
            await loadTransactions();
        } else {
            showAlert('Failed to delete user: ' + result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting user: ' + error.message, 'danger');
    }
}

// ==================== PORTFOLIOS ====================

async function loadPortfolios() {
    showLoading('portfolios');
    try {
        const response = await fetch(`${API_V1}/portfolios`);
        const data = await response.json();
        allPortfolios = data.portfolios || [];

        document.getElementById('portfoliosCount').textContent = allPortfolios.length;
        renderPortfoliosTable(allPortfolios);
        hideLoading('portfolios');
    } catch (error) {
        showAlert('Error loading portfolios: ' + error.message, 'danger');
        hideLoading('portfolios');
    }
}

function renderPortfoliosTable(portfolios) {
    const tbody = document.getElementById('portfoliosTable');
    tbody.innerHTML = '';

    portfolios.forEach(portfolio => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${portfolio.portfolio_id}</td>
            <td>${portfolio.user_id}</td>
            <td><strong>${portfolio.portfolio_name}</strong></td>
            <td>$${parseFloat(portfolio.total_value).toFixed(2)}</td>
            <td>${portfolio.is_active ? '<span class="badge bg-success">Active</span>' : '<span class="badge bg-secondary">Inactive</span>'}</td>
            <td class="action-buttons">
                <button class="btn btn-sm btn-outline-primary" onclick="viewPortfolio(${portfolio.portfolio_id})">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deletePortfolio(${portfolio.portfolio_id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function filterPortfoliosByUser() {
    const userId = document.getElementById('portfolioUserFilter').value;
    if (userId === '') {
        renderPortfoliosTable(allPortfolios);
        document.getElementById('portfoliosCount').textContent = allPortfolios.length;
    } else {
        try {
            const response = await fetch(`${API_V1}/users/${userId}/portfolios`);
            const data = await response.json();
            renderPortfoliosTable(data.portfolios);
            document.getElementById('portfoliosCount').textContent = `${data.portfolios.length} (filtered)`;
        } catch (error) {
            showAlert('Error filtering portfolios: ' + error.message, 'danger');
        }
    }
}

async function viewPortfolio(portfolioId) {
    try {
        const response = await fetch(`${API_V1}/portfolios/${portfolioId}`);
        const portfolio = await response.json();

        const modal = createModal('View Portfolio Details', `
            <div class="row">
                <div class="col-md-6"><strong>Portfolio ID:</strong> ${portfolio.portfolio_id}</div>
                <div class="col-md-6"><strong>User ID:</strong> ${portfolio.user_id}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12"><strong>Portfolio Name:</strong> ${portfolio.portfolio_name}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12"><strong>Description:</strong> ${portfolio.description || 'No description'}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6"><strong>Total Value:</strong> $${portfolio.total_value}</div>
                <div class="col-md-6"><strong>Status:</strong> ${portfolio.is_active ? 'Active' : 'Inactive'}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12"><strong>Created:</strong> ${new Date(portfolio.created_at).toLocaleString()}</div>
            </div>
        `);
        showModal(modal);
    } catch (error) {
        showAlert('Error viewing portfolio: ' + error.message, 'danger');
    }
}

async function deletePortfolio(portfolioId) {
    if (!confirm('Are you sure you want to delete this portfolio?')) return;

    try {
        const response = await fetch(`${API_V1}/portfolios/${portfolioId}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showAlert('Portfolio deleted successfully', 'success');
            await loadPortfolios();
        } else {
            showAlert('Failed to delete portfolio: ' + result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting portfolio: ' + error.message, 'danger');
    }
}

// ==================== TRANSACTIONS ====================

async function loadTransactions() {
    showLoading('transactions');
    try {
        const response = await fetch(`${API_V1}/transactions`);
        const data = await response.json();
        allTransactions = data.transactions || [];

        document.getElementById('transactionsCount').textContent = allTransactions.length;
        renderTransactionsTable(allTransactions);
        populateTransactionFilters();
        hideLoading('transactions');
    } catch (error) {
        showAlert('Error loading transactions: ' + error.message, 'danger');
        hideLoading('transactions');
    }
}

function renderTransactionsTable(transactions) {
    const tbody = document.getElementById('transactionsTable');
    tbody.innerHTML = '';

    transactions.forEach(txn => {
        const row = document.createElement('tr');
        const typeClass = txn.transaction_type === 'BUY' ? 'success' : 'danger';
        row.innerHTML = `
            <td>${txn.transaction_id}</td>
            <td><span class="badge bg-${typeClass}">${txn.transaction_type}</span></td>
            <td>${txn.user_id}</td>
            <td>${txn.stock_id}</td>
            <td>${txn.quantity}</td>
            <td>$${parseFloat(txn.price_per_share).toFixed(2)}</td>
            <td>$${parseFloat(txn.total_amount).toFixed(2)}</td>
            <td>${new Date(txn.transaction_date).toLocaleDateString()}</td>
            <td class="action-buttons">
                <button class="btn btn-sm btn-outline-primary" onclick="viewTransaction(${txn.transaction_id})">
                    <i class="bi bi-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteTransaction(${txn.transaction_id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function filterTransactionsByUser() {
    const userId = document.getElementById('transactionUserFilter').value;
    if (userId === '') {
        renderTransactionsTable(allTransactions);
        document.getElementById('transactionsCount').textContent = allTransactions.length;
    } else {
        try {
            const response = await fetch(`${API_V1}/users/${userId}/transactions`);
            const data = await response.json();
            renderTransactionsTable(data.transactions);
            document.getElementById('transactionsCount').textContent = `${data.transactions.length} (filtered)`;
        } catch (error) {
            showAlert('Error filtering transactions: ' + error.message, 'danger');
        }
    }
}

async function filterTransactionsByStock() {
    const stockId = document.getElementById('transactionStockFilter').value;
    if (stockId === '') {
        renderTransactionsTable(allTransactions);
        document.getElementById('transactionsCount').textContent = allTransactions.length;
    } else {
        try {
            const response = await fetch(`${API_V1}/stocks/${stockId}/transactions`);
            const data = await response.json();
            renderTransactionsTable(data.transactions);
            document.getElementById('transactionsCount').textContent = `${data.transactions.length} (filtered)`;
        } catch (error) {
            showAlert('Error filtering transactions: ' + error.message, 'danger');
        }
    }
}

async function viewTransaction(transactionId) {
    try {
        const response = await fetch(`${API_V1}/transactions/${transactionId}`);
        const txn = await response.json();

        const modal = createModal('View Transaction Details', `
            <div class="row">
                <div class="col-md-4"><strong>Transaction ID:</strong> ${txn.transaction_id}</div>
                <div class="col-md-4"><strong>Type:</strong> <span class="badge bg-${txn.transaction_type === 'BUY' ? 'success' : 'danger'}">${txn.transaction_type}</span></div>
                <div class="col-md-4"><strong>Date:</strong> ${new Date(txn.transaction_date).toLocaleString()}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-4"><strong>User ID:</strong> ${txn.user_id}</div>
                <div class="col-md-4"><strong>Stock ID:</strong> ${txn.stock_id}</div>
                <div class="col-md-4"><strong>Portfolio ID:</strong> ${txn.portfolio_id}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-4"><strong>Quantity:</strong> ${txn.quantity}</div>
                <div class="col-md-4"><strong>Price/Share:</strong> $${txn.price_per_share}</div>
                <div class="col-md-4"><strong>Total Amount:</strong> $${txn.total_amount}</div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-12"><strong>Notes:</strong> ${txn.notes || 'No notes'}</div>
            </div>
        `);
        showModal(modal);
    } catch (error) {
        showAlert('Error viewing transaction: ' + error.message, 'danger');
    }
}

async function deleteTransaction(transactionId) {
    if (!confirm('Are you sure you want to delete this transaction?')) return;

    try {
        const response = await fetch(`${API_V1}/transactions/${transactionId}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showAlert('Transaction deleted successfully', 'success');
            await loadTransactions();
        } else {
            showAlert('Failed to delete transaction: ' + result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting transaction: ' + error.message, 'danger');
    }
}

// ==================== WATCHLIST ====================

async function loadWatchlist() {
    showLoading('watchlist');
    try {
        // Note: This endpoint doesn't exist in the API, so we'll need to modify this
        // For now, we'll load watchlist for user 1 as an example
        const response = await fetch(`${API_V1}/users/1/watchlist`);
        const data = await response.json();
        allWatchlist = data.watchlist || [];

        document.getElementById('watchlistCount').textContent = allWatchlist.length;
        renderWatchlistTable(allWatchlist);
        hideLoading('watchlist');
    } catch (error) {
        // If endpoint doesn't work, show empty state
        hideLoading('watchlist');
        document.getElementById('watchlistContent').innerHTML = '<p class="text-muted text-center">No watchlist data available</p>';
    }
}

function renderWatchlistTable(watchlist) {
    const tbody = document.getElementById('watchlistTable');
    tbody.innerHTML = '';

    watchlist.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.watchlist_id}</td>
            <td>${item.user_id}</td>
            <td>${item.stock_id}</td>
            <td>${item.target_price ? '$' + item.target_price : 'N/A'}</td>
            <td>${item.alert_enabled ? '<i class="bi bi-bell-fill text-warning"></i>' : '<i class="bi bi-bell-slash text-muted"></i>'}</td>
            <td>${new Date(item.added_date).toLocaleDateString()}</td>
            <td class="action-buttons">
                <button class="btn btn-sm btn-outline-danger" onclick="deleteWatchlistItem(${item.watchlist_id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function filterWatchlistByUser() {
    const userId = document.getElementById('watchlistUserFilter').value;
    if (userId === '') {
        await loadWatchlist();
    } else {
        try {
            const response = await fetch(`${API_V1}/users/${userId}/watchlist`);
            const data = await response.json();
            renderWatchlistTable(data.watchlist);
            document.getElementById('watchlistCount').textContent = `${data.watchlist.length} (filtered)`;
        } catch (error) {
            showAlert('Error filtering watchlist: ' + error.message, 'danger');
        }
    }
}

async function deleteWatchlistItem(watchlistId) {
    if (!confirm('Are you sure you want to remove this item from the watchlist?')) return;

    try {
        const response = await fetch(`${API_V1}/watchlist/${watchlistId}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showAlert('Item removed from watchlist', 'success');
            await loadWatchlist();
        } else {
            showAlert('Failed to remove item: ' + result.message, 'danger');
        }
    } catch (error) {
        showAlert('Error removing item: ' + error.message, 'danger');
    }
}

// ==================== HELPER FUNCTIONS ====================

function showLoading(entity) {
    document.getElementById(`${entity}Loading`).style.display = 'block';
    document.getElementById(`${entity}Content`).style.display = 'none';
}

function hideLoading(entity) {
    document.getElementById(`${entity}Loading`).style.display = 'none';
    document.getElementById(`${entity}Content`).style.display = 'block';
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show alert-custom`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);

    setTimeout(() => {
        alert.remove();
    }, 5000);
}

function formatLargeNumber(num) {
    if (num >= 1000000000000) return (num / 1000000000000).toFixed(2) + 'T';
    if (num >= 1000000000) return (num / 1000000000).toFixed(2) + 'B';
    if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(2) + 'K';
    return num.toString();
}

function createModal(title, content, footerButtons = '') {
    return `
        <div class="modal fade" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    <div class="modal-footer">
                        ${footerButtons}
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function showModal(modalHTML) {
    const container = document.getElementById('modalsContainer');
    container.innerHTML = modalHTML;
    const modalElement = container.querySelector('.modal');
    const modal = new bootstrap.Modal(modalElement);
    modal.show();

    modalElement.addEventListener('hidden.bs.modal', function () {
        container.innerHTML = '';
    });
}

function populateUserFilters() {
    const selects = [
        document.getElementById('portfolioUserFilter'),
        document.getElementById('transactionUserFilter'),
        document.getElementById('watchlistUserFilter')
    ];

    selects.forEach(select => {
        select.innerHTML = '<option value="">All Users</option>';
        allUsers.forEach(user => {
            const option = document.createElement('option');
            option.value = user.user_id;
            option.textContent = `${user.username} (ID: ${user.user_id})`;
            select.appendChild(option);
        });
    });
}

function populateTransactionFilters() {
    const select = document.getElementById('transactionStockFilter');
    select.innerHTML = '<option value="">All Stocks</option>';
    allStocks.forEach(stock => {
        const option = document.createElement('option');
        option.value = stock.stock_id;
        option.textContent = `${stock.ticker_symbol} - ${stock.company_name}`;
        select.appendChild(option);
    });
}

// ==================== CREATE FUNCTIONS (Placeholders for modals) ====================

function showCreateStockModal() {
    showAlert('Create Stock modal - to be implemented', 'info');
}

function showCreateUserModal() {
    showAlert('Create User modal - to be implemented', 'info');
}

function showCreatePortfolioModal() {
    showAlert('Create Portfolio modal - to be implemented', 'info');
}

function showCreateTransactionModal() {
    showAlert('Create Transaction modal - to be implemented', 'info');
}

function showCreateWatchlistModal() {
    showAlert('Create Watchlist modal - to be implemented', 'info');
}

function editStock(stockId) {
    showAlert('Edit Stock modal - to be implemented', 'info');
}

function editUserBalance(userId) {
    showAlert('Edit User Balance modal - to be implemented', 'info');
}

console.log('App.js loaded successfully');
