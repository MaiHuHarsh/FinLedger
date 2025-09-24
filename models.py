"""
ExpenseTracker Models
Database models and schema definitions for the expense management application
"""

import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

class BaseModel:
    """Base model class with common functionality"""

    def __init__(self):
        self.conn = None

    def get_connection(self):
        """Get database connection"""
        if not self.conn:
            self.conn = get_db_connection()
        return self.conn

    def close_connection(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None

class User(BaseModel):
    """User model for authentication and user management"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.username = None
        self.email = None
        self.password_hash = None
        self.created_at = None
        self.updated_at = None

    @classmethod
    def create_user(cls, username, email, password):
        """Create a new user"""
        user = cls()
        conn = user.get_connection()

        try:
            # Check if user already exists
            existing = conn.execute(
                'SELECT id FROM users WHERE username = ? OR email = ?',
                (username, email)
            ).fetchone()

            if existing:
                return None, "Username or email already exists"

            # Create new user
            password_hash = generate_password_hash(password)
            insert_query = """INSERT INTO users (username, email, password, created_at, updated_at) 
                             VALUES (?, ?, ?, ?, ?)"""
            cursor = conn.execute(
                insert_query,
                (username, email, password_hash, datetime.now(), datetime.now())
            )
            conn.commit()

            # Load the created user
            user.id = cursor.lastrowid
            user.username = username
            user.email = email
            user.password_hash = password_hash
            user.created_at = datetime.now()
            user.updated_at = datetime.now()

            return user, "User created successfully"

        except sqlite3.Error as e:
            return None, f"Database error: {str(e)}"
        finally:
            user.close_connection()

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate user with username and password"""
        user = cls()
        conn = user.get_connection()

        try:
            row = conn.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()

            if row and check_password_hash(row['password'], password):
                user.id = row['id']
                user.username = row['username']
                user.email = row['email']
                user.password_hash = row['password']
                user.created_at = row['created_at']
                user.updated_at = row['updated_at']
                return user, "Authentication successful"

            return None, "Invalid username or password"

        except sqlite3.Error as e:
            return None, f"Database error: {str(e)}"
        finally:
            user.close_connection()

    @classmethod
    def get_by_id(cls, user_id):
        """Get user by ID"""
        user = cls()
        conn = user.get_connection()

        try:
            row = conn.execute(
                'SELECT * FROM users WHERE id = ?',
                (user_id,)
            ).fetchone()

            if row:
                user.id = row['id']
                user.username = row['username']
                user.email = row['email']
                user.password_hash = row['password']
                user.created_at = row['created_at']
                user.updated_at = row['updated_at']
                return user

            return None

        except sqlite3.Error:
            return None
        finally:
            user.close_connection()

    def update_password(self, new_password):
        """Update user password"""
        conn = self.get_connection()

        try:
            password_hash = generate_password_hash(new_password)
            conn.execute(
                'UPDATE users SET password = ?, updated_at = ? WHERE id = ?',
                (password_hash, datetime.now(), self.id)
            )
            conn.commit()
            self.password_hash = password_hash
            self.updated_at = datetime.now()
            return True, "Password updated successfully"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            self.close_connection()

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Expense(BaseModel):
    """Expense model for expense management"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.user_id = None
        self.expense_date = None
        self.expense_time = None
        self.amount = None
        self.subject = None
        self.description = None
        self.category = None
        self.payment_method = None
        self.tags = None
        self.is_recurring = False
        self.created_at = None
        self.updated_at = None

    @classmethod
    def create_expense(cls, user_id, expense_date, expense_time, amount, subject, 
                      description=None, category='Other', payment_method='Cash', 
                      tags=None, is_recurring=False):
        """Create a new expense"""
        expense = cls()
        conn = expense.get_connection()

        try:
            insert_query = """INSERT INTO expenses 
                             (user_id, expense_date, expense_time, amount, subject, description, 
                              category, payment_method, tags, is_recurring, created_at, updated_at) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor = conn.execute(
                insert_query,
                (user_id, expense_date, expense_time, amount, subject, description,
                 category, payment_method, tags, is_recurring, datetime.now(), datetime.now())
            )
            conn.commit()

            # Load the created expense
            expense.id = cursor.lastrowid
            expense.user_id = user_id
            expense.expense_date = expense_date
            expense.expense_time = expense_time
            expense.amount = amount
            expense.subject = subject
            expense.description = description
            expense.category = category
            expense.payment_method = payment_method
            expense.tags = tags
            expense.is_recurring = is_recurring
            expense.created_at = datetime.now()
            expense.updated_at = datetime.now()

            return expense, "Expense created successfully"

        except sqlite3.Error as e:
            return None, f"Database error: {str(e)}"
        finally:
            expense.close_connection()

    @classmethod
    def get_by_user(cls, user_id, limit=None, offset=0, filters=None):
        """Get expenses by user with optional filters"""
        conn = get_db_connection()

        try:
            query = 'SELECT * FROM expenses WHERE user_id = ?'
            params = [user_id]

            # Apply filters
            if filters:
                if filters.get('category') and filters['category'] != 'all':
                    query += ' AND category = ?'
                    params.append(filters['category'])

                if filters.get('date_from'):
                    query += ' AND expense_date >= ?'
                    params.append(filters['date_from'])

                if filters.get('date_to'):
                    query += ' AND expense_date <= ?'
                    params.append(filters['date_to'])

                if filters.get('min_amount'):
                    query += ' AND amount >= ?'
                    params.append(filters['min_amount'])

                if filters.get('max_amount'):
                    query += ' AND amount <= ?'
                    params.append(filters['max_amount'])

                if filters.get('search'):
                    query += ' AND (subject LIKE ? OR description LIKE ?)'
                    search_term = f"%{filters['search']}%"
                    params.extend([search_term, search_term])

            # Apply sorting
            sort_by = filters.get('sort_by', 'date_desc') if filters else 'date_desc'
            if sort_by == 'date_desc':
                query += ' ORDER BY expense_date DESC, expense_time DESC'
            elif sort_by == 'date_asc':
                query += ' ORDER BY expense_date ASC, expense_time ASC'
            elif sort_by == 'amount_desc':
                query += ' ORDER BY amount DESC'
            elif sort_by == 'amount_asc':
                query += ' ORDER BY amount ASC'
            elif sort_by == 'category':
                query += ' ORDER BY category, expense_date DESC'

            # Apply pagination
            if limit:
                query += ' LIMIT ? OFFSET ?'
                params.extend([limit, offset])

            rows = conn.execute(query, params).fetchall()

            expenses = []
            for row in rows:
                expense = cls()
                expense.load_from_row(row)
                expenses.append(expense)

            return expenses, "Success"

        except sqlite3.Error as e:
            return [], f"Database error: {str(e)}"
        finally:
            conn.close()

    @classmethod
    def get_by_id(cls, expense_id, user_id=None):
        """Get expense by ID"""
        expense = cls()
        conn = expense.get_connection()

        try:
            query = 'SELECT * FROM expenses WHERE id = ?'
            params = [expense_id]

            if user_id:
                query += ' AND user_id = ?'
                params.append(user_id)

            row = conn.execute(query, params).fetchone()

            if row:
                expense.load_from_row(row)
                return expense

            return None

        except sqlite3.Error:
            return None
        finally:
            expense.close_connection()

    @classmethod
    def get_statistics(cls, user_id, period=None):
        """Get expense statistics for a user"""
        conn = get_db_connection()

        try:
            stats = {}

            # Total expenses
            row = conn.execute(
                'SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total FROM expenses WHERE user_id = ?',
                (user_id,)
            ).fetchone()
            stats['total_expenses'] = row['count']
            stats['total_amount'] = row['total']

            # Current month
            current_month = datetime.now().strftime('%Y-%m')
            monthly_query = """SELECT COUNT(*) as count, COALESCE(SUM(amount), 0) as total 
                              FROM expenses WHERE user_id = ? AND strftime('%Y-%m', expense_date) = ?"""
            row = conn.execute(monthly_query, (user_id, current_month)).fetchone()
            stats['monthly_expenses'] = row['count']
            stats['monthly_amount'] = row['total']

            # Category breakdown
            category_query = """SELECT category, COUNT(*) as count, SUM(amount) as total
                               FROM expenses WHERE user_id = ? 
                               GROUP BY category ORDER BY total DESC"""
            category_rows = conn.execute(category_query, (user_id,)).fetchall()
            stats['categories'] = [dict(row) for row in category_rows]

            # Monthly trend (last 12 months)
            trend_query = """SELECT strftime('%Y-%m', expense_date) as month, 
                                   COUNT(*) as count, SUM(amount) as total
                            FROM expenses WHERE user_id = ? 
                            AND expense_date >= date('now', '-12 months')
                            GROUP BY strftime('%Y-%m', expense_date)
                            ORDER BY month"""
            monthly_rows = conn.execute(trend_query, (user_id,)).fetchall()
            stats['monthly_trend'] = [dict(row) for row in monthly_rows]

            return stats, "Success"

        except sqlite3.Error as e:
            return {}, f"Database error: {str(e)}"
        finally:
            conn.close()

    def update(self, **kwargs):
        """Update expense fields"""
        conn = self.get_connection()

        try:
            # Build dynamic update query
            fields = []
            values = []

            for field, value in kwargs.items():
                if hasattr(self, field) and field != 'id':
                    fields.append(f"{field} = ?")
                    values.append(value)
                    setattr(self, field, value)

            if not fields:
                return False, "No valid fields to update"

            # Add updated_at
            fields.append("updated_at = ?")
            values.append(datetime.now())
            values.append(self.id)

            query = f"UPDATE expenses SET {', '.join(fields)} WHERE id = ?"
            conn.execute(query, values)
            conn.commit()

            self.updated_at = datetime.now()
            return True, "Expense updated successfully"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            self.close_connection()

    def delete(self):
        """Delete expense"""
        conn = self.get_connection()

        try:
            conn.execute('DELETE FROM expenses WHERE id = ?', (self.id,))
            conn.commit()
            return True, "Expense deleted successfully"

        except sqlite3.Error as e:
            return False, f"Database error: {str(e)}"
        finally:
            self.close_connection()

    def load_from_row(self, row):
        """Load expense data from database row"""
        self.id = row['id']
        self.user_id = row['user_id']
        self.expense_date = row['expense_date']
        self.expense_time = row['expense_time']
        self.amount = row['amount']
        self.subject = row['subject']
        self.description = row['description']
        self.category = row['category']
        self.payment_method = row['payment_method']
        self.tags = row['tags']
        self.is_recurring = row['is_recurring']
        self.created_at = row['created_at']
        self.updated_at = row['updated_at']

    def to_dict(self):
        """Convert expense object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'expense_date': self.expense_date,
            'expense_time': self.expense_time,
            'amount': self.amount,
            'subject': self.subject,
            'description': self.description,
            'category': self.category,
            'payment_method': self.payment_method,
            'tags': self.tags,
            'is_recurring': self.is_recurring,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# Utility functions
def format_currency(amount, currency='INR'):
    """Format amount as currency"""
    if currency == 'INR':
        return f"₹{amount:,.2f}"
    else:
        return f"{currency} {amount:,.2f}"

def validate_expense_data(data):
    """Validate expense data"""
    errors = []

    if not data.get('amount'):
        errors.append("Amount is required")
    elif not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        errors.append("Amount must be a positive number")
    elif data['amount'] > 1000000:
        errors.append("Amount cannot exceed ₹10,00,000")

    if not data.get('subject') or not data['subject'].strip():
        errors.append("Subject is required")
    elif len(data['subject']) > 100:
        errors.append("Subject cannot exceed 100 characters")

    if not data.get('expense_date'):
        errors.append("Expense date is required")

    if not data.get('expense_time'):
        errors.append("Expense time is required")

    if data.get('description') and len(data['description']) > 500:
        errors.append("Description cannot exceed 500 characters")

    return errors

def get_expense_categories():
    """Get list of available expense categories"""
    return [
        'Food & Dining',
        'Transportation', 
        'Shopping',
        'Bills & Utilities',
        'Entertainment',
        'Healthcare',
        'Education',
        'Travel',
        'Groceries',
        'Gas',
        'Other'
    ]

if __name__ == '__main__':
    # Test the models
    print("Testing ExpenseTracker Models...")

    # Test user creation
    user, message = User.create_user('testuser', 'test@example.com', 'password123')
    if user:
        print(f"✅ User created: {user.username}")

        # Test expense creation
        expense, message = Expense.create_expense(
            user.id, '2024-09-24', '14:30', 250.00, 
            'Test Lunch', 'Testing expense creation', 'Food & Dining'
        )

        if expense:
            print(f"✅ Expense created: {expense.subject} - ₹{expense.amount}")
        else:
            print(f"❌ Expense creation failed: {message}")
    else:
        print(f"❌ User creation failed: {message}")
