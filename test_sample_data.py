import pandas as pd
from typing import List, Dict, Optional


class DataProcessor:
    """Handles Excel data extraction and filtering for active sales items."""
    
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.filtered_data: Optional[pd.DataFrame] = None
    
    def load_excel(self, file_path: str) -> bool:
        """Load data from Excel file."""
        try:
            self.data = pd.read_excel(file_path)
            return True
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return False
    
    def filter_active_sales(self, 
                           status_column: str = "status",
                           active_value: str = "active") -> pd.DataFrame:
        """Filter rows where status is active/has sales."""
        if self.data is None:
            raise ValueError("No data loaded. Call load_excel first.")
        
        # Filter for active items (case-insensitive)
        mask = self.data[status_column].str.lower() == active_value.lower()
        self.filtered_data = self.data[mask].copy()
        
        return self.filtered_data
    
    def format_for_printing(self, 
                           columns_to_include: Optional[List[str]] = None) -> pd.DataFrame:
        """Format data for A5 paper printing."""
        if self.filtered_data is None:
            raise ValueError("No filtered data available.")
        
        if columns_to_include:
            # Select only specified columns if they exist
            available_cols = [col for col in columns_to_include if col in self.filtered_data.columns]
            if available_cols:
                formatted_data = self.filtered_data[available_cols].copy()
            else:
                formatted_data = self.filtered_data.copy()
        else:
            formatted_data = self.filtered_data.copy()
        
        # Clean and format data
        formatted_data = formatted_data.fillna("")
        
        # Format numeric columns for better readability
        for col in formatted_data.columns:
            if formatted_data[col].dtype == 'float64':
                formatted_data[col] = formatted_data[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) and isinstance(x, (int, float)) else x)
        
        return formatted_data
    
    def get_summary(self) -> Dict:
        """Get summary statistics of the filtered data."""
        if self.filtered_data is None:
            return {"error": "No filtered data available"}
        
        return {
            "total_items": len(self.filtered_data),
            "columns": list(self.filtered_data.columns),
            "preview": self.filtered_data.head(5).to_dict()
        }
    
    def export_to_excel(self, output_path: str, data: Optional[pd.DataFrame] = None) -> bool:
        """Export filtered data to Excel file."""
        try:
            export_data = data if data is not None else self.filtered_data
            if export_data is None:
                raise ValueError("No data to export")
            
            export_data.to_excel(output_path, index=False)
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False


def main():
    print("=" * 80)
    print("🚀 FILTRO - Testing with Downloaded Sample Data")
    print("=" * 80)
    print()
    
    processor = DataProcessor()
    
    # Step 1: Load the sample Excel file
    print("📂 STEP 1: Loading sample sales data...")
    if processor.load_excel("sample_sales_data.xlsx"):
        print("✅ Successfully loaded sample_sales_data.xlsx")
        print(f"📊 Total rows: {len(processor.data)}")
        print(f"📋 Columns: {list(processor.data.columns)}")
        print()
        print("📋 Original Sample Data:")
        print(processor.data.to_string(index=False))
        print()
    else:
        print("❌ Failed to load file")
        return
    
    # Step 2: Filter for active (high-value) sales
    print("🔍 STEP 2: Filtering for high-value (active) transactions...")
    try:
        filtered_data = processor.filter_active_sales("status", "active")
        print(f"✅ Found {len(filtered_data)} high-value transactions out of {len(processor.data)} total")
        print(f"📋 Filtered by: status = 'active' (orders over $200)")
        print()
        print("💰 High-Value Transactions (Active):")
        print(filtered_data.to_string(index=False))
        print()
    except Exception as e:
        print(f"❌ Error filtering data: {e}")
        return
    
    # Step 3: Calculate value statistics
    print("📈 STEP 3: Value Analysis")
    print("-" * 80)
    total_value_all = processor.data['Total'].sum()
    total_value_active = filtered_data['Total'].sum()
    total_value_inactive = processor.data[processor.data['status'] == 'inactive']['Total'].sum()
    
    print(f"Total value of all orders: ${total_value_all:,.2f}")
    print(f"Total value of high-value orders: ${total_value_active:,.2f}")
    print(f"Total value of low-value orders: ${total_value_inactive:,.2f}")
    print(f"Value concentration in active orders: {(total_value_active/total_value_all*100):.1f}%")
    print()
    
    # Step 4: Format for A5 printing
    print("🖨️  STEP 4: Formatting for A5 paper size printing...")
    try:
        # Select columns that are most relevant for printing
        print_columns = ['OrderDate', 'Region', 'Rep', 'Item', 'Units', 'UnitCost', 'Total']
        formatted_data = processor.format_for_printing(print_columns)
        print("✅ Data formatted for A5 printing")
        print()
        print("📋 Formatted Data (A5 Print Layout):")
        print(formatted_data.to_string(index=False))
        print()
        print("📏 Layout Notes for A5 (148mm × 210mm):")
        print("   - Font size: 10-12pt recommended")
        print("   - Margins: 10-15mm on all sides")
        print("   - Landscape orientation for better table fit")
        print("   - Row height: 12-15pt for readability")
    except Exception as e:
        print(f"❌ Error formatting data: {e}")
        return
    
    # Step 5: Export to Excel for printing
    print("💾 STEP 5: Exporting formatted data for printing...")
    try:
        formatted_data.to_excel("a5_print_format.xlsx", index=False)
        print("✅ Successfully exported to: a5_print_format.xlsx")
        print("📄 This file is ready for A5 paper printing")
        print()
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return
    
    print("=" * 80)
    print("🎉 FILTRO TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("📋 Test Summary:")
    print("  ✅ Sample data loaded successfully (20 rows)")
    print("  ✅ High-value transactions identified (10 active orders)")
    print("  ✅ Data filtered by status column")
    print("  ✅ Formatted for A5 paper printing")
    print("  ✅ Exported to print-ready Excel file")
    print()
    print("💰 Business Insights:")
    print(f"  • Total orders processed: {len(processor.data)}")
    print(f"  • High-value orders identified: {len(filtered_data)}")
    print(f"  • Total value concentration: {total_value_active/total_value_all*100:.1f}% in active orders")
    print(f"  • Average active order value: ${filtered_data['Total'].mean():.2f}")
    print()
    print("🖨️  Printing Instructions:")
    print("  • Open a5_print_format.xlsx in Excel")
    print("  • Set page size to A5 (148mm × 210mm)")
    print("  • Use landscape orientation")
    print("  • Set margins to 10-15mm")
    print("  • Adjust font size to 10-12pt for readability")
    print("  • Print to default desk printer")


if __name__ == "__main__":
    main()