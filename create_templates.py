#!/usr/bin/env python3
"""
Create missing template files for the dashboard
"""

import os

def create_templates():
    """Create all necessary template files"""
    
    # Create templates directory
    os.makedirs('dashboard_portal/templates', exist_ok=True)
    
    # Base template
    base_html = '''<!DOCTYPE html>
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
    
    <!-- Chat Button -->
    <div class="chat-button" onclick="toggleChat()">
        <i class="fas fa-comments"></i>
    </div>
    
    <!-- Chat Window -->
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
    
    <!-- Notification Container -->
    <div id="notificationContainer" class="notification-badge"></div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Socket.IO connection
        const socket = io();
        
        socket.on('connect', function() {
            console.log('Connected to server');
        });
        
        socket.on('real_time_update', function(data) {
            showNotification(data.message, data.type);
        });
        
        // Chat functionality
        function toggleChat() {
            const chatWindow = document.getElementById('chatWindow');
            chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message) {
                // Add user message
                addMessage(message, 'user');
                
                // Send to server
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
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                alert.remove();
            }, 5000);
        }
        
        // Enter key to send message
        document.getElementById('chatInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
    {% block extra_js %}{% endblock %}
</body>
</html>'''
    
    # Login template
    login_html = '''<!DOCTYPE html>
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
</html>'''
    
    # Dashboard template
    dashboard_html = '''{% extends "base.html" %}

{% block title %}Executive Summary - Bevco Dashboard{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Executive Summary</h1>
    <button class="btn btn-primary" onclick="refreshDashboard()">
        <i class="fas fa-sync-alt me-2"></i> Refresh
    </button>
</div>

<!-- KPI Cards -->
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

<!-- Charts Row -->
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

<!-- Product Performance -->
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
    // Sales Trend Chart
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
    
    // Region Chart
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
    
    // Product Chart
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
            // Update KPIs
            document.getElementById('totalSales').textContent = 'R ' + (data.total_sales / 1000000).toFixed(1) + 'M';
            document.getElementById('profitMargin').textContent = data.profit_margin.toFixed(1) + '%';
            document.getElementById('salesGrowth').textContent = '8.2%';
            document.getElementById('marginChange').textContent = '2.1%';
            document.getElementById('activeCustomers').textContent = '724';
            document.getElementById('customerGrowth').textContent = '5.3%';
            document.getElementById('inventoryTurnover').textContent = '8.2x';
            document.getElementById('turnoverChange').textContent = '1.5%';
            
            // Update Sales Trend Chart
            if (data.sales_trend && salesTrendChart) {
                salesTrendChart.data.labels = data.sales_trend.map(item => {
                    const date = new Date(item.date);
                    return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
                });
                salesTrendChart.data.datasets[0].data = data.sales_trend.map(item => item.sales);
                salesTrendChart.update();
            }
            
            // Update Region Chart
            if (data.sales_by_region && regionChart) {
                regionChart.data.labels = data.sales_by_region.map(item => item.region);
                regionChart.data.datasets[0].data = data.sales_by_region.map(item => item.sales);
                regionChart.update();
            }
            
            // Update Product Chart
            if (data.top_products && productChart) {
                productChart.data.labels = data.top_products.map(item => item.product_category);
                productChart.data.datasets[0].data = data.top_products.map(item => item.sales);
                productChart.update();
            }
            
            // Update activity feed
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

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    refreshDashboard();
    
    // Refresh every 30 seconds
    setInterval(refreshDashboard, 30000);
});
</script>
{% endblock %}'''
    
    # Sales template
    sales_html = '''{% extends "base.html" %}

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
// Initialize sales analytics
document.addEventListener('DOMContentLoaded', function() {
    loadSalesData();
});

function loadSalesData() {
    fetch('/api/sales_data')
        .then(response => response.json())
        .then(data => {
            // Category chart
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
            
            // Customer chart
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
            
            // Vendor table
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
}
</script>
{% endblock %}'''
    
    # Finance template
    finance_html = '''{% extends "base.html" %}

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

<div class="row">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Budget vs Actual</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Department</th>
                                <th>Budget (R)</th>
                                <th>Actual (R)</th>
                                <th>Variance</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Sales</td>
                                <td>R 5,000,000</td>
                                <td>R 5,234,000</td>
                                <td class="text-success">+4.7%</td>
                                <td><span class="badge bg-success">On Track</span></td>
                            </tr>
                            <tr>
                                <td>Marketing</td>
                                <td>R 800,000</td>
                                <td>R 825,000</td>
                                <td class="text-danger">-3.1%</td>
                                <td><span class="badge bg-warning">Over Budget</span></td>
                            </tr>
                            <tr>
                                <td>Operations</td>
                                <td>R 2,500,000</td>
                                <td>R 2,450,000</td>
                                <td class="text-success">+2.0%</td>
                                <td><span class="badge bg-success">Under Budget</span></td>
                            </tr>
                        </tbody>
                    </table>
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
{% endblock %}'''
    
    # Operations template
    operations_html = '''{% extends "base.html" %}

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

<div class="row">
    <div class="col-md-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Supply Chain Metrics</h5>
            </div>
            <div class="card-body">
                <div class="row text-center">
                    <div class="col-md-3">
                        <h3 class="text-primary">3.2 days</h3>
                        <p>Avg Lead Time</p>
                    </div>
                    <div class="col-md-3">
                        <h3 class="text-success">98.5%</h3>
                        <p>On-Time Delivery</p>
                    </div>
                    <div class="col-md-3">
                        <h3 class="text-warning">12</h3>
                        <p>Active Suppliers</p>
                    </div>
                    <div class="col-md-3">
                        <h3 class="text-info">R 2.8M</h3>
                        <p>Inventory Value</p>
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
    // Inventory Chart
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
    
    // Employee Chart
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
{% endblock %}'''
    
    # Analytics template
    analytics_html = '''{% extends "base.html" %}

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

<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">AI Recommendations</h5>
            </div>
            <div class="card-body">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">
                        <i class="fas fa-lightbulb text-warning me-2"></i>
                        Increase beer inventory in JHB by 15% for upcoming holiday
                    </li>
                    <li class="list-group-item">
                        <i class="fas fa-chart-line text-success me-2"></i>
                        Focus marketing on wine products in Western Cape
                    </li>
                    <li class="list-group-item">
                        <i class="fas fa-users text-info me-2"></i>
                        Target wholesale customers with bulk discount offers
                    </li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Customer Churn Risk</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Customer</th>
                                <th>Risk Level</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Tops Liquor (Durban)</td>
                                <td><span class="badge bg-danger">High</span></td>
                                <td><button class="btn btn-sm btn-primary">Contact</button></td>
                            </tr>
                            <tr>
                                <td>Pick n Pay (Cape Town)</td>
                                <td><span class="badge bg-warning">Medium</span></td>
                                <td><button class="btn btn-sm btn-primary">Review</button></td>
                            </tr>
                        </tbody>
                    </table>
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
    
    // Generate forecast data
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
    
    # Write all templates
    templates = {
        'base.html': base_html,
        'login.html': login_html,
        'dashboard.html': dashboard_html,
        'sales.html': sales_html,
        'finance.html': finance_html,
        'operations.html': operations_html,
        'analytics.html': analytics_html
    }
    
    for filename, content in templates.items():
        filepath = os.path.join('dashboard_portal/templates', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {filename}")
    
    print("\n✅ All templates created successfully!")

if __name__ == "__main__":
    create_templates()