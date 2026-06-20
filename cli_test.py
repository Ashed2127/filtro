#!/usr/bin/env python3
"""
Command-line interface for testing Filtro functionality
This allows testing the application without GUI requirements
"""

import pandas as pd
from typing import List, Dict, Optional
import sys
import os


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


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🔍 FILTRO - Excel Data Filter & Print Tool")
    print("📊 Command-Line Interface for Testing")
    print("=" * 60)
    print()


def display_menu():
    """Display main menu options"""
    print("Please select an option:")
    print("1. Load Excel file")
    print("2. Filter active sales")
    print("3. Show data summary")
    print("4. Display filtered data")
    print("5. Export to Excel")
    print("6. Exit")
    print()


def main():
    """Main CLI application loop"""
    print_banner()
    
    processor = DataProcessor()
    current_file = None
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                # Load Excel file
                file_path = input("Enter Excel file path (or press Enter for test_sales_data.xlsx): ").strip()
                if not file_path:
                    file_path = "test_sales_data.xlsx"
                
                if os.path.exists(file_path):
                    if processor.load_excel(file_path):
                        current_file = file_path
                        print(f"✅ Successfully loaded: {file_path}")
                        print(f"📊 Total rows: {len(processor.data)}")
                        print(f"📋 Columns: {list(processor.data.columns)}")
                    else:
                        print("❌ Failed to load file")
                else:
                    print(f"❌ File not found: {file_path}")
            
            elif choice == "2":
                # Filter active sales
                if processor.data is None:
                    print("❌ Please load an Excel file first (option 1)")
                    continue
                
                status_column = input("Enter status column name (default: status): ").strip()
                if not status_column:
                    status_column = "status"
                
                active_value = input("Enter active value (default: active): ").strip()
                if not active_value:
                    active_value = "active"
                
                try:
                    filtered_data = processor.filter_active_sales(status_column, active_value)
                    print(f"✅ Found {len(filtered_data)} active items")
                    print(f"📋 Filtered by: {status_column} = {active_value}")
                except Exception as e:
                    print(f"❌ Error filtering data: {e}")
            
            elif choice == "3":
                # Show summary
                if processor.filtered_data is None:
                    print("❌ No filtered data available. Please filter data first (option 2)")
                    continue
                
                summary = processor.get_summary()
                print("📈 DATA SUMMARY")
                print("-" * 40)
                print(f"Total active items: {summary['total_items']}")
                print(f"Columns: {', '.join(summary['columns'])}")
                print()
                print("Preview (first 5 rows):")
                print(pd.DataFrame(summary['preview']).to_string(index=False))
            
            elif choice == "4":
                # Display filtered data
                if processor.filtered_data is None:
                    print("❌ No filtered data available. Please filter data first (option 2)")
                    continue
                
                print("📋 FILTERED DATA")
                print("-" * 40)
                print(processor.filtered_data.to_string(index=False))
                print(f"\nTotal rows: {len(processor.filtered_data)}")
            
            elif choice == "5":
                # Export to Excel
                if processor.filtered_data is None:
                    print("❌ No filtered data available. Please filter data first (option 2)")
                    continue
                
                output_path = input("Enter output file name (default: filtered_output.xlsx): ").strip()
                if not output_path:
                    output_path = "filtered_output.xlsx"
                
                if processor.export_to_excel(output_path):
                    print(f"✅ Successfully exported to: {output_path}")
                else:
                    print("❌ Export failed")
            
            elif choice == "6":
                # Exit
                print("👋 Thank you for using Filtro CLI!")
                break
            
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 6.")
            
            print()  # Add blank line for readability
            
        except KeyboardInterrupt:
            print("\n👋 Program interrupted by user")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
        
        input("Press Enter to continue...")
        print()  # Add blank line after clearing screen


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)