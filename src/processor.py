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
    
    def filter_specific_transactions(self) -> pd.DataFrame:
        """Filter for specific transaction types: 85.00Birr, 100.00Birr, and zero price operations."""
        if self.data is None:
            raise ValueError("No data loaded. Call load_excel first.")
        
        if not self.is_real_time_format:
            print("Warning: Specific transaction filtering is only available for Real Time format.")
            return self.data.copy()
        
        # First filter by Order Status = Completed
        if "Order Status" in self.data.columns:
            status_mask = self.data["Order Status"].str.lower() == "completed"
            filtered_by_status = self.data[status_mask].copy()
        else:
            filtered_by_status = self.data.copy()
        
        # Clean payment amounts for filtering
        filtered_by_status["CleanAmount"] = filtered_by_status["Total Payment Amount"].apply(
            lambda x: self._extract_numeric_amount(x)
        )
        
        # Filter for specific amounts: 85.00, 100.00, and 0.00
        amount_mask = (
            (filtered_by_status["CleanAmount"] == 85.00) |
            (filtered_by_status["CleanAmount"] == 100.00) |
            (filtered_by_status["CleanAmount"] == 0.00)
        )
        
        # For zero price transactions, also check Business Operation column
        zero_price_mask = filtered_by_status["CleanAmount"] == 0.00
        if "Business Operation" in filtered_by_status.columns:
            # Include zero price transactions with specific business operations
            business_operations_to_include = [
                "Change Subscriber SIM Card",
                "Create Customer", 
                "Change Supplementary Offering"
            ]
            business_op_mask = filtered_by_status["Business Operation"].isin(business_operations_to_include)
            # Combine: either (zero price AND valid business op) OR (85/100 birr)
            final_mask = (
                (zero_price_mask & business_op_mask) |
                (filtered_by_status["CleanAmount"] == 85.00) |
                (filtered_by_status["CleanAmount"] == 100.00)
            )
        else:
            # If no Business Operation column, just use amount filter
            final_mask = amount_mask
        
        self.filtered_data = filtered_by_status[final_mask].copy()
        
        # Add categorization
        self.filtered_data["Category"] = self.filtered_data.apply(self._categorize_transaction, axis=1)
        
        # Remove the temporary CleanAmount column
        if "CleanAmount" in self.filtered_data.columns:
            del self.filtered_data["CleanAmount"]
        
        return self.filtered_data
    
    def _categorize_transaction(self, row) -> str:
        """Categorize transaction based on business operation and amount."""
        # Get clean amount
        amount_str = str(row.get('Total Payment Amount', ''))
        amount = self._extract_numeric_amount(amount_str)
        
        business_op = str(row.get('Business Operation', '')).lower()
        
        # Categorization logic
        if amount == 85.0:
            return 'Offer'  # 85 birr transactions
        elif amount == 100.0 and 'change subscriber sim card' in business_op:
            return 'Replacement'  # 100 birr SIM card changes
        elif amount == 0.0:
            return 'Transfer'  # Zero price transactions
        elif amount == 100.0:
            return 'Bundle'  # Other 100 birr transactions (potential bundles)
        
        return 'Other'
    
    def _extract_numeric_amount(self, amount):
        """Extract numeric value from payment amount string."""
        if pd.isna(amount) or amount == "":
            return 0.0
        
        amount_str = str(amount)
        # Remove 'Birr' suffix, commas, and whitespace
        amount_str = amount_str.replace("Birr", "").replace(",", "").strip()
        
        try:
            return float(amount_str)
        except (ValueError, TypeError):
            return 0.0
    
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
        
        # Clean payment amounts if in Real Time format
        if self.is_real_time_format and "Total Payment Amount" in formatted_data.columns:
            formatted_data["Total Payment Amount"] = formatted_data["Total Payment Amount"].apply(
                lambda x: self._clean_payment_amount(x)
            )
        
        return formatted_data
    
    def _clean_payment_amount(self, amount):
        """Clean payment amount by removing 'Birr' suffix and converting to proper format."""
        if pd.isna(amount) or amount == "":
            return ""
        
        amount_str = str(amount)
        # Remove 'Birr' suffix, commas, and any whitespace
        amount_str = amount_str.replace("Birr", "").replace(",", "").strip()
        
        return amount_str
    
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