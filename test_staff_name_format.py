import pandas as pd
from src.processor import DataProcessor

# Create sample data that matches the user's example with Staff Name
sample_data = {
    'Service Number': ['992193461', '992207146', '', '992108743', '', '992193849', '', '957564258', '992158395', ''],
    'Order No': ['30156421421', '30156421421', '30156421276', '30156421214', '30156421095', '30156420994', '30156420870', '30156420663', '30156420561', '30156420240'],
    'Business Operation': ['Create Subscriber', 'Create Subscriber', 'Create Customer', 'Create Subscriber', 'Create Customer', 'Create Subscriber', 'Create Customer', 'Change Subscriber SIM Card', 'Create Subscriber', 'Create Customer'],
    'Total Payment Amount': ['85.00 Birr', '85.00 Birr', '0.00 Birr', '85.00 Birr', '0.00 Birr', '85.00 Birr', '0.00 Birr', '100.00 Birr', '85.00 Birr', '0.00 Birr'],
    'Sales Date and Time': ['16-06-2026 10:30', '16-06-2026 11:45', '16-06-2026 12:00', '16-06-2026 13:15', '16-06-2026 14:00', '16-06-2026 15:30', '16-06-2026 16:00', '16-06-2026 17:00', '16-06-2026 18:00', '16-06-2026 19:00'],
    'Customer Name': ['IFTU NEGES', 'IFTU NEGES', 'IFTU NEGES', 'REBUMA MUL', 'REBUMA MUL', 'LELISA SHE', 'LELISA SHE', 'ABDII WALD', 'TILHUN MUL', 'TILHUN MUL'],
    'Staff Name': ['John Doe', 'John Doe', 'John Doe', 'Jane Smith', 'Jane Smith', 'Bob Johnson', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson', 'Charlie Wilson'],
    'Order Status': ['Completed', 'Completed', 'Completed', 'Completed', 'Completed', 'Completed', 'Completed', 'Completed', 'Completed', 'Completed'],
    'Category': ['Offer', 'Offer', 'Transfer', 'Offer', 'Transfer', 'Offer', 'Transfer', 'Replacement', 'Offer', 'Transfer']
}

# Create processor and load sample data
processor = DataProcessor()
processor.data = pd.DataFrame(sample_data)
processor.filtered_data = processor.data.copy()
processor.is_real_time_format = True

# Test the new business report format
try:
    report = processor.generate_business_report()
    print("Business Report:")
    print(report)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
