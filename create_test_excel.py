from openpyxl import Workbook

# Create a new workbook
wb = Workbook()
ws = wb.active

# Add headers
headers = ['id', 'product_name', 'quantity', 'price', 'status', 'date']
ws.append(headers)

# Add sample data
data = [
    [1, 'Widget A', 100, 10.99, 'active', '2024-01-15'],
    [2, 'Widget B', 50, 15.50, 'inactive', '2024-01-16'],
    [3, 'Gadget X', 75, 8.75, 'active', '2024-01-17'],
    [4, 'Gadget Y', 25, 12.25, 'active', '2024-01-18'],
    [5, 'Tool Z', 150, 20.00, 'inactive', '2024-01-19'],
    [6, 'Widget C', 80, 11.25, 'active', '2024-01-20'],
    [7, 'Gadget W', 60, 9.50, 'inactive', '2024-01-21'],
    [8, 'Tool V', 40, 14.75, 'active', '2024-01-22'],
    [9, 'Widget D', 120, 13.00, 'active', '2024-01-23'],
    [10, 'Gadget U', 90, 7.99, 'inactive', '2024-01-24']
]

for row in data:
    ws.append(row)

# Save the workbook
wb.save('test_sales_data.xlsx')
print("Test Excel file created: test_sales_data.xlsx")