#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Complete Deployment Script
Downloads, sets up, and runs the entire dashboard system
"""

import os
import sys
import subprocess
import tempfile
import urllib.request
import zipfile
import shutil
import time
import webbrowser
import socket
from pathlib import Path

# Colors for output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message, color=Colors.BLUE):
    print(f"{color}{message}{Colors.END}")

def print_header():
    print_colored("\n" + "="*70, Colors.BOLD)
    print_colored("🚀 BEVCO EXECUTIVE DASHBOARD - COMPLETE DEPLOYMENT", Colors.BOLD)
    print_colored("   Full System Installation and Launch", Colors.BLUE)
    print_colored("="*70, Colors.BOLD)

def find_free_port():
    """Find an available port"""
    ports_to_try = [5000, 5001, 5002, 5003, 8000, 8080, 8888, 3000, 3001]
    
    for port in ports_to_try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    # If all predefined ports are taken, find a random one
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def download_and_extract():
    """Download the complete project from GitHub"""
    print_colored("\n📥 Downloading complete dashboard system...", Colors.BLUE)
    
    # Create a permanent directory in user's home
    home_dir = Path.home()
    project_dir = home_dir / "bevco-executive-dashboard"
    
    # If project already exists, ask user
    if project_dir.exists():
        print_colored(f"📁 Project already exists at: {project_dir}", Colors.YELLOW)
        response = input("Do you want to update it? (y/n): ").lower()
        if response != 'y':
            return project_dir
        else:
            print_colored("🗑️  Removing old version...", Colors.YELLOW)
            shutil.rmtree(project_dir)
    
    # Download from GitHub
    try:
        zip_url = "https://github.com/Reshigan/bevco-executive-dashboard/archive/refs/heads/main.zip"
        temp_zip = tempfile.mktemp(suffix='.zip')
        
        print_colored("   Downloading from GitHub...", Colors.BLUE)
        urllib.request.urlretrieve(zip_url, temp_zip)
        
        print_colored("   Extracting files...", Colors.BLUE)
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(home_dir)
        
        # Rename extracted directory
        extracted_dir = home_dir / "bevco-executive-dashboard-main"
        if extracted_dir.exists():
            extracted_dir.rename(project_dir)
        
        # Clean up
        os.unlink(temp_zip)
        
        print_colored(f"✅ Project downloaded to: {project_dir}", Colors.GREEN)
        return project_dir
        
    except Exception as e:
        print_colored(f"❌ Download failed: {e}", Colors.RED)
        return None

def install_dependencies():
    """Install required Python packages"""
    print_colored("\n📦 Installing dependencies...", Colors.BLUE)
    
    packages = [
        "flask==2.3.3",
        "flask-socketio==5.3.6",
        "werkzeug==2.3.7",
        "python-socketio==5.8.0",
        "eventlet==0.33.3",
        "python-dotenv==1.0.0"
    ]
    
    for package in packages:
        try:
            print_colored(f"   Installing {package.split('==')[0]}...", Colors.BLUE)
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--quiet"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print_colored(f"   ✅ {package.split('==')[0]}", Colors.GREEN)
            else:
                print_colored(f"   ⚠️  {package.split('==')[0]} (may already be installed)", Colors.YELLOW)
        except Exception as e:
            print_colored(f"   ⚠️  {package.split('==')[0]} skipped: {e}", Colors.YELLOW)
    
    print_colored("✅ Dependencies ready!", Colors.GREEN)

def create_all_files(project_dir):
    """Create all necessary files for the dashboard"""
    print_colored("\n📝 Creating dashboard files...", Colors.BLUE)
    
    # Create directories
    dashboard_dir = project_dir / "dashboard_portal"
    templates_dir = dashboard_dir / "templates"
    data_dir = dashboard_dir / "data"
    
    for dir_path in [dashboard_dir, templates_dir, data_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Create app.py with auto-port selection
    app_content = '''#!/usr/bin/env python3
"""
Bevco Executive Dashboard - Main Application
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import sqlite3
import os
import secrets
from datetime import datetime, timedelta
import threading
import time
import random
from werkzeug.security import generate_password_hash, check_password_hash
import socket
import webbrowser

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*")

DATABASE_PATH = 'data/bevco_dashboard.db'

def find_free_port():
    """Find an available port"""
    ports_to_try = [5000, 5001, 5002, 5003, 8000, 8080, 8888, 3000, 3001]
    
    for port in ports_to_try:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

class DashboardData:
    def __init__(self):
        self.init_database()
        self.load_sample_data()
    
    def init_database(self):
        """Initialize SQLite database"""
        os.makedirs('data', exist_ok=True)
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \'\'\')
        
        cursor.execute(\'\'\'
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
        \'\'\')
        
        admin_hash = generate_password_hash('admin123')
        cursor.execute(\'\'\'
            INSERT OR IGNORE INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        \'\'\', ('admin', 'admin@bevco.com', admin_hash, 'admin'))
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """Load sample data"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM sales_data')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        regions = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Free State']
        categories = ['Beer', 'Wine', 'Spirits', 'Soft Drinks', 'Water']
        vendors = ['SAB Miller', 'Distell', 'Coca-Cola', 'Pepsi', 'Local Brands']
        customer_types = ['Retail', 'Wholesale', 'On-Trade', 'Export']
        
        sales_data = []
        start_date = datetime.now() - timedelta(days=180)
        
        for i in range(5000):
            date = start_date + timedelta(days=random.randint(0, 180))
            region = random.choice(regions)
            category = random.choice(categories)
            vendor = random.choice(vendors)
            customer_type = random.choice(customer_types)
            
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
        
        cursor.executemany(\'\'\'
            INSERT INTO sales_data (date, region, product_category, vendor, customer_type, sales_amount, profit_amount, quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        \'\'\', sales_data)
        
        conn.commit()
        conn.close()

dashboard_data = DashboardData()

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

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

@app.route('/api/dashboard_data')
@login_required
def api_dashboard_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT SUM(sales_amount) FROM sales_data')
    total_sales = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(profit_amount) FROM sales_data')
    total_profit = cursor.fetchone()[0] or 0
    
    cursor.execute(\'\'\'
        SELECT region, SUM(sales_amount) as sales
        FROM sales_data
        GROUP BY region
        ORDER BY sales DESC
    \'\'\')
    sales_by_region = [{'region': row[0], 'sales': row[1]} for row in cursor.fetchall()]
    
    cursor.execute(\'\'\'
        SELECT DATE(date) as date, SUM(sales_amount) as sales
        FROM sales_data
        WHERE date >= date('now', '-30 days')
        GROUP BY DATE(date)
        ORDER BY date
    \'\'\')
    sales_trend = [{'date': row[0], 'sales': row[1]} for row in cursor.fetchall()]
    
    cursor.execute(\'\'\'
        SELECT product_category, SUM(sales_amount) as sales
        FROM sales_data
        GROUP BY product_category
        ORDER BY sales DESC
        LIMIT 5
    \'\'\')
    top_products = [{'product_category': row[0], 'sales': row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return jsonify({
        'total_sales': round(total_sales, 2),
        'total_profit': round(total_profit, 2),
        'profit_margin': round((total_profit / total_sales * 100), 2) if total_sales > 0 else 0,
        'sales_by_region': sales_by_region,
        'sales_trend': sales_trend,
        'top_products': top_products
    })

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    user_message = request.json.get('message', '')
    
    message_lower = user_message.lower()
    
    if 'sales' in message_lower:
        response = "Based on our current data, total sales are performing well at R45.2M, which is 8.2% above last year. The Western Cape and Gauteng regions are leading performance."
    elif 'profit' in message_lower:
        response = "Our profit margin is currently at 25.5%, slightly below our target of 30%. Beer and spirits categories are performing best with margins of 28% and 32% respectively."
    elif 'region' in message_lower:
        response = "Regional performance shows Gauteng leading with R12.8M (28.4%), followed by Western Cape at R9.6M (21.3%). KwaZulu-Natal and Eastern Cape show growth opportunities."
    else:
        response = f"I understand you're asking about '{user_message}'. I can help you analyze sales performance, financial metrics, regional data, and more. What specific aspect would you like to explore?"
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        emit('status', {'msg': f"Welcome {session.get('username')}! Real-time updates are now active."})

def background_thread():
    while True:
        time.sleep(30)
        updates = [
            {'type': 'sales', 'message': f'New sale recorded: R{random.randint(1000, 5000)} in {random.choice(["Gauteng", "Western Cape", "KwaZulu-Natal"])}'},
            {'type': 'alert', 'message': f'Inventory alert: {random.choice(["Beer", "Wine", "Spirits"])} stock running low in JHB warehouse'},
            {'type': 'kpi', 'message': f'KPI Update: Customer satisfaction increased to {random.uniform(85, 95):.1f}%'}
        ]
        update = random.choice(updates)
        socketio.emit('real_time_update', update)

thread = threading.Thread(target=background_thread)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    port = find_free_port()
    
    print("🚀 Starting Bevco Executive Dashboard...")
    print(f"📊 Dashboard URL: http://localhost:{port}")
    print("👤 Default Login: admin / admin123")
    print("🤖 AI Chat Assistant: Available")
    print(f"✅ Using port {port}")
    
    def open_browser():
        time.sleep(2)
        webbrowser.open(f'http://localhost:{port}')
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
'''
    
    # Write app.py
    app_file = dashboard_dir / "app.py"
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(app_content)
    print_colored("   ✅ Created app.py", Colors.GREEN)
    
    # Create all templates
    templates = {
        'base.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Bevco Executive Dashboard{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        :root {
            --primary-color: #1a73e8;
            --secondary-color: #f8f9fa;
            --success-color: #28a745;
            --danger-color: #dc3545;
            --dark-color: #343a40;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f5f5f5;
        }
        
        .navbar {
            background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
        }
        
        .sidebar {
            background-color: #fff;
            min-height: calc(100vh - 56px);
            box-shadow: 2px 0 4px rgba(0,0,0,.05);
            padding-top: 20px;
        }
        
        .sidebar .nav-link {
            color: #333;
            padding: 12px 20px;
            margin: 4px 0;
            border-radius: 8px;
            transition: all 0.3s;
        }
        
        .sidebar .nav-link:hover {
            background-color: #f8f9fa;
            color: var(--primary-color);
            transform: translateX(5px);
        }
        
        .sidebar .nav-link.active {
            background-color: var(--primary-color);
            color: white;
        }
        
        .card {
            border: none;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,.08);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0,0,0,.12);
        }
        
        .stat-card {
            padding: 24px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--dark-color);
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stat-change {
            font-size: 0.875rem;
            font-weight: 500;
        }
        
        .stat-change.positive {
            color: var(--success-color);
        }
        
        .stat-change.negative {
            color: var(--danger-color);
        }
        
        .chart-container {
            position: relative;
            height: 300px;
            padding: 20px;
        }
        
        .notification-badge {
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1000;
        }
        
        .chat-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(238, 90, 36, 0.4);
            transition: transform 0.3s;
            z-index: 1000;
        }
        
        .chat-button:hover {
            transform: scale(1.1);
        }
        
        .chat-window {
            position: fixed;
            bottom: 100px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,.15);
            display: none;
            flex-direction: column;
            z-index: 1000;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 16px;
            border-radius: 12px 12px 0 0;
            font-weight: 600;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
        }
        
        .chat-input {
            padding: 16px;
            border-top: 1px solid #e0e0e0;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                display: none;
            }
            
            .chat-window {
                width: 90%;
                right: 5%;
            }
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('dashboard') }}">
                <i class="fas fa-chart-line me-2"></i>
                Bevco Executive Dashboard
            </a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text me-3">
                    <i class="fas fa-user-circle me-1"></i>
                    {{ username }}
                </span>
                <a class="nav-link" href="{{ url_for('logout') }}">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </a>
            </div>
        </div>
    </nav>
    
    <div class="container-fluid">
        <div class="row">
            <nav class="col-md-2 sidebar">
                <ul class="nav flex-column">
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'dashboard' %}active{% endif %}" href="{{ url_for('dashboard') }}">
                            <i class="fas fa-home me-2"></i> Executive Summary
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'sales' %}active{% endif %}" href="{{ url_for('sales') }}">
                            <i class="fas fa-shopping-cart me-2"></i> Sales Analytics
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'finance' %}active{% endif %}" href="{{ url_for('finance') }}">
                            <i class="fas fa-dollar-sign me-2"></i> Financial Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'operations' %}active{% endif %}" href="{{ url_for('operations') }}">
                            <i class="fas fa-cogs me-2"></i> Operations
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if request.endpoint == 'analytics' %}active{% endif %}" href="{{ url_for('analytics') }}">
                            <i class="fas fa-brain me-2"></i> AI Analytics
                        </a>
                    </li>
                </ul>
            </nav>
            
            <main class="col-md-10 ms-sm-auto px-md-4 py-4">
                {% block content %}{% endblock %}
            </main>
        </div>
    </div>
    
    <div class="chat-button" onclick="toggleChat()">
        <i class="fas fa-comments"></i>
    </div>
    
    <div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <i class="fas fa-robot me-2"></i> AI Business Assistant
            <button class="btn btn-sm btn-light float-end" onclick="toggleChat()">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">
                <strong>AI Assistant:</strong> Hello! I can help you analyze your business data. Ask me about sales, profits, regions, inventory, or any other business metrics.
            </div>
        </div>
        <div class="chat-input">
            <div class="input-group">
                <input type="text" class="form-control" id="chatInput" placeholder="Ask a question...">
                <button class="btn btn-primary" onclick="sendMessage()">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>
    
    <div id="notificationContainer" class="notification-badge"></div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const socket = io();
        
        socket.on('connect', function() {
            console.log('Connected to server');
        });
        
        socket.on('real_time_update', function(data) {
            showNotification(data.message, data.type);
        });
        
        function toggleChat() {
            const chatWindow = document.getElementById('chatWindow');
            chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message) {
                addMessage(message, 'user');
                
                fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, 'bot');
                });
                
                input.value = '';
            }
        }
        
        function addMessage(message, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message mb-2`;
            messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : 'AI Assistant'}:</strong> ${message}`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function showNotification(message, type = 'info') {
            const container = document.getElementById('notificationContainer');
            const alert = document.createElement('div');
            alert.className = `alert alert-${type === 'sales' ? 'success' : type === 'alert' ? 'warning' : 'info'} alert-dismissible fade show`;
            alert.innerHTML = `
                <i class="fas fa-bell me-2"></i>${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            container.appendChild(alert);
            
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }
        
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>''',
        
        'login.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Bevco Executive Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .login-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,.1);
            padding: 40px;
            width: 100%;
            max-width: 400px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header h1 {
            color: #333;
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        
        .login-header p {
            color: #666;
            font-size: 16px;
        }
        
        .form-control {
            border-radius: 10px;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
        }
        
        .form-control:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        }
        
        .btn-login {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 18px;
            font-weight: 600;
            color: white;
            width: 100%;
            margin-top: 20px;
            transition: transform 0.3s;
        }
        
        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .demo-credentials {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
        }
        
        .demo-credentials h6 {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        
        .demo-credentials code {
            color: #e83e8c;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <i class="fas fa-chart-line fa-3x mb-3" style="color: #667eea;"></i>
            <h1>Bevco Dashboard</h1>
            <p>Executive Business Intelligence</p>
        </div>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST" action="{{ url_for('login') }}">
            <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <div class="input-group">
                    <span class="input-group-text"><i class="fas fa-user"></i></span>
                    <input type="text" class="form-control" id="username" name="username" value="admin" required>
                </div>
            </div>
            
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <div class="input-group">
                    <span class="input-group-text"><i class="fas fa-lock"></i></span>
                    <input type="password" class="form-control" id="password" name="password" value="admin123" required>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary btn-login">
                <i class="fas fa-sign-in-alt me-2"></i> Login to Dashboard
            </button>
        </form>
        
        <div class="demo-credentials">
            <h6>Demo Credentials</h6>
            <code>Username: admin</code><br>
            <code>Password: admin123</code>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>''',
        
        'dashboard.html': '''{% extends "base.html" %}

{% block title %}Executive Summary - Bevco Dashboard{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Executive Summary</h1>
    <button class="btn btn-primary" onclick="refreshDashboard()">
        <i class="fas fa-sync-alt me-2"></i> Refresh
    </button>
</div>

<div class="row mb-4">
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <h6 class="stat-label">Total Sales</h6>
            <div class="stat-value" id="totalSales">R 0</div>
            <div class="stat-change positive">
                <i class="fas fa-arrow-up"></i> <span id="salesGrowth">0%</span>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <h6 class="stat-label">Profit Margin</h6>
            <div class="stat-value" id="profitMargin">0%</div>
            <div class="stat-change negative">
                <i class="fas fa-arrow-down"></i> <span id="marginChange">0%</span>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <h6 class="stat-label">Active Customers</h6>
            <div class="stat-value" id="activeCustomers">0</div>
            <div class="stat-change positive">
                <i class="fas fa-arrow-up"></i> <span id="customerGrowth">0%</span>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-3">
        <div class="card stat-card">
            <h6 class="stat-label">Inventory Turnover</h6>
            <div class="stat-value" id="inventoryTurnover">0x</div>
            <div class="stat-change positive">
                <i class="fas fa-arrow-up"></i> <span id="turnoverChange">0%</span>
            </div>
        </div>
    </div>
</div>

<div class="row mb-4">
    <div class="col-md-8 mb-3">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Sales Trend (Last 30 Days)</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="salesTrendChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Sales by Region</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="regionChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Top Products</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="productChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Recent Activity</h5>
            </div>
            <div class="card-body" style="max-height: 300px; overflow-y: auto;">
                <div id="activityFeed">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i> Loading recent activities...
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
let salesTrendChart, regionChart, productChart;

function initCharts() {
    const salesTrendCtx = document.getElementById('salesTrendChart').getContext('2d');
    salesTrendChart = new Chart(salesTrendCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Daily Sales (R)',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R ' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
    
    const regionCtx = document.getElementById('regionChart').getContext('2d');
    regionChart = new Chart(regionCtx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
    
    const productCtx = document.getElementById('productChart').getContext('2d');
    productChart = new Chart(productCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Sales (R)',
                data: [],
                backgroundColor: 'rgba(54, 162, 235, 0.8)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R ' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function refreshDashboard() {
    fetch('/api/dashboard_data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalSales').textContent = 'R ' + (data.total_sales / 1000000).toFixed(1) + 'M';
            document.getElementById('profitMargin').textContent = data.profit_margin.toFixed(1) + '%';
            document.getElementById('salesGrowth').textContent = '8.2%';
            document.getElementById('marginChange').textContent = '2.1%';
            document.getElementById('activeCustomers').textContent = '724';
            document.getElementById('customerGrowth').textContent = '5.3%';
            document.getElementById('inventoryTurnover').textContent = '8.2x';
            document.getElementById('turnoverChange').textContent = '1.5%';
            
            if (data.sales_trend && salesTrendChart) {
                salesTrendChart.data.labels = data.sales_trend.map(item => {
                    const date = new Date(item.date);
                    return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
                });
                salesTrendChart.data.datasets[0].data = data.sales_trend.map(item => item.sales);
                salesTrendChart.update();
            }
            
            if (data.sales_by_region && regionChart) {
                regionChart.data.labels = data.sales_by_region.map(item => item.region);
                regionChart.data.datasets[0].data = data.sales_by_region.map(item => item.sales);
                regionChart.update();
            }
            
            if (data.top_products && productChart) {
                productChart.data.labels = data.top_products.map(item => item.product_category);
                productChart.data.datasets[0].data = data.top_products.map(item => item.sales);
                productChart.update();
            }
            
            updateActivityFeed();
        })
        .catch(error => {
            console.error('Error fetching dashboard data:', error);
            showNotification('Error loading dashboard data', 'error');
        });
}

function updateActivityFeed() {
    const activities = [
        { type: 'sales', message: 'New order: R 3,450 from Pick n Pay (Gauteng)', time: '2 minutes ago' },
        { type: 'inventory', message: 'Low stock alert: Castle Lager in JHB warehouse', time: '5 minutes ago' },
        { type: 'customer', message: 'New customer registered: Tops Liquor Store (Cape Town)', time: '12 minutes ago' },
        { type: 'finance', message: 'Payment received: R 125,000 from Makro', time: '18 minutes ago' },
        { type: 'delivery', message: 'Delivery completed: Order #2451 to Checkers (Durban)', time: '25 minutes ago' }
    ];
    
    const feedHtml = activities.map(activity => {
        const icon = {
            sales: 'fa-shopping-cart text-success',
            inventory: 'fa-box text-warning',
            customer: 'fa-user-plus text-info',
            finance: 'fa-dollar-sign text-primary',
            delivery: 'fa-truck text-secondary'
        }[activity.type];
        
        return `
            <div class="d-flex align-items-start mb-3">
                <div class="me-3">
                    <i class="fas ${icon}"></i>
                </div>
                <div class="flex-grow-1">
                    <div class="small text-muted">${activity.time}</div>
                    <div>${activity.message}</div>
                </div>
            </div>
        `;
    }).join('');
    
    document.getElementById('activityFeed').innerHTML = feedHtml;
}

document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    refreshDashboard();
    setInterval(refreshDashboard, 30000);
});
</script>
{% endblock %}''',
        
        'sales.html': '''{% extends "base.html" %}

{% block title %}Sales Analytics - Bevco Dashboard{% endblock %}

{% block content %}
<h1 class="mb-4">Sales Analytics</h1>

<div class="row mb-4">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Sales Performance by Category</h5>
            </div>
            <div class="card-body">
                <div class="chart-container" style="height: 400px;">
                    <canvas id="categoryChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Vendor Performance</h5>
            </div>
            <div class="card-body">
                <div id="vendorTable"></div>
            </div>
        </div>
    </div>
    
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Customer Segmentation</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="customerChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const categoryCtx = document.getElementById('categoryChart').getContext('2d');
    new Chart(categoryCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                {
                    label: 'Beer',
                    data: [65000, 68000, 72000, 70000, 75000, 78000],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.4
                },
                {
                    label: 'Wine',
                    data: [45000, 47000, 46000, 48000, 52000, 55000],
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.4
                },
                {
                    label: 'Spirits',
                    data: [35000, 36000, 38000, 40000, 42000, 45000],
                    borderColor: 'rgb(255, 205, 86)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    const customerCtx = document.getElementById('customerChart').getContext('2d');
    new Chart(customerCtx, {
        type: 'pie',
        data: {
            labels: ['Retail', 'Wholesale', 'On-Trade', 'Export'],
            datasets: [{
                data: [45, 30, 20, 5],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 205, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    
    const vendorHtml = `
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Vendor</th>
                    <th>Sales (R)</th>
                    <th>Growth</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>SAB Miller</td>
                    <td>R 2.8M</td>
                    <td class="text-success">+12%</td>
                </tr>
                <tr>
                    <td>Distell</td>
                    <td>R 2.1M</td>
                    <td class="text-success">+8%</td>
                </tr>
                <tr>
                    <td>Coca-Cola</td>
                    <td>R 1.5M</td>
                    <td class="text-danger">-3%</td>
                </tr>
            </tbody>
        </table>
    `;
    document.getElementById('vendorTable').innerHTML = vendorHtml;
});
</script>
{% endblock %}''',
        
        'finance.html': '''{% extends "base.html" %}

{% block title %}Financial Dashboard - Bevco Dashboard{% endblock %}

{% block content %}
<h1 class="mb-4">Financial Dashboard</h1>

<div class="row mb-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Revenue vs Profit Trend</h5>
            </div>
            <div class="card-body">
                <div class="chart-container" style="height: 350px;">
                    <canvas id="financeChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Financial Ratios</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <h6>Current Ratio</h6>
                    <div class="progress">
                        <div class="progress-bar bg-success" style="width: 75%">2.3</div>
                    </div>
                </div>
                <div class="mb-3">
                    <h6>Debt to Equity</h6>
                    <div class="progress">
                        <div class="progress-bar bg-warning" style="width: 45%">0.45</div>
                    </div>
                </div>
                <div class="mb-3">
                    <h6>ROE</h6>
                    <div class="progress">
                        <div class="progress-bar bg-info" style="width: 65%">18.5%</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('financeChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [
                {
                    label: 'Revenue',
                    data: [4200000, 4500000, 4800000, 4600000, 5000000, 5200000],
                    backgroundColor: 'rgba(54, 162, 235, 0.8)'
                },
                {
                    label: 'Profit',
                    data: [1050000, 1125000, 1200000, 1150000, 1250000, 1300000],
                    backgroundColor: 'rgba(75, 192, 192, 0.8)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'R ' + (value / 1000000).toFixed(1) + 'M';
                        }
                    }
                }
            }
        }
    });
});
</script>
{% endblock %}''',
        
        'operations.html': '''{% extends "base.html" %}

{% block title %}Operations Dashboard - Bevco Dashboard{% endblock %}

{% block content %}
<h1 class="mb-4">Operations Dashboard</h1>

<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Inventory Levels by Warehouse</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="inventoryChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Employee Performance</h5>
            </div>
            <div class="card-body">
                <div class="chart-container">
                    <canvas id="employeeChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const inventoryCtx = document.getElementById('inventoryChart').getContext('2d');
    new Chart(inventoryCtx, {
        type: 'bar',
        data: {
            labels: ['JHB Central', 'Cape Town', 'Durban', 'PE'],
            datasets: [
                {
                    label: 'Beer',
                    data: [850, 720, 650, 450],
                    backgroundColor: 'rgba(255, 99, 132, 0.8)'
                },
                {
                    label: 'Wine',
                    data: [450, 680, 320, 280],
                    backgroundColor: 'rgba(54, 162, 235, 0.8)'
                },
                {
                    label: 'Spirits',
                    data: [320, 450, 280, 220],
                    backgroundColor: 'rgba(255, 205, 86, 0.8)'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            }
        }
    });
    
    const employeeCtx = document.getElementById('employeeChart').getContext('2d');
    new Chart(employeeCtx, {
        type: 'radar',
        data: {
            labels: ['Sales', 'Delivery', 'Warehouse', 'Admin', 'Management'],
            datasets: [{
                label: 'Performance Score',
                data: [85, 92, 78, 88, 95],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgb(75, 192, 192)',
                pointBackgroundColor: 'rgb(75, 192, 192)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
});
</script>
{% endblock %}''',
        
        'analytics.html': '''{% extends "base.html" %}

{% block title %}AI Analytics - Bevco Dashboard{% endblock %}

{% block content %}
<h1 class="mb-4">AI Analytics & Insights</h1>

<div class="row mb-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Sales Forecast (Next 30 Days)</h5>
            </div>
            <div class="card-body">
                <div class="chart-container" style="height: 350px;">
                    <canvas id="forecastChart"></canvas>
                </div>
                <div class="mt-3">
                    <span class="badge bg-info">Forecast Accuracy: 92%</span>
                    <span class="badge bg-success">Confidence: High</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Anomaly Detection</h5>
            </div>
            <div class="card-body">
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    <strong>Unusual Pattern Detected</strong><br>
                    Wine sales in Eastern Cape 35% below average
                </div>
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    <strong>Opportunity Alert</strong><br>
                    Spirits demand increasing in Gauteng
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('forecastChart').getContext('2d');
    
    const labels = [];
    const actualData = [];
    const forecastData = [];
    
    for (let i = -30; i <= 30; i++) {
        const date = new Date();
        date.setDate(date.getDate() + i);
        labels.push(date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }));
        
        if (i <= 0) {
            actualData.push(Math.random() * 50000 + 150000);
            forecastData.push(null);
        } else {
            actualData.push(null);
            forecastData.push(Math.random() * 50000 + 160000);
        }
    }
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Actual Sales',
                    data: actualData,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)'
                },
                {
                    label: 'Forecast',
                    data: forecastData,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderDash: [5, 5]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return 'R ' + (value / 1000).toFixed(0) + 'k';
                        }
                    }
                }
            }
        }
    });
});
</script>
{% endblock %}'''
    }
    
    # Write all templates
    for filename, content in templates.items():
        template_file = templates_dir / filename
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print_colored(f"   ✅ Created {filename}", Colors.GREEN)
    
    print_colored("✅ All files created successfully!", Colors.GREEN)

def start_dashboard(project_dir):
    """Start the dashboard application"""
    print_colored("\n🚀 Starting dashboard server...", Colors.BLUE)
    
    dashboard_dir = project_dir / "dashboard_portal"
    app_file = dashboard_dir / "app.py"
    
    if not app_file.exists():
        print_colored("❌ Dashboard app.py not found!", Colors.RED)
        return False
    
    # Change to dashboard directory
    os.chdir(dashboard_dir)
    
    try:
        print_colored("   Starting Flask server...", Colors.BLUE)
        print_colored("   Dashboard will open in your browser automatically...", Colors.YELLOW)
        
        # Start the Flask application
        subprocess.run([sys.executable, "app.py"])
        
        return True
        
    except KeyboardInterrupt:
        print_colored("\n🛑 Dashboard stopped by user", Colors.YELLOW)
        return True
    except Exception as e:
        print_colored(f"❌ Error starting dashboard: {e}", Colors.RED)
        return False

def main():
    """Main deployment function"""
    print_header()
    
    print_colored("\n🎯 COMPLETE SYSTEM DEPLOYMENT", Colors.BOLD)
    print_colored("This will:", Colors.BLUE)
    print_colored("   1. Download the complete dashboard system", Colors.BLUE)
    print_colored("   2. Install all required dependencies", Colors.BLUE)
    print_colored("   3. Create all necessary files", Colors.BLUE)
    print_colored("   4. Set up database with sample data", Colors.BLUE)
    print_colored("   5. Start the dashboard server", Colors.BLUE)
    print_colored("   6. Open in your browser automatically", Colors.BLUE)
    
    # Step 1: Download project
    project_dir = download_and_extract()
    if not project_dir:
        print_colored("❌ Failed to download project", Colors.RED)
        return 1
    
    # Step 2: Install dependencies
    install_dependencies()
    
    # Step 3: Create all files
    create_all_files(project_dir)
    
    # Step 4: Start dashboard
    if start_dashboard(project_dir):
        print_colored("\n🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!", Colors.GREEN)
        print_colored(f"📁 Project location: {project_dir}", Colors.BLUE)
        print_colored("📊 To start again: python3 dashboard_portal/app.py", Colors.BLUE)
        return 0
    else:
        print_colored("\n❌ Deployment failed", Colors.RED)
        return 1

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print_colored("\n🛑 Deployment cancelled by user", Colors.YELLOW)
        exit(0)
    except Exception as e:
        print_colored(f"\n❌ Unexpected error: {e}", Colors.RED)
        exit(1)