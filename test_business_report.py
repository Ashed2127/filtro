#!/usr/bin/env python3
"""
Test script for the new business report generation functionality
"""

import pandas as pd
from src.processor import DataProcessor

def main():
    print("=" * 80)
    print("🚀 FILTRO - Testing Business Report Generation")
    print("=" * 80)
    print()
    
    processor = DataProcessor()
    
    # Create sample test data
    print("📂 STEP 1: Creating test data...")
    test_data = pd.DataFrame({
        'Date': ['01/01/2025', '01/01/2025', '01/01/2025', '01/01/2025', '01/01/2025'],
        'Ref No': ['INV001', 'INV002', 'INV003', 'INV004', 'INV005'],
        'Category': ['Rep', 'Rep', 'Bandi', 'Transfer', 'Bandi'],
        'Amount': [100, 200, 300, 85, 400],
        'Customer Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
        'Status': ['Completed', 'Completed', 'Completed', 'Completed', 'Completed']
    })
    
    processor.data = test_data
    processor.filtered_data = test_data
    processor._detect_business_columns()
    
    print("✅ Test data created")
    print(f"📊 Business columns detected: {processor.business_columns}")
    print()
    
    # Generate business report
    print("📋 STEP 2: Generating business report...")
    try:
        report = processor.generate_business_report()
        print("✅ Business report generated successfully")
        print()
        print("📄 GENERATED REPORT:")
        print("=" * 80)
        print(report)
        print("=" * 80)
        print()
        
        # Save report to file
        with open('test_business_report.txt', 'w') as f:
            f.write(report)
        print("💾 Report saved to: test_business_report.txt")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print()
    print("=" * 80)
    print("🎉 BUSINESS REPORT TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()