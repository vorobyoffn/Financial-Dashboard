#!/usr/bin/env python3
"""
Financial Forecast Dashboard - Main Web Application
Flask-based web interface for financial data analysis
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
import json
import traceback
from datetime import datetime
import logging

# Import local modules
try:
    from dashboard_config import *
    from get_company_info import get_company_info
    from get_index import get_index_info
    from get_package_name import get_package_name
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'csv'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_input_files():
    """Get list of input files"""
    input_dir = Path("Input")
    if not input_dir.exists():
        return []
    
    files = []
    for file_path in input_dir.glob("*.xls*"):
        try:
            stat = file_path.stat()
            files.append({
                'name': file_path.name,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'path': str(file_path)
            })
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
    
    return sorted(files, key=lambda x: x['modified'], reverse=True)

def get_output_files():
    """Get list of output files"""
    output_dir = Path("Output")
    if not output_dir.exists():
        return {}
    
    output_files = {}
    for subdir in ['spreadsheets', 'heatmaps', 'charts', 'summaries']:
        subdir_path = output_dir / subdir
        if subdir_path.exists():
            files = list(subdir_path.glob("*"))
            output_files[subdir] = [
                {
                    'name': f.name,
                    'size': f.stat().st_size if f.is_file() else 0,
                    'modified': datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S') if f.is_file() else ''
                }
                for f in files
            ]
    
    return output_files

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        input_files = get_input_files()
        output_files = get_output_files()
        
        # Get system stats
        total_input_files = len(input_files)
        total_output_files = sum(len(files) for files in output_files.values())
        
        return render_template('dashboard.html',
                             input_files=input_files,
                             output_files=output_files,
                             total_input_files=total_input_files,
                             total_output_files=total_output_files)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        flash(f"Error loading dashboard: {str(e)}", 'error')
        return render_template('error.html', error=str(e))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads"""
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Save to Input directory
            input_dir = Path("Input")
            input_dir.mkdir(exist_ok=True)
            
            file_path = input_dir / filename
            file.save(file_path)
            
            flash(f'File {filename} uploaded successfully!', 'success')
            logger.info(f"File uploaded: {filename}")
        else:
            flash('Invalid file type. Please upload .xls, .xlsx, or .csv files.', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/process', methods=['POST'])
def process_files():
    """Process uploaded files"""
    try:
        # Get list of files to process
        input_files = get_input_files()
        if not input_files:
            flash('No files to process', 'error')
            return redirect(url_for('index'))
        
        # For now, just show success message
        # In a real implementation, you would call your processing functions here
        flash(f'Processing {len(input_files)} files...', 'info')
        
        # TODO: Implement actual file processing
        # This would call your existing processing functions
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Processing error: {e}")
        flash(f'Processing failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/files')
def api_files():
    """API endpoint to get file information"""
    try:
        input_files = get_input_files()
        output_files = get_output_files()
        
        return jsonify({
            'input_files': input_files,
            'output_files': output_files,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/process', methods=['POST'])
def api_process():
    """API endpoint to process files"""
    try:
        data = request.get_json()
        file_list = data.get('files', [])
        
        if not file_list:
            return jsonify({'status': 'error', 'message': 'No files specified'}), 400
        
        # TODO: Implement actual processing
        # For now, return success
        return jsonify({
            'status': 'success',
            'message': f'Processing {len(file_list)} files',
            'files_processed': file_list
        })
        
    except Exception as e:
        logger.error(f"API processing error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a file"""
    try:
        # Look in Output directory first
        output_path = Path("Output") / filename
        if output_path.exists():
            return send_file(output_path, as_attachment=True)
        
        # Look in Input directory
        input_path = Path("Input") / filename
        if input_path.exists():
            return send_file(input_path, as_attachment=True)
        
        flash('File not found', 'error')
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        flash(f'Download failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting Financial Forecast Dashboard...")
    print("📊 Web interface will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        logger.error(f"Failed to start dashboard: {e}")
