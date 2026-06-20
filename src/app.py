import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))
from processor import DataProcessor


class FiltroApp(ctk.CTk):
    """Main GUI application for Filtro - Excel filtering and printing tool."""
    
    def __init__(self):
        super().__init__()
        
        self.processor = DataProcessor()
        self.current_file = None
        
        self.setup_window()
        self.setup_ui()
    
    def setup_window(self):
        """Configure main window properties."""
        self.title("Filtro - Excel Filter & Print Tool")
        self.geometry("800x600")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
    
    def setup_ui(self):
        """Build the user interface."""
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # File Selection Section
        self.file_frame = ctk.CTkFrame(self.main_frame)
        self.file_frame.pack(fill="x", pady=(0, 20))
        
        self.file_label = ctk.CTkLabel(
            self.file_frame, 
            text="Select Excel File:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.file_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.file_path_entry = ctk.CTkEntry(self.file_frame, placeholder_text="No file selected")
        self.file_path_entry.pack(fill="x", padx=10, pady=5)
        
        self.browse_button = ctk.CTkButton(
            self.file_frame,
            text="Browse",
            command=self.browse_file,
            width=100
        )
        self.browse_button.pack(anchor="e", padx=10, pady=(5, 10))
        
        # Filter Options Section
        self.filter_frame = ctk.CTkFrame(self.main_frame)
        self.filter_frame.pack(fill="x", pady=(0, 20))
        
        self.filter_label = ctk.CTkLabel(
            self.filter_frame,
            text="Filter Options:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.filter_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Status column input
        self.status_label = ctk.CTkLabel(self.filter_frame, text="Status Column Name:")
        self.status_label.pack(anchor="w", padx=10, pady=5)
        self.status_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="status")
        self.status_entry.pack(fill="x", padx=10, pady=5)
        self.status_entry.insert(0, "status")
        
        # Active value input
        self.active_label = ctk.CTkLabel(self.filter_frame, text="Active Value:")
        self.active_label.pack(anchor="w", padx=10, pady=5)
        self.active_entry = ctk.CTkEntry(self.filter_frame, placeholder_text="active")
        self.active_entry.pack(fill="x", padx=10, pady=(5, 10))
        self.active_entry.insert(0, "active")
        
        # Action Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", pady=(0, 20))
        
        self.process_button = ctk.CTkButton(
            self.button_frame,
            text="Process Data",
            command=self.process_data,
            height=40
        )
        self.process_button.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        self.print_button = ctk.CTkButton(
            self.button_frame,
            text="Print (A5)",
            command=self.print_data,
            height=40,
            fg_color="#2CC985",
            hover_color="#229E68"
        )
        self.print_button.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        # Results Section
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Results Preview:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.results_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.results_text = ctk.CTkTextbox(self.results_frame)
        self.results_text.pack(fill="both", expand=True, padx=10, pady=(5, 10))
    
    def browse_file(self):
        """Open file dialog to select Excel file."""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
    
    def process_data(self):
        """Process the Excel file and display results."""
        if not self.current_file:
            messagebox.showerror("Error", "Please select an Excel file first.")
            return
        
        status_column = self.status_entry.get() or "status"
        active_value = self.active_entry.get() or "active"
        
        try:
            # Load the Excel file
            if not self.processor.load_excel(self.current_file):
                messagebox.showerror("Error", "Failed to load Excel file.")
                return
            
            # Filter active sales
            self.processor.filter_active_sales(status_column, active_value)
            
            # Format for printing
            formatted_data = self.processor.format_for_printing()
            
            # Get summary
            summary = self.processor.get_summary()
            
            # Display results
            self.display_results(summary, formatted_data)
            
            messagebox.showinfo("Success", f"Processed {summary['total_items']} active items.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process data: {str(e)}")
    
    def display_results(self, summary: dict, data):
        """Display processed data in the results textbox."""
        self.results_text.delete("1.0", tk.END)
        
        result_text = f"Total Active Items: {summary['total_items']}\n"
        result_text += f"Columns: {', '.join(summary['columns'])}\n\n"
        result_text += "Preview:\n"
        result_text += data.to_string(max_rows=10)
        
        self.results_text.insert("1.0", result_text)
    
    def print_data(self):
        """Print the processed data to default printer (A5 format)."""
        if self.processor.filtered_data is None:
            messagebox.showerror("Error", "Please process data first.")
            return
        
        try:
            # Export to temporary Excel file for printing
            temp_file = "temp_filtered_output.xlsx"
            self.processor.export_to_excel(temp_file)
            
            # Open file with default application (user can print from there)
            os.startfile(temp_file)
            
            messagebox.showinfo("Print", f"Data exported to {temp_file}. Please print from Excel with A5 paper size settings.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare print data: {str(e)}")


def main():
    """Run the Filtro application."""
    app = FiltroApp()
    app.mainloop()


if __name__ == "__main__":
    main()