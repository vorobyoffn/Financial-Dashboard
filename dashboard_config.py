#!/usr/bin/env python3
"""
Dashboard Configuration
Simple settings for the Financial Forecast Dashboard
"""

# Dashboard Settings
DASHBOARD_TITLE = "Financial Forecast Dashboard"
DASHBOARD_VERSION = "1.0.0"
DASHBOARD_DESCRIPTION = "Complete financial data analysis and visualization system"

# Web Interface Settings
WEB_HOST = "localhost"
WEB_PORT = 5000
WEB_DEBUG = True
WEB_THREADED = True

# File Upload Settings
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
UPLOAD_FOLDER = "uploads"

# Processing Settings
DEFAULT_INPUT_DIR = "Input"
DEFAULT_OUTPUT_DIR = "Output"
BATCH_SIZE = 10  # Number of files to process at once

# Display Settings
HEATMAP_COLORMAP = "RdYlGn"  # Red-Yellow-Green
CHART_STYLE = "seaborn-v0_8"
FIGURE_SIZE = (12, 8)
DPI = 100

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "dashboard.log"

# Performance Settings
CACHE_TIMEOUT = 300  # 5 minutes
MAX_WORKERS = 4
TIMEOUT = 30  # seconds

# Security Settings
SECRET_KEY = "your-secret-key-change-this-in-production"
SESSION_TIMEOUT = 3600  # 1 hour

# Output Formats
SUPPORTED_OUTPUT_FORMATS = ['xlsx', 'png', 'jpg', 'pdf', 'csv']
DEFAULT_OUTPUT_FORMAT = 'xlsx'

# Chart Settings
CHART_TYPES = ['line', 'bar', 'heatmap', 'scatter', 'pie']
DEFAULT_CHART_TYPE = 'line'

# Data Processing
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_TIMEZONE = "UTC"
ROUND_DECIMALS = 4

# Notification Settings
ENABLE_NOTIFICATIONS = True
NOTIFICATION_EMAIL = ""
NOTIFICATION_WEBHOOK = ""

def get_config():
    """Get all configuration as a dictionary"""
    return {key: value for key, value in globals().items() 
            if not key.startswith('_') and key.isupper()}

def update_config(key, value):
    """Update a configuration value"""
    if key in globals() and key.isupper():
        globals()[key] = value
        return True
    return False
