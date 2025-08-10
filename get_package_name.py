#!/usr/bin/env python3
"""
Package Name Module
Handles package naming and identification for financial data
"""

import re
from typing import Optional, Dict, List

def get_package_name(filename: str) -> str:
    """
    Extract package name from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        Extracted package name
    """
    # Remove file extension
    name = filename.rsplit('.', 1)[0] if '.' in filename else filename
    
    # Try to extract meaningful package name
    # Look for patterns like "Package_2024_01_15" or "Package_Jan15"
    patterns = [
        r'Package_(\w+)_(\d{4})_(\d{2})_(\d{2})',
        r'Package_(\w+)_(\w{3})(\d{2})',
        r'Package_(\w+)',
        r'(\w+)_(\d{4})_(\d{2})_(\d{2})',
        r'(\w+)_(\w{3})(\d{2})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, name, re.IGNORECASE)
        if match:
            if len(match.groups()) >= 2:
                return f"Package_{match.group(1)}_{match.group(2)}"
            else:
                return f"Package_{match.group(1)}"
    
    # Fallback: use filename as package name
    return name

def get_package_info(filename: str) -> Dict[str, str]:
    """
    Get detailed package information from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        Dictionary with package information
    """
    package_name = get_package_name(filename)
    
    # Try to extract date information
    date_match = re.search(r'(\d{4})_(\d{2})_(\d{2})', filename)
    date_info = {}
    
    if date_match:
        date_info = {
            'year': date_match.group(1),
            'month': date_match.group(2),
            'day': date_match.group(3),
            'date': f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
        }
    
    return {
        'filename': filename,
        'package_name': package_name,
        'date_info': date_info
    }

def get_package_list(filenames: List[str]) -> List[Dict[str, str]]:
    """
    Get list of all packages from filenames
    
    Args:
        filenames: List of filenames
        
    Returns:
        List of package information dictionaries
    """
    packages = []
    
    for filename in filenames:
        if filename.strip():
            packages.append(get_package_info(filename))
    
    return packages
