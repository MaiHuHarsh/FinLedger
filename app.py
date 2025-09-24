from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, get_db_connection
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration route"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        
        # Check if user already exists
        existing_user = conn.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?', 
            (username, email)
        ).fetchone()
        
        if existing_user:
            flash('Username or email already exists!', 'error')
        else:
            # Create new user
            hashed_password = generate_password_hash(password)
            conn.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hashed_password)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            conn.close()
            return redirect(url_for('login'))
        
        conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    flash('You have been logged out!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Dashboard route - requires login"""
    if 'user_id' not in session:
        flash('Please login to access the dashboard!', 'error')
        return redirect(url_for('login'))
    
    # Get recent expenses for dashboard preview
    conn = get_db_connection()
    recent_expenses = conn.execute(
        '''SELECT * FROM expenses 
           WHERE user_id = ? 
           ORDER BY expense_date DESC, created_at DESC 
           LIMIT 5''', 
        (session['user_id'],)
    ).fetchall()
    
    # Get total expenses for current month
    current_month = datetime.now().strftime('%Y-%m')
    monthly_total = conn.execute(
        '''SELECT COALESCE(SUM(amount), 0) as total 
           FROM expenses 
           WHERE user_id = ? AND strftime('%Y-%m', expense_date) = ?''',
        (session['user_id'], current_month)
    ).fetchone()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         recent_expenses=recent_expenses, 
                         monthly_total=monthly_total['total'])

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    """Add expense route - requires login"""
    if 'user_id' not in session:
        flash('Please login to add expenses!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        expense_date = request.form['expense_date']
        expense_time = request.form['expense_time']
        amount = float(request.form['amount'])
        subject = request.form['subject']
        description = request.form.get('description', '')
        category = request.form.get('category', 'Other')
        
        # Combine date and time
        datetime_str = f"{expense_date} {expense_time}"
        
        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO expenses 
               (user_id, expense_date, expense_time, amount, subject, description, category) 
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (session['user_id'], expense_date, expense_time, amount, subject, description, category)
        )
        conn.commit()
        conn.close()
        
        flash('Expense added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_expense.html')

@app.route('/view_expenses')
def view_expenses():
    """View expenses route with filtering - requires login"""
    if 'user_id' not in session:
        flash('Please login to view expenses!', 'error')
        return redirect(url_for('login'))
    
    # Get filter parameters
    filter_type = request.args.get('filter', 'all')
    sort_by = request.args.get('sort', 'date_desc')
    category_filter = request.args.get('category', 'all')
    
    conn = get_db_connection()
    
    # Base query
    query = 'SELECT * FROM expenses WHERE user_id = ?'
    params = [session['user_id']]
    
    # Apply filters
    if filter_type == 'today':
        query += ' AND expense_date = date("now")'
    elif filter_type == 'week':
        query += ' AND expense_date >= date("now", "-7 days")'
    elif filter_type == 'month':
        query += ' AND strftime("%Y-%m", expense_date) = strftime("%Y-%m", "now")'
    elif filter_type == 'year':
        query += ' AND strftime("%Y", expense_date) = strftime("%Y", "now")'
    
    # Category filter
    if category_filter != 'all':
        query += ' AND category = ?'
        params.append(category_filter)
    
    # Apply sorting
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
    
    expenses = conn.execute(query, params).fetchall()
    
    # Get categories for filter dropdown
    categories = conn.execute(
        'SELECT DISTINCT category FROM expenses WHERE user_id = ? ORDER BY category',
        (session['user_id'],)
    ).fetchall()
    
    # Calculate totals
    total_amount = sum(expense['amount'] for expense in expenses)
    
    conn.close()
    
    return render_template('view_expenses.html', 
                         expenses=expenses, 
                         categories=categories,
                         total_amount=total_amount,
                         current_filter=filter_type,
                         current_sort=sort_by,
                         current_category=category_filter)

@app.route('/api/expenses/summary')
def expense_summary():
    """API endpoint for expense summary data"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    
    # Monthly summary for current year
    monthly_data = conn.execute(
        '''SELECT strftime('%Y-%m', expense_date) as month, 
                  SUM(amount) as total,
                  COUNT(*) as count
           FROM expenses 
           WHERE user_id = ? AND strftime('%Y', expense_date) = strftime('%Y', 'now')
           GROUP BY strftime('%Y-%m', expense_date)
           ORDER BY month''',
        (session['user_id'],)
    ).fetchall()
    
    # Category summary
    category_data = conn.execute(
        '''SELECT category, SUM(amount) as total, COUNT(*) as count
           FROM expenses 
           WHERE user_id = ?
           GROUP BY category
           ORDER BY total DESC''',
        (session['user_id'],)
    ).fetchall()
    
    conn.close()
    
    return jsonify({
        'monthly': [dict(row) for row in monthly_data],
        'categories': [dict(row) for row in category_data]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)