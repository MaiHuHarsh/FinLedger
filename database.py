import sqlite3
from datetime import datetime
import os

DATABASE = 'expense_manager.db'

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    
    # Create users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create expenses table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            expense_date DATE NOT NULL,
            expense_time TIME NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            subject TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'Other',
            payment_method TEXT DEFAULT 'Cash',
            tags TEXT,
            is_recurring BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    # Create categories table for future use
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            color TEXT DEFAULT '#6366f1',
            icon TEXT DEFAULT 'shopping',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    # Create budgets table for future use
    conn.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            period TEXT DEFAULT 'monthly',  -- monthly, weekly, yearly
            start_date DATE NOT NULL,
            end_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    # Create indexes for better performance
    conn.execute("CREATE INDEX IF NOT EXISTS idx_expenses_user_date ON expenses(user_id, expense_date)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_expenses_amount ON expenses(amount)")
    
    # Insert default categories if they don't exist
    default_categories = [
        'Food & Dining', 'Transportation', 'Shopping', 'Entertainment',
        'Bills & Utilities', 'Healthcare', 'Education', 'Travel',
        'Groceries', 'Gas', 'Other'
    ]
    
    # Create a default admin user for testing (remove in production)
    from werkzeug.security import generate_password_hash
    
    existing_admin = conn.execute(
        'SELECT * FROM users WHERE username = ?', ('admin',)
    ).fetchone()
    
    if not existing_admin:
        admin_password = generate_password_hash('admin123')  # Change this in production
        conn.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            ('admin', 'admin@expensemanager.com', admin_password)
        )
        print("Default admin user created: admin / admin123")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def create_sample_data():
    """Create sample expense data for testing"""
    conn = get_db_connection()
    
    # Get admin user ID
    admin_user = conn.execute(
        'SELECT id FROM users WHERE username = ?', ('admin',)
    ).fetchone()
    
    if admin_user:
        user_id = admin_user['id']
        
        # Sample expenses
        sample_expenses = [
            ('2024-09-20', '09:30', 25.50, 'Breakfast', 'Coffee and sandwich at cafe', 'Food & Dining'),
            ('2024-09-20', '14:15', 450.00, 'Grocery Shopping', 'Weekly grocery shopping', 'Groceries'),
            ('2024-09-21', '18:45', 35.00, 'Gas', 'Fuel for car', 'Transportation'),
            ('2024-09-22', '12:00', 180.00, 'Lunch with friends', 'Restaurant bill', 'Food & Dining'),
            ('2024-09-23', '16:20', 1200.00, 'Phone Bill', 'Monthly phone bill payment', 'Bills & Utilities'),
        ]
        
        for expense in sample_expenses:
            # Check if expense already exists to avoid duplicates
            existing = conn.execute(
                'SELECT * FROM expenses WHERE user_id = ? AND expense_date = ? AND expense_time = ? AND amount = ?',
                (user_id, expense[0], expense[1], expense[2])
            ).fetchone()
            
            if not existing:
                conn.execute(
                    """INSERT INTO expenses 
                       (user_id, expense_date, expense_time, amount, subject, description, category)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (user_id,) + expense
                )
        
        conn.commit()
        print("Sample data created successfully!")
    
    conn.close()

def get_expense_stats(user_id):
    """Get expense statistics for a user"""
    conn = get_db_connection()
    
    # Total expenses
    total = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE user_id = ?',
        (user_id,)
    ).fetchone()['total']
    
    # This month's expenses
    current_month = datetime.now().strftime('%Y-%m')
    monthly = conn.execute(
        'SELECT COALESCE(SUM(amount), 0) as monthly FROM expenses WHERE user_id = ? AND strftime("%Y-%m", expense_date) = ?',
        (user_id, current_month)
    ).fetchone()['monthly']
    
    # Category breakdown
    categories = conn.execute(
        'SELECT category, SUM(amount) as total FROM expenses WHERE user_id = ? GROUP BY category ORDER BY total DESC',
        (user_id,)
    ).fetchall()
    
    conn.close()
    
    return {
        'total': total,
        'monthly': monthly,
        'categories': [dict(cat) for cat in categories]
    }

if __name__ == '__main__':
    init_db()
    create_sample_data()