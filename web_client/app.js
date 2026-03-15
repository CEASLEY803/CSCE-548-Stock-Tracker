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
        const response = await fetch(`${API_V1}/watchlist`);
        const data = await response.json();
        allWatchlist = data.watchlist || [];

        document.getElementById('watchlistCount').textContent = allWatchlist.length;
        renderWatchlistTable(allWatchlist);
        hideLoading('watchlist');
    } catch (error) {
        showAlert('Error loading watchlist: ' + error.message, 'danger');
        hideLoading('watchlist');
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

// ==================== CREATE FUNCTIONS ====================

function showCreateStockModal() {
    const modalContent = `
        <form id="createStockForm">
            <div class="mb-3">
                <label class="form-label">Ticker Symbol *</label>
                <input type="text" class="form-control" id="stockTicker" required maxlength="10" placeholder="e.g., AAPL">
            </div>
            <div class="mb-3">
                <label class="form-label">Company Name *</label>
                <input type="text" class="form-control" id="stockCompany" required maxlength="100" placeholder="e.g., Apple Inc.">
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Current Price * ($)</label>
                    <input type="number" class="form-control" id="stockPrice" required step="0.01" min="0.01" placeholder="0.00">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Market Cap *</label>
                    <input type="number" class="form-control" id="stockMarketCap" required min="1" placeholder="1000000000">
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Sector *</label>
                    <select class="form-control" id="stockSector" required>
                        <option value="">Select Sector</option>
                        <option value="Technology">Technology</option>
                        <option value="Healthcare">Healthcare</option>
                        <option value="Finance">Finance</option>
                        <option value="Energy">Energy</option>
                        <option value="Consumer">Consumer</option>
                        <option value="Industrial">Industrial</option>
                    </select>
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Industry</label>
                    <input type="text" class="form-control" id="stockIndustry" maxlength="50" placeholder="Optional">
                </div>
            </div>
        </form>
    `;

    const modal = createModal('Create New Stock', modalContent,
        '<button type="button" class="btn btn-primary" onclick="submitCreateStock()">Create Stock</button>');
    showModal(modal);
}

async function submitCreateStock() {
    const stockData = {
        ticker_symbol: document.getElementById('stockTicker').value.trim().toUpperCase(),
        company_name: document.getElementById('stockCompany').value.trim(),
        current_price: parseFloat(document.getElementById('stockPrice').value),
        market_cap: parseInt(document.getElementById('stockMarketCap').value),
        sector: document.getElementById('stockSector').value,
        industry: document.getElementById('stockIndustry').value.trim() || null
    };

    if (!stockData.ticker_symbol || !stockData.company_name || !stockData.current_price || !stockData.market_cap || !stockData.sector) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/stocks`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(stockData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert('Stock created successfully!', 'success');
            bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            await loadStocks();
        } else {
            showAlert('Error: ' + (result.message || result.detail || 'Failed to create stock'), 'danger');
        }
    } catch (error) {
        showAlert('Error creating stock: ' + error.message, 'danger');
    }
}

function showCreateUserModal() {
    const modalContent = `
        <form id="createUserForm">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Username *</label>
                    <input type="text" class="form-control" id="userUsername" required minlength="3" maxlength="50">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Email *</label>
                    <input type="email" class="form-control" id="userEmail" required>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">First Name *</label>
                    <input type="text" class="form-control" id="userFirstName" required maxlength="50">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Last Name *</label>
                    <input type="text" class="form-control" id="userLastName" required maxlength="50">
                </div>
            </div>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label class="form-label">Password *</label>
                    <input type="password" class="form-control" id="userPassword" required minlength="8">
                </div>
                <div class="col-md-6 mb-3">
                    <label class="form-label">Initial Balance ($)</label>
                    <input type="number" class="form-control" id="userBalance" step="0.01" min="0" value="10000.00">
                </div>
            </div>
        </form>
    `;

    const modal = createModal('Create New User', modalContent,
        '<button type="button" class="btn btn-primary" onclick="submitCreateUser()">Create User</button>');
    showModal(modal);
}

async function submitCreateUser() {
    const userData = {
        username: document.getElementById('userUsername').value.trim(),
        email: document.getElementById('userEmail').value.trim(),
        password: document.getElementById('userPassword').value,
        first_name: document.getElementById('userFirstName').value.trim(),
        last_name: document.getElementById('userLastName').value.trim(),
        initial_balance: parseFloat(document.getElementById('userBalance').value) || 10000.00
    };

    if (!userData.username || !userData.email || !userData.password || !userData.first_name || !userData.last_name) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }

    if (userData.password.length < 8) {
        showAlert('Password must be at least 8 characters', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert('User created successfully!', 'success');
            bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            await loadUsers();
        } else {
            showAlert('Error: ' + (result.message || result.detail || 'Failed to create user'), 'danger');
        }
    } catch (error) {
        showAlert('Error creating user: ' + error.message, 'danger');
    }
}

function showCreatePortfolioModal() {
    const modalContent = `
        <form id="createPortfolioForm">
            <div class="mb-3">
                <label class="form-label">User *</label>
                <select class="form-control" id="portfolioUserId" required>
                    <option value="">Select User</option>
                    ${allUsers.map(u => `<option value="${u.user_id}">${u.username} (ID: ${u.user_id})</option>`).join('')}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Portfolio Name *</label>
                <input type="text" class="form-control" id="portfolioName" required maxlength="100" placeholder="e.g., Growth Portfolio">
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" id="portfolioDescription" rows="3" placeholder="Optional description"></textarea>
            </div>
        </form>
    `;

    const modal = createModal('Create New Portfolio', modalContent,
        '<button type="button" class="btn btn-primary" onclick="submitCreatePortfolio()">Create Portfolio</button>');
    showModal(modal);
}

async function submitCreatePortfolio() {
    const portfolioData = {
        user_id: parseInt(document.getElementById('portfolioUserId').value),
        portfolio_name: document.getElementById('portfolioName').value.trim(),
        description: document.getElementById('portfolioDescription').value.trim() || null
    };

    if (!portfolioData.user_id || !portfolioData.portfolio_name) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/portfolios`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(portfolioData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert('Portfolio created successfully!', 'success');
            bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            await loadPortfolios();
        } else {
            showAlert('Error: ' + (result.message || result.detail || 'Failed to create portfolio'), 'danger');
        }
    } catch (error) {
        showAlert('Error creating portfolio: ' + error.message, 'danger');
    }
}

function showCreateTransactionModal() {
    const modalContent = `
        <form id="createTransactionForm">
            <div class="mb-3">
                <label class="form-label">User *</label>
                <select class="form-control" id="txnUserId" required onchange="filterPortfoliosBySelectedUser()">
                    <option value="">Select User</option>
                    ${allUsers.map(u => `<option value="${u.user_id}">${u.username} (Balance: $${u.account_balance})</option>`).join('')}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Portfolio *</label>
                <select class="form-control" id="txnPortfolioId" required disabled>
                    <option value="">Select a user first</option>
                </select>
                <small class="text-muted">Select a user to see their portfolios</small>
            </div>
            <div class="mb-3">
                <label class="form-label">Stock *</label>
                <select class="form-control" id="txnStockId" required onchange="updateTransactionPrice()">
                    <option value="">Select Stock</option>
                    ${allStocks.map(s => `<option value="${s.stock_id}" data-price="${s.current_price}">${s.ticker_symbol} - ${s.company_name} ($${parseFloat(s.current_price).toFixed(2)})</option>`).join('')}
                </select>
            </div>
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label class="form-label">Type *</label>
                    <select class="form-control" id="txnType" required>
                        <option value="">Select Type</option>
                        <option value="BUY">BUY</option>
                        <option value="SELL">SELL</option>
                    </select>
                </div>
                <div class="col-md-4 mb-3">
                    <label class="form-label">Quantity *</label>
                    <input type="number" class="form-control" id="txnQuantity" required min="1" placeholder="10" onchange="calculateTransactionTotal()">
                </div>
                <div class="col-md-4 mb-3">
                    <label class="form-label">Price/Share * ($)</label>
                    <input type="number" class="form-control" id="txnPrice" required step="0.01" min="0.01" placeholder="0.00" onchange="calculateTransactionTotal()">
                    <small class="text-muted">Auto-filled from stock price</small>
                </div>
            </div>
            <div class="mb-3">
                <div class="alert alert-info" role="alert">
                    <strong>Total Amount:</strong> $<span id="txnTotalAmount">0.00</span>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label">Notes</label>
                <textarea class="form-control" id="txnNotes" rows="2" placeholder="Optional notes"></textarea>
            </div>
        </form>
    `;

    const modal = createModal('Create New Transaction', modalContent,
        '<button type="button" class="btn btn-primary" onclick="submitCreateTransaction()">Create Transaction</button>');
    showModal(modal);
}

// Helper function to filter portfolios when user is selected
function filterPortfoliosBySelectedUser() {
    const userId = parseInt(document.getElementById('txnUserId').value);
    const portfolioSelect = document.getElementById('txnPortfolioId');

    if (!userId) {
        portfolioSelect.disabled = true;
        portfolioSelect.innerHTML = '<option value="">Select a user first</option>';
        return;
    }

    // Filter portfolios for the selected user
    const userPortfolios = allPortfolios.filter(p => p.user_id === userId);

    portfolioSelect.disabled = false;
    if (userPortfolios.length === 0) {
        portfolioSelect.innerHTML = '<option value="">No portfolios found for this user</option>';
    } else {
        portfolioSelect.innerHTML = '<option value="">Select Portfolio</option>' +
            userPortfolios.map(p => `<option value="${p.portfolio_id}">${p.portfolio_name}</option>`).join('');
    }
}

// Helper function to auto-populate price when stock is selected
function updateTransactionPrice() {
    const stockSelect = document.getElementById('txnStockId');
    const priceInput = document.getElementById('txnPrice');

    if (stockSelect.value) {
        const selectedOption = stockSelect.options[stockSelect.selectedIndex];
        const price = selectedOption.getAttribute('data-price');
        priceInput.value = parseFloat(price).toFixed(2);
        calculateTransactionTotal();
    }
}

// Helper function to calculate and display total amount
function calculateTransactionTotal() {
    const quantity = parseInt(document.getElementById('txnQuantity').value) || 0;
    const price = parseFloat(document.getElementById('txnPrice').value) || 0;
    const total = quantity * price;

    const totalDisplay = document.getElementById('txnTotalAmount');
    if (totalDisplay) {
        totalDisplay.textContent = total.toFixed(2);
    }
}

async function submitCreateTransaction() {
    const txnData = {
        user_id: parseInt(document.getElementById('txnUserId').value),
        stock_id: parseInt(document.getElementById('txnStockId').value),
        portfolio_id: parseInt(document.getElementById('txnPortfolioId').value),
        transaction_type: document.getElementById('txnType').value,
        quantity: parseInt(document.getElementById('txnQuantity').value),
        price_per_share: parseFloat(document.getElementById('txnPrice').value),
        notes: document.getElementById('txnNotes').value.trim() || null
    };

    if (!txnData.user_id || !txnData.stock_id || !txnData.portfolio_id || !txnData.transaction_type || !txnData.quantity || !txnData.price_per_share) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/transactions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(txnData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert('Transaction created successfully!', 'success');
            bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            await loadTransactions();
            await loadUsers(); // Refresh to show updated balance
            await loadPortfolios(); // Refresh to show updated portfolio value
        } else {
            showAlert('Error: ' + (result.message || result.detail || 'Failed to create transaction'), 'danger');
        }
    } catch (error) {
        showAlert('Error creating transaction: ' + error.message, 'danger');
    }
}

function showCreateWatchlistModal() {
    const modalContent = `
        <form id="createWatchlistForm">
            <div class="mb-3">
                <label class="form-label">User *</label>
                <select class="form-control" id="watchlistUserId" required>
                    <option value="">Select User</option>
                    ${allUsers.map(u => `<option value="${u.user_id}">${u.username} (ID: ${u.user_id})</option>`).join('')}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Stock *</label>
                <select class="form-control" id="watchlistStockId" required>
                    <option value="">Select Stock</option>
                    ${allStocks.map(s => `<option value="${s.stock_id}">${s.ticker_symbol} - ${s.company_name} ($${s.current_price})</option>`).join('')}
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Target Price ($)</label>
                <input type="number" class="form-control" id="watchlistTargetPrice" step="0.01" min="0.01" placeholder="Optional">
            </div>
            <div class="mb-3">
                <label class="form-label">Notes</label>
                <textarea class="form-control" id="watchlistNotes" rows="2" placeholder="Optional notes"></textarea>
            </div>
            <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" id="watchlistAlert">
                <label class="form-check-label" for="watchlistAlert">
                    Enable Price Alert
                </label>
            </div>
        </form>
    `;

    const modal = createModal('Add to Watchlist', modalContent,
        '<button type="button" class="btn btn-primary" onclick="submitCreateWatchlist()">Add to Watchlist</button>');
    showModal(modal);
}

async function submitCreateWatchlist() {
    const targetPrice = document.getElementById('watchlistTargetPrice').value;
    const watchlistData = {
        user_id: parseInt(document.getElementById('watchlistUserId').value),
        stock_id: parseInt(document.getElementById('watchlistStockId').value),
        target_price: targetPrice ? parseFloat(targetPrice) : null,
        notes: document.getElementById('watchlistNotes').value.trim() || null,
        alert_enabled: document.getElementById('watchlistAlert').checked
    };

    if (!watchlistData.user_id || !watchlistData.stock_id) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/watchlist`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(watchlistData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert('Item added to watchlist successfully!', 'success');
            bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            await loadWatchlist();
        } else {
            showAlert('Error: ' + (result.message || result.detail || 'Failed to add to watchlist'), 'danger');
        }
    } catch (error) {
        showAlert('Error adding to watchlist: ' + error.message, 'danger');
    }
}

// ==================== UPDATE FUNCTIONS ====================

async function editStock(stockId) {
    try {
        const response = await fetch(`${API_V1}/stocks/${stockId}`);
        const stock = await response.json();

        const modalContent = `
            <form id="editStockForm">
                <div class="mb-3">
                    <label class="form-label">Current Price: $${stock.current_price}</label>
                </div>
                <div class="mb-3">
                    <label class="form-label">New Price * ($)</label>
                    <input type="number" class="form-control" id="editStockPrice" required step="0.01" min="0.01"
                           value="${stock.current_price}" placeholder="0.00">
                </div>
                <p class="text-muted small">This will update the stock price for ${stock.ticker_symbol} - ${stock.company_name}</p>
            </form>
        `;

        const modal = createModal('Update Stock Price', modalContent,
            `<button type="button" class="btn btn-warning" onclick="submitEditStock(${stockId})">Update Price</button>`);
        showModal(modal);
    } catch (error) {
        showAlert('Error loading stock: ' + error.message, 'danger');
    }
}

async function submitEditStock(stockId) {
    const newPrice = parseFloat(document.getElementById('editStockPrice').value);

    if (!newPrice || newPrice <= 0) {
        showAlert('Please enter a valid price', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/stocks/${stockId}/price`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_price: newPrice })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert('Stock price updated successfully!', 'success');
            bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            await loadStocks();
        } else {
            showAlert('Error: ' + (result.message || result.detail || 'Failed to update price'), 'danger');
        }
    } catch (error) {
        showAlert('Error updating stock price: ' + error.message, 'danger');
    }
}

async function editUserBalance(userId) {
    try {
        const response = await fetch(`${API_V1}/users/${userId}`);
        const user = await response.json();

        const modalContent = `
            <form id="editBalanceForm">
                <div class="mb-3">
                    <label class="form-label">Current Balance: $${user.account_balance}</label>
                </div>
                <div class="mb-3">
                    <label class="form-label">Operation *</label>
                    <select class="form-control" id="balanceOperation" required>
                        <option value="add">Add Funds</option>
                        <option value="subtract">Subtract Funds</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Amount * ($)</label>
                    <input type="number" class="form-control" id="balanceAmount" required step="0.01" min="0.01" placeholder="0.00">
                </div>
                <p class="text-muted small">This will ${userId}'s account balance for ${user.username}</p>
            </form>
        `;

        const modal = createModal('Update User Balance', modalContent,
            `<button type="button" class="btn btn-warning" onclick="submitEditBalance(${userId})">Update Balance</button>`);
        showModal(modal);
    } catch (error) {
        showAlert('Error loading user: ' + error.message, 'danger');
    }
}

async function submitEditBalance(userId) {
    const amount = parseFloat(document.getElementById('balanceAmount').value);
    const operation = document.getElementById('balanceOperation').value;

    if (!amount || amount <= 0) {
        showAlert('Please enter a valid amount', 'warning');
        return;
    }

    try {
        const response = await fetch(`${API_V1}/users/${userId}/balance`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount: amount, operation: operation })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert('User balance updated successfully!', 'success');
            bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
            await loadUsers();
        } else {
            showAlert('Error: ' + (result.message || result.detail || 'Failed to update balance'), 'danger');
        }
    } catch (error) {
        showAlert('Error updating balance: ' + error.message, 'danger');
    }
}

console.log('App.js loaded successfully');
