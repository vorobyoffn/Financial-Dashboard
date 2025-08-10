#!/usr/bin/env python3
"""
Company Information Module
Extracts and processes company information from financial data
"""

import pandas as pd
from typing import Dict, Optional, List
import re

def get_company_info(symbol: str, data: pd.DataFrame = None) -> Dict[str, str]:
    """
    Get company information for a given symbol
    
    Args:
        symbol: Stock symbol/ticker
        data: Optional DataFrame containing company data
        
    Returns:
        Dictionary with company information
    """
    # Default company info structure
    company_info = {
        'symbol': symbol,
        'name': symbol,
        'sector': 'Unknown',
        'industry': 'Unknown',
        'description': f'Company information for {symbol}'
    }
    
    if data is not None and not data.empty:
        # Try to extract additional info from data
        if 'company_name' in data.columns:
            company_info['name'] = str(data['company_name'].iloc[0])
        if 'sector' in data.columns:
            company_info['sector'] = str(data['sector'].iloc[0])
        if 'industry' in data.columns:
            company_info['industry'] = str(data['industry'].iloc[0])
    
    return company_info

def get_company_list(data: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Get list of all companies from data
    
    Args:
        data: DataFrame containing company data
        
    Returns:
        List of company information dictionaries
    """
    companies = []
    
    if data is not None and not data.empty:
        if 'symbol' in data.columns:
            symbols = data['symbol'].unique()
            for symbol in symbols:
                if pd.notna(symbol) and str(symbol).strip():
                    company_data = data[data['symbol'] == symbol]
                    companies.append(get_company_info(symbol, company_data))
    
    return companies
