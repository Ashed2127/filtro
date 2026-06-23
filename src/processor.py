import pandas as pd
from typing import List, Dict, Optional
import os


class DataProcessor:
    """Handles Excel data extraction and filtering for active sales items."""
    
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.filtered_data: Optional[pd.DataFrame] = None
        self.is_real_time_format = False
    
    def _is_real_time_file(self, file_path: str) -> bool:
        """Check if the file is a Real Time Customer Order Payment List Report."""
        filename = os.path.basename(file_path)
        return filename.startswith("Real Time")
    
    def load_excel(self, file_path: str) -> bool:
        """Load data from Excel file."""
        try:
            self.is_real_time_format = self._is_real_time_file(file_path)
            
            if self.is_real_time_format:
                # Real Time format has header at row 10 (0-indexed)
                self.data = pd.read_excel(file_path, header=10)
            else:
                # Standard format
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
        
        # Use appropriate column name based on file format
        if self.is_real_time_format:
            status_column = "Order Status"
            active_value = "Completed"  # Default for Real Time files
        
        # Filter for active items (case-insensitive)
        if status_column in self.data.columns:
            mask = self.data[status_column].str.lower() == active_value.lower()
            self.filtered_data = self.data[mask].copy()
        else:
            # If column doesn't exist, return all data
            print(f"Warning: Column '{status_column}' not found. Returning all data.")
            self.filtered_data = self.data.copy()
        
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