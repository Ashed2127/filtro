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


# Test the DataProcessor
if __name__ == "__main__":
    print("🧪 Testing Filtro DataProcessor")
    print("=" * 50)
    
    # Create processor instance
    processor = DataProcessor()
    
    # Load the test Excel file
    print("📂 Loading test_sales_data.xlsx...")
    if processor.load_excel("test_sales_data.xlsx"):
        print("✅ File loaded successfully!")
        print(f"📊 Total rows in file: {len(processor.data)}")
        print(f"📋 Columns: {list(processor.data.columns)}")
        print()
        
        # Display first few rows
        print("🔍 First few rows of data:")
        print(processor.data.head())
        print()
        
        # Filter active sales
        print("🔎 Filtering for active sales...")
        filtered_data = processor.filter_active_sales("status", "active")
        print(f"✅ Found {len(filtered_data)} active items!")
        print()
        
        # Display filtered data
        print("📋 Filtered data:")
        print(filtered_data)
        print()
        
        # Get summary
        print("📈 Summary:")
        summary = processor.get_summary()
        print(f"Total active items: {summary['total_items']}")
        print(f"Columns: {summary['columns']}")
        print()
        
        # Format for printing
        print("🖨️  Formatting for printing...")
        formatted_data = processor.format_for_printing()
        print("✅ Data formatted successfully!")
        print()
        
        # Export to Excel
        print("💾 Exporting filtered data to Excel...")
        if processor.export_to_excel("filtered_output.xlsx"):
            print("✅ Export successful! Created: filtered_output.xlsx")
        else:
            print("❌ Export failed!")
        
        print()
        print("=" * 50)
        print("🎉 Test completed successfully!")
        print("🚀 The Filtro executable is ready to use!")
        print("📁 You can run it with: ./dist/Filtro")
        
    else:
        print("❌ Failed to load Excel file!")
        print("Make sure test_sales_data.xlsx exists in the current directory.")