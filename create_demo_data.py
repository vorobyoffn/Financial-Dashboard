#!/usr/bin/env python3
"""
Demo Data Generator
Creates sample Excel files for testing the dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_demo_forecast():
    """Create a demo forecast Excel file"""
    
    # Create sample data
    assets = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'AMD', 'INTC']
    time_periods = ['3_days', '7_days', '14_days', '1_month', '3_months', '1_year']
    
    # Generate random forecast data
    np.random.seed(42)  # For reproducible results
    
    data = []
    for asset in assets:
        for period in time_periods:
            # Generate realistic-looking forecast data
            base_return = np.random.normal(0.02, 0.05)  # 2% mean, 5% std
            confidence = np.random.uniform(0.6, 0.95)
            volatility = np.random.uniform(0.01, 0.03)
            
            data.append({
                'Asset': asset,
                'Time_Period': period,
                'Forecast_Return': round(base_return * 100, 2),
                'Confidence': round(confidence * 100, 1),
                'Volatility': round(volatility * 100, 2),
                'Risk_Score': round(np.random.uniform(1, 10), 1),
                'Trend': np.random.choice(['Bullish', 'Bearish', 'Neutral']),
                'Last_Updated': datetime.now().strftime('%Y-%m-%d')
            })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create Excel file with multiple sheets
    output_file = 'Input/demo_forecast_2024.xlsx'
    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        # Main forecast sheet
        df.to_excel(writer, sheet_name='3-7-14days', index=False)
        
        # Summary sheet
        summary_data = df.groupby('Asset').agg({
            'Forecast_Return': 'mean',
            'Confidence': 'mean',
            'Risk_Score': 'mean'
        }).round(2)
        summary_data.to_excel(writer, sheet_name='Summary')
        
        # Risk analysis sheet
        risk_data = df[df['Risk_Score'] > 7].copy()
        risk_data.to_excel(writer, sheet_name='High_Risk', index=False)
    
    print(f"✅ Created demo forecast file: {output_file}")
    return output_file

def create_demo_macro():
    """Create a demo macro analysis file"""
    
    # Macro indicators
    indicators = ['GDP_Growth', 'Inflation_Rate', 'Interest_Rate', 'Unemployment', 'Consumer_Confidence']
    regions = ['US', 'EU', 'Asia', 'Global']
    
    data = []
    for indicator in indicators:
        for region in regions:
            # Generate realistic macro data
            if indicator == 'GDP_Growth':
                value = np.random.normal(2.5, 1.0)
            elif indicator == 'Inflation_Rate':
                value = np.random.normal(3.0, 0.5)
            elif indicator == 'Interest_Rate':
                value = np.random.normal(4.0, 1.5)
            elif indicator == 'Unemployment':
                value = np.random.normal(5.0, 1.0)
            else:  # Consumer_Confidence
                value = np.random.normal(70, 10)
            
            data.append({
                'Indicator': indicator,
                'Region': region,
                'Current_Value': round(value, 2),
                'Previous_Value': round(value + np.random.normal(0, 0.5), 2),
                'Change': round(np.random.normal(0, 0.3), 2),
                'Forecast': round(value + np.random.normal(0, 0.8), 2),
                'Date': datetime.now().strftime('%Y-%m-%d')
            })
    
    df = pd.DataFrame(data)
    output_file = 'Input/demo_macro_analysis_2024.xlsx'
    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Macro_Data', index=False)
        
        # Add summary sheet
        summary = df.groupby('Indicator').agg({
            'Current_Value': 'mean',
            'Change': 'mean'
        }).round(2)
        summary.to_excel(writer, sheet_name='Summary')
    
    print(f"✅ Created demo macro analysis file: {output_file}")
    return output_file

def create_demo_top30():
    """Create a demo top 30 performance file"""
    
    # Generate 30 assets with performance data
    assets = [f'STOCK_{i:03d}' for i in range(1, 31)]
    
    data = []
    for asset in assets:
        # Generate performance metrics
        return_1d = np.random.normal(0.5, 2.0)
        return_1w = np.random.normal(2.0, 5.0)
        return_1m = np.random.normal(8.0, 12.0)
        return_3m = np.random.normal(15.0, 20.0)
        return_1y = np.random.normal(25.0, 35.0)
        
        data.append({
            'Symbol': asset,
            'Company_Name': f'Company {asset.split("_")[1]}',
            'Sector': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer']),
            'Return_1D': round(return_1d, 2),
            'Return_1W': round(return_1w, 2),
            'Return_1M': round(return_1m, 2),
            'Return_3M': round(return_3m, 2),
            'Return_1Y': round(return_1y, 2),
            'Market_Cap': round(np.random.uniform(1, 100), 1),
            'Volume': round(np.random.uniform(1000000, 10000000), 0),
            'Rating': np.random.choice(['Buy', 'Hold', 'Sell']),
            'Last_Updated': datetime.now().strftime('%Y-%m-%d')
        })
    
    # Sort by 1-year return (top performers first)
    df = pd.DataFrame(data)
    df = df.sort_values('Return_1Y', ascending=False).reset_index(drop=True)
    
    output_file = 'Input/demo_top30_performance_2024.xlsx'
    
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Top30', index=False)
        
        # Add sector summary
        sector_summary = df.groupby('Sector').agg({
            'Return_1Y': 'mean',
            'Market_Cap': 'sum'
        }).round(2)
        sector_summary.to_excel(writer, sheet_name='Sector_Summary')
    
    print(f"✅ Created demo top 30 performance file: {output_file}")
    return output_file

def main():
    """Create all demo files"""
    print("🎯 Creating Demo Data for Dashboard Testing")
    print("=" * 50)
    
    # Ensure Input directory exists
    os.makedirs('Input', exist_ok=True)
    
    try:
        # Create demo files
        forecast_file = create_demo_forecast()
        macro_file = create_demo_macro()
        top30_file = create_demo_top30()
        
        print("\n🎉 Demo data creation completed!")
        print(f"📁 Files created in Input/ directory:")
        print(f"  📊 {forecast_file}")
        print(f"  🌍 {macro_file}")
        print(f"  🏆 {top30_file}")
        
        print("\n💡 You can now:")
        print("  1. Run the dashboard: python3 start_dashboard.py")
        print("  2. Test file processing: python3 main_processor.py --mode scan")
        print("  3. Launch web interface: python3 app.py")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {e}")

if __name__ == "__main__":
    main()
