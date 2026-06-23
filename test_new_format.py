import pandas as pd
from src.processor import DataProcessor

# Create sample data that matches the Real Time format
sample_data = {
    'Service Number': ['80954413', '80954413', '80954413', '80954413'],
    'Order No': ['921283293', '88036970', '88036970', '88036970'],
    'Business Operation': ['Payment', 'Payment', 'Payment', 'Payment'],
    'Total Payment Amount': ['-5.00 Birr', '-55.00 Birr', '-25.00 Birr', '-5.00 Birr'],
    'Sales Date and Time': ['18-06-2024 10:30', '18-06-2024 11:45', '18-06-2024 12:00', '18-06-2024 13:15'],
    'Customer Name': ['Meskerem', 'Meskerem', 'Meskerem', 'Meskerem'],
    'Order Status': ['Completed', 'Completed', 'Completed', 'Completed'],
    'Category': ['rep', 'rep', 'bandl', 'rep']
}

# Create processor and load sample data
processor = DataProcessor()
processor.data = pd.DataFrame(sample_data)
processor.filtered_data = processor.data.copy()
processor.is_real_time_format = True

# Test the new format_for_report method
try:
    formatted_data = processor.format_for_report()
    print("Formatted Data:")
    print(formatted_data)
    print("\n" + "="*50 + "\n")
    
    # Test the new business report format
    report = processor.generate_business_report()
    print("Business Report:")
    print(report)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
