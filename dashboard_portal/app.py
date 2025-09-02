#!/usr/bin/env python3
"""
Bevco Executive Dashboard Portal
Modern web-based dashboard system with AI chat functionality
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import sqlite3
import pandas as pd
import json
import os
import secrets
from datetime import datetime, timedelta
import openai
from werkzeug.security import generate_password_hash, check_password_hash
import threading
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
DATABASE_PATH = 'data/bevco_dashboard.db'
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'demo-key')  # Set your OpenAI API key

class DashboardData:
    def __init__(self):
        self.init_database()
        self.load_sample_data()
    
    def init_database(self):
        """Initialize SQLite database with tables"""
        os.makedirs('data', exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sales data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                region TEXT NOT NULL,
                product_category TEXT NOT NULL,
                vendor TEXT NOT NULL,
                customer_type TEXT NOT NULL,
                sales_amount REAL NOT NULL,
                profit_amount REAL NOT NULL,
                quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # KPI data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpi_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                target_value REAL NOT NULL,
                date DATE NOT NULL,
                department TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Chat messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT NOT NULL,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user
        admin_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@bevco.com', admin_hash, 'admin'))
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """Load sample business data"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute('SELECT COUNT(*) FROM sales_data')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Generate sample sales data
        regions = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Free State']
        categories = ['Beer', 'Wine', 'Spirits', 'Soft Drinks', 'Water']
        vendors = ['SAB Miller', 'Distell', 'Coca-Cola', 'Pepsi', 'Local Brands']
        customer_types = ['Retail', 'Wholesale', 'On-Trade', 'Export']
        
        sales_data = []
        start_date = datetime.now() - timedelta(days=180)
        
        for i in range(5000):  # Generate 5000 sample records
            date = start_date + timedelta(days=random.randint(0, 180))
            region = random.choice(regions)
            category = random.choice(categories)
            vendor = random.choice(vendors)
            customer_type = random.choice(customer_types)
            
            # Generate realistic sales amounts based on category
            base_amount = {
                'Beer': random.uniform(1000, 5000),
                'Wine': random.uniform(2000, 8000),
                'Spirits': random.uniform(3000, 12000),
                'Soft Drinks': random.uniform(500, 3000),
                'Water': random.uniform(200, 1500)
            }[category]
            
            sales_amount = round(base_amount, 2)
            profit_margin = random.uniform(0.15, 0.35)
            profit_amount = round(sales_amount * profit_margin, 2)
            quantity = random.randint(10, 500)
            
            sales_data.append((
                date.strftime('%Y-%m-%d'),
                region,
                category,
                vendor,
                customer_type,
                sales_amount,
                profit_amount,
                quantity
            ))
        
        cursor.executemany('''
            INSERT INTO sales_data (date, region, product_category, vendor, customer_type, sales_amount, profit_amount, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sales_data)
        
        # Generate KPI data
        kpi_data = []
        departments = ['Sales', 'Marketing', 'Finance', 'Operations', 'HR']
        metrics = [
            ('Total Sales', 50000000, 45000000),
            ('Profit Margin %', 25.5, 30.0),
            ('Customer Satisfaction', 87.3, 90.0),
            ('Employee Retention %', 92.1, 95.0),
            ('Inventory Turnover', 8.2, 12.0)
        ]
        
        for dept in departments:
            for metric_name, current, target in metrics:
                kpi_data.append((
                    metric_name,
                    current + random.uniform(-5, 5),
                    target,
                    datetime.now().strftime('%Y-%m-%d'),
                    dept
                ))
        
        cursor.executemany('''
            INSERT INTO kpi_data (metric_name, metric_value, target_value, date, department)
            VALUES (?, ?, ?, ?, ?)
        ''', kpi_data)
        
        conn.commit()
        conn.close()

# Initialize data
dashboard_data = DashboardData()

# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash, role FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            session['role'] = user[2]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/sales')
@login_required
def sales():
    return render_template('sales.html', username=session.get('username'))

@app.route('/finance')
@login_required
def finance():
    return render_template('finance.html', username=session.get('username'))

@app.route('/operations')
@login_required
def operations():
    return render_template('operations.html', username=session.get('username'))

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', username=session.get('username'))

# API Routes
@app.route('/api/dashboard_data')
@login_required
def api_dashboard_data():
    """Get dashboard summary data"""
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Total sales
    total_sales = pd.read_sql_query(
        'SELECT SUM(sales_amount) as total FROM sales_data', conn
    ).iloc[0]['total']
    
    # Total profit
    total_profit = pd.read_sql_query(
        'SELECT SUM(profit_amount) as total FROM sales_data', conn
    ).iloc[0]['total']
    
    # Sales by region
    sales_by_region = pd.read_sql_query('''
        SELECT region, SUM(sales_amount) as sales
        FROM sales_data
        GROUP BY region
        ORDER BY sales DESC
    ''', conn)
    
    # Sales trend (last 30 days)
    sales_trend = pd.read_sql_query('''
        SELECT DATE(date) as date, SUM(sales_amount) as sales
        FROM sales_data
        WHERE date >= date('now', '-30 days')
        GROUP BY DATE(date)
        ORDER BY date
    ''', conn)
    
    # Top products
    top_products = pd.read_sql_query('''
        SELECT product_category, SUM(sales_amount) as sales
        FROM sales_data
        GROUP BY product_category
        ORDER BY sales DESC
        LIMIT 5
    ''', conn)
    
    conn.close()
    
    return jsonify({
        'total_sales': round(total_sales, 2) if total_sales else 0,
        'total_profit': round(total_profit, 2) if total_profit else 0,
        'profit_margin': round((total_profit / total_sales * 100), 2) if total_sales > 0 else 0,
        'sales_by_region': sales_by_region.to_dict('records'),
        'sales_trend': sales_trend.to_dict('records'),
        'top_products': top_products.to_dict('records')
    })

@app.route('/api/sales_data')
@login_required
def api_sales_data():
    """Get detailed sales data"""
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Sales by category over time
    category_trend = pd.read_sql_query('''
        SELECT product_category, DATE(date) as date, SUM(sales_amount) as sales
        FROM sales_data
        WHERE date >= date('now', '-90 days')
        GROUP BY product_category, DATE(date)
        ORDER BY date, product_category
    ''', conn)
    
    # Sales by vendor
    vendor_sales = pd.read_sql_query('''
        SELECT vendor, SUM(sales_amount) as sales, SUM(profit_amount) as profit
        FROM sales_data
        GROUP BY vendor
        ORDER BY sales DESC
    ''', conn)
    
    # Customer type analysis
    customer_analysis = pd.read_sql_query('''
        SELECT customer_type, SUM(sales_amount) as sales, COUNT(*) as transactions
        FROM sales_data
        GROUP BY customer_type
        ORDER BY sales DESC
    ''', conn)
    
    conn.close()
    
    return jsonify({
        'category_trend': category_trend.to_dict('records'),
        'vendor_sales': vendor_sales.to_dict('records'),
        'customer_analysis': customer_analysis.to_dict('records')
    })

@app.route('/api/financial_data')
@login_required
def api_financial_data():
    """Get financial analysis data"""
    conn = sqlite3.connect(DATABASE_PATH)
    
    # Monthly financial summary
    monthly_summary = pd.read_sql_query('''
        SELECT 
            strftime('%Y-%m', date) as month,
            SUM(sales_amount) as revenue,
            SUM(profit_amount) as profit,
            COUNT(*) as transactions
        FROM sales_data
        WHERE date >= date('now', '-12 months')
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
    ''', conn)
    
    # Profit margin by category
    margin_by_category = pd.read_sql_query('''
        SELECT 
            product_category,
            SUM(sales_amount) as sales,
            SUM(profit_amount) as profit,
            ROUND(SUM(profit_amount) / SUM(sales_amount) * 100, 2) as margin_percent
        FROM sales_data
        GROUP BY product_category
        ORDER BY margin_percent DESC
    ''', conn)
    
    conn.close()
    
    return jsonify({
        'monthly_summary': monthly_summary.to_dict('records'),
        'margin_by_category': margin_by_category.to_dict('records')
    })

@app.route('/api/kpi_data')
@login_required
def api_kpi_data():
    """Get KPI data"""
    conn = sqlite3.connect(DATABASE_PATH)
    
    kpis = pd.read_sql_query('''
        SELECT metric_name, metric_value, target_value, department
        FROM kpi_data
        ORDER BY department, metric_name
    ''', conn)
    
    conn.close()
    
    return jsonify({
        'kpis': kpis.to_dict('records')
    })

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handle AI chat requests"""
    user_message = request.json.get('message', '')
    user_id = session.get('user_id')
    
    # Simple AI response (replace with OpenAI API call)
    ai_response = generate_ai_response(user_message)
    
    # Save chat to database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_messages (user_id, message, response)
        VALUES (?, ?, ?)
    ''', (user_id, user_message, ai_response))
    conn.commit()
    conn.close()
    
    return jsonify({
        'response': ai_response,
        'timestamp': datetime.now().isoformat()
    })

def generate_ai_response(message):
    """Generate AI response (demo version)"""
    message_lower = message.lower()
    
    # Simple keyword-based responses
    if 'sales' in message_lower:
        return "Based on our current data, total sales are performing well at R45.2M, which is 8.2% above last year. The Western Cape and Gauteng regions are leading performance. Would you like me to dive deeper into any specific region or product category?"
    
    elif 'profit' in message_lower:
        return "Our profit margin is currently at 25.5%, slightly below our target of 30%. Beer and spirits categories are performing best with margins of 28% and 32% respectively. I recommend focusing on optimizing soft drinks margins."
    
    elif 'region' in message_lower:
        return "Regional performance shows Gauteng leading with R12.8M (28.4%), followed by Western Cape at R9.6M (21.3%). KwaZulu-Natal and Eastern Cape show growth opportunities. Would you like a detailed regional breakdown?"
    
    elif 'inventory' in message_lower:
        return "Current inventory turnover is at 8.2 times per year, below our target of 12. Stock levels are healthy across all warehouses, but we have slow-moving items in the water category that need attention."
    
    elif 'employee' in message_lower or 'hr' in message_lower:
        return "Employee retention is strong at 92.1%, close to our 95% target. Sales team productivity is up 15% this quarter. The operations team could benefit from additional training on new inventory systems."
    
    elif 'budget' in message_lower:
        return "We're currently 3.2% over budget in marketing spend but 2.1% under in operations. Overall budget variance is +0.8%, which is within acceptable limits. Q4 forecast looks positive."
    
    elif 'customer' in message_lower:
        return "Customer satisfaction is at 87.3%, approaching our 90% target. Retail customers show highest satisfaction (91%), while wholesale needs improvement (83%). Recent feedback highlights delivery speed as a key concern."
    
    else:
        return f"I understand you're asking about '{message}'. I can help you analyze sales performance, financial metrics, regional data, inventory levels, employee productivity, budget variance, and customer insights. What specific aspect would you like to explore?"

# WebSocket events for real-time updates
@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        emit('status', {'msg': f"Welcome {session.get('username')}! Real-time updates are now active."})

@socketio.on('disconnect')
def handle_disconnect():
    pass

# Background task to simulate real-time data updates
def background_thread():
    """Send periodic updates to connected clients"""
    while True:
        time.sleep(30)  # Update every 30 seconds
        
        # Generate random update
        updates = [
            {'type': 'sales', 'message': f'New sale recorded: R{random.randint(1000, 5000)} in {random.choice(["Gauteng", "Western Cape", "KwaZulu-Natal"])}'},
            {'type': 'alert', 'message': f'Inventory alert: {random.choice(["Beer", "Wine", "Spirits"])} stock running low in JHB warehouse'},
            {'type': 'kpi', 'message': f'KPI Update: Customer satisfaction increased to {random.uniform(85, 95):.1f}%'}
        ]
        
        update = random.choice(updates)
        socketio.emit('real_time_update', update)

# Start background thread
thread = threading.Thread(target=background_thread)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    print("🚀 Starting Bevco Executive Dashboard Portal...")
    print("📊 Dashboard URL: http://localhost:5000")
    print("👤 Default Login: admin / admin123")
    print("🤖 AI Chat Assistant: Available")
    print("📱 Real-time Updates: Active")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)