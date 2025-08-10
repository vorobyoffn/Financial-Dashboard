#!/usr/bin/env python3
"""
Index Module
Handles index-related operations and data extraction
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import re

def get_index(symbol: str, data: pd.DataFrame = None) -> Dict[str, any]:
    """
    Get index information for a given symbol
    
    Args:
        symbol: Index symbol
        data: Optional DataFrame containing index data
        
    Returns:
        Dictionary with index information
    """
    index_info = {
        'symbol': symbol,
        'name': symbol,
        'type': 'Unknown',
        'components': [],
        'weighting': 'Unknown'
    }
    
    if data is not None and not data.empty:
        # Try to extract additional info from data
        if 'index_name' in data.columns:
            index_info['name'] = str(data['index_name'].iloc[0])
        if 'index_type' in data.columns:
            index_info['type'] = str(data['index_type'].iloc[0])
        if 'weighting_method' in data.columns:
            index_info['weighting'] = str(data['weighting_method'].iloc[0])
    
    return index_info

def get_index_components(symbol: str, data: pd.DataFrame = None) -> List[str]:
    """
    Get list of components for a given index
    
    Args:
        symbol: Index symbol
        data: Optional DataFrame containing index data
        
    Returns:
        List of component symbols
    """
    components = []
    
    if data is not None and not data.empty:
        # Look for columns that might contain component information
        component_columns = ['component', 'components', 'symbol', 'ticker']
        
        for col in component_columns:
            if col in data.columns:
                components = [str(x) for x in data[col].dropna().unique() if str(x).strip()]
                if components:
                    break
    
    return components

def get_index_performance(symbol: str, data: pd.DataFrame = None) -> Dict[str, float]:
    """
    Get performance metrics for a given index
    
    Args:
        symbol: Index symbol
        data: Optional DataFrame containing index data
        
    Returns:
        Dictionary with performance metrics
    """
    performance = {
        'return_1d': 0.0,
        'return_1w': 0.0,
        'return_1m': 0.0,
        'return_3m': 0.0,
        'return_1y': 0.0,
        'volatility': 0.0
    }
    
    if data is not None and not data.empty:
        # Try to extract performance data
        for metric in performance.keys():
            if metric in data.columns:
                try:
                    performance[metric] = float(data[metric].iloc[0])
                except (ValueError, TypeError):
                    pass
    
    return performance

def get_index_list(data: pd.DataFrame) -> List[Dict[str, any]]:
    """
    Get list of all indices from data
    
    Args:
        data: DataFrame containing index data
        
    Returns:
        List of index information dictionaries
    """
    indices = []
    
    if data is not None and not data.empty:
        if 'index_symbol' in data.columns:
            symbols = data['index_symbol'].unique()
        elif 'symbol' in data.columns:
            symbols = data['symbol'].unique()
        else:
            return indices
        
        for symbol in symbols:
            if pd.notna(symbol) and str(symbol).strip():
                index_data = data[data['symbol'] == symbol] if 'symbol' in data.columns else data
                indices.append(get_index(symbol, index_data))
    
    return indices
