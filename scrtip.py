# Create the view expenses template
view_expenses_template = '''{% extends "base.html" %}

{% block title %}View Expenses - ExpenseTracker{% endblock %}

{% block content %}
<div class="view-expenses-page">
    <div class="page-header">
        <div class="header-content">
            <h1 class="page-title">Your Expenses</h1>
            <p class="page-subtitle">Track and analyze your spending patterns</p>
        </div>
        <div class="header-actions">
            <a href="{{ url_for('add_expense') }}" class="btn btn-primary">
                <span class="btn-icon">➕</span>
                Add Expense
            </a>
            <button class="btn btn-secondary" id="exportBtn">
                <span class="btn-icon">📊</span>
                Export
            </button>
        </div>
    </div>

    <!-- Filter Panel -->
    <div class="filter-panel">
        <div class="filter-section">
            <h3 class="filter-title">📅 Time Period</h3>
            <div class="filter-buttons">
                <a href="{{ url_for('view_expenses', filter='today') }}" 
                   class="filter-btn {% if current_filter == 'today' %}active{% endif %}">
                    Today
                </a>
                <a href="{{ url_for('view_expenses', filter='week') }}" 
                   class="filter-btn {% if current_filter == 'week' %}active{% endif %}">
                    This Week
                </a>
                <a href="{{ url_for('view_expenses', filter='month') }}" 
                   class="filter-btn {% if current_filter == 'month' %}active{% endif %}">
                    This Month
                </a>
                <a href="{{ url_for('view_expenses', filter='year') }}" 
                   class="filter-btn {% if current_filter == 'year' %}active{% endif %}">
                    This Year
                </a>
                <a href="{{ url_for('view_expenses', filter='all') }}" 
                   class="filter-btn {% if current_filter == 'all' %}active{% endif %}">
                    All Time
                </a>
            </div>
        </div>

        <div class="filter-section">
            <h3 class="filter-title">📁 Category</h3>
            <div class="category-filter">
                <select id="categoryFilter" class="filter-select">
                    <option value="all" {% if current_category == 'all' %}selected{% endif %}>All Categories</option>
                    {% for category in categories %}
                    <option value="{{ category.category }}" {% if current_category == category.category %}selected{% endif %}>
                        {{ category.category }}
                    </option>
                    {% endfor %}
                </select>
            </div>
        </div>

        <div class="filter-section">
            <h3 class="filter-title">🔄 Sort By</h3>
            <div class="sort-buttons">
                <select id="sortFilter" class="filter-select">
                    <option value="date_desc" {% if current_sort == 'date_desc' %}selected{% endif %}>Latest First</option>
                    <option value="date_asc" {% if current_sort == 'date_asc' %}selected{% endif %}>Oldest First</option>
                    <option value="amount_desc" {% if current_sort == 'amount_desc' %}selected{% endif %}>Highest Amount</option>
                    <option value="amount_asc" {% if current_sort == 'amount_asc' %}selected{% endif %}>Lowest Amount</option>
                    <option value="category" {% if current_sort == 'category' %}selected{% endif %}>By Category</option>
                </select>
            </div>
        </div>
    </div>

    <!-- Summary Cards -->
    <div class="summary-section">
        <div class="summary-cards">
            <div class="summary-card">
                <div class="summary-icon">💰</div>
                <div class="summary-content">
                    <h3 class="summary-value">₹{{ "%.2f"|format(total_amount) }}</h3>
                    <p class="summary-label">Total Amount</p>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-icon">📊</div>
                <div class="summary-content">
                    <h3 class="summary-value">{{ expenses|length }}</h3>
                    <p class="summary-label">Transactions</p>
                </div>
            </div>
            <div class="summary-card">
                <div class="summary-icon">📈</div>
                <div class="summary-content">
                    <h3 class="summary-value">₹{{ "%.0f"|format(total_amount / expenses|length if expenses else 0) }}</h3>
                    <p class="summary-label">Average</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Expenses List -->
    <div class="expenses-section">
        {% if expenses %}
            <div class="expenses-grid">
                {% for expense in expenses %}
                <div class="expense-card" data-category="{{ expense.category }}" data-amount="{{ expense.amount }}">
                    <div class="expense-header">
                        <div class="expense-category-icon">
                            {% if expense.category == 'Food & Dining' %}🍽️
                            {% elif expense.category == 'Transportation' %}🚗
                            {% elif expense.category == 'Shopping' %}🛍️
                            {% elif expense.category == 'Bills & Utilities' %}💡
                            {% elif expense.category == 'Entertainment' %}🎬
                            {% elif expense.category == 'Healthcare' %}🏥
                            {% elif expense.category == 'Groceries' %}🛒
                            {% elif expense.category == 'Gas' %}⛽
                            {% else %}💰{% endif %}
                        </div>
                        <div class="expense-amount">
                            <span class="amount-value">₹{{ "%.2f"|format(expense.amount) }}</span>
                        </div>
                    </div>
                    
                    <div class="expense-body">
                        <h4 class="expense-title">{{ expense.subject }}</h4>
                        <p class="expense-category">{{ expense.category }}</p>
                        {% if expense.description %}
                            <p class="expense-description">{{ expense.description }}</p>
                        {% endif %}
                    </div>
                    
                    <div class="expense-footer">
                        <div class="expense-datetime">
                            <span class="expense-date">{{ expense.expense_date }}</span>
                            <span class="expense-time">{{ expense.expense_time }}</span>
                        </div>
                        <div class="expense-actions">
                            <button class="action-btn edit-btn" data-id="{{ expense.id }}">✏️</button>
                            <button class="action-btn delete-btn" data-id="{{ expense.id }}">🗑️</button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>

            <!-- Pagination (for future use) -->
            <div class="pagination">
                <div class="pagination-info">
                    Showing {{ expenses|length }} expenses
                </div>
            </div>
        {% else %}
            <div class="empty-state">
                <div class="empty-icon">📝</div>
                <h3 class="empty-title">No expenses found</h3>
                <p class="empty-description">
                    {% if current_filter != 'all' %}
                        Try changing your filter settings or add some expenses for this period.
                    {% else %}
                        Start tracking your expenses by adding your first transaction.
                    {% endif %}
                </p>
                <a href="{{ url_for('add_expense') }}" class="btn btn-primary">
                    <span class="btn-icon">➕</span>
                    Add Expense
                </a>
            </div>
        {% endif %}
    </div>
</div>

<!-- Edit Modal (for future use) -->
<div id="editModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 class="modal-title">Edit Expense</h3>
            <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
            <!-- Edit form will be loaded here -->
        </div>
    </div>
</div>

<!-- Delete Confirmation Modal -->
<div id="deleteModal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 class="modal-title">Delete Expense</h3>
            <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
            <p>Are you sure you want to delete this expense? This action cannot be undone.</p>
            <div class="modal-actions">
                <button class="btn btn-secondary" onclick="closeModal('deleteModal')">Cancel</button>
                <button class="btn btn-danger" id="confirmDelete">Delete</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Filter functionality
    document.getElementById('categoryFilter').addEventListener('change', function() {
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('category', this.value);
        window.location.href = currentUrl.toString();
    });

    document.getElementById('sortFilter').addEventListener('change', function() {
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('sort', this.value);
        window.location.href = currentUrl.toString();
    });

    // Export functionality
    document.getElementById('exportBtn').addEventListener('click', function() {
        const expenses = {{ expenses | tojson }};
        let csvContent = "Date,Time,Amount,Category,Subject,Description\\n";
        
        expenses.forEach(expense => {
            const row = [
                expense.expense_date,
                expense.expense_time,
                expense.amount,
                expense.category,
                `"${expense.subject}"`,
                `"${expense.description || ''}"`
            ].join(',');
            csvContent += row + "\\n";
        });
        
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `expenses_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    });

    // Modal functions
    function openModal(modalId) {
        document.getElementById(modalId).style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Edit functionality (placeholder)
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const expenseId = this.getAttribute('data-id');
            // TODO: Implement edit functionality
            alert(`Edit expense #${expenseId} - Coming soon!`);
        });
    });

    // Delete functionality (placeholder)
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const expenseId = this.getAttribute('data-id');
            openModal('deleteModal');
            
            document.getElementById('confirmDelete').onclick = function() {
                // TODO: Implement delete functionality
                alert(`Delete expense #${expenseId} - Coming soon!`);
                closeModal('deleteModal');
            };
        });
    });

    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            e.target.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });

    // Close modal with close button
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.modal').style.display = 'none';
            document.body.style.overflow = 'auto';
        });
    });

    // Search functionality (client-side)
    function addSearchFunctionality() {
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search expenses...';
        searchInput.className = 'search-input';
        
        const filterPanel = document.querySelector('.filter-panel');
        const searchSection = document.createElement('div');
        searchSection.className = 'filter-section';
        searchSection.innerHTML = '<h3 class="filter-title">🔍 Search</h3>';
        searchSection.appendChild(searchInput);
        filterPanel.appendChild(searchSection);
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const expenseCards = document.querySelectorAll('.expense-card');
            
            expenseCards.forEach(card => {
                const title = card.querySelector('.expense-title').textContent.toLowerCase();
                const description = card.querySelector('.expense-description')?.textContent.toLowerCase() || '';
                const category = card.querySelector('.expense-category').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm) || category.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Add search functionality on page load
    document.addEventListener('DOMContentLoaded', function() {
        addSearchFunctionality();
        
        // Animate expense cards
        const cards = document.querySelectorAll('.expense-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('animate-in');
            }, index * 50);
        });
    });
</script>
{% endblock %}'''

# Save the view expenses template
with open('templates/view_expenses.html', 'w') as f:
    f.write(view_expenses_template)

print("✅ View Expenses template (templates/view_expenses.html) created successfully!")