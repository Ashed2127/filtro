import pandas as pd

# Create sample test data
data = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'product_name': ['Widget A', 'Widget B', 'Gadget X', 'Gadget Y', 'Tool Z', 
                     'Widget C', 'Gadget W', 'Tool V', 'Widget D', 'Gadget U'],
    'quantity': [100, 50, 75, 25, 150, 80, 60, 40, 120, 90],
    'price': [10.99, 15.50, 8.75, 12.25, 20.00, 11.25, 9.50, 14.75, 13.00, 7.99],
    'status': ['active', 'inactive', 'active', 'active', 'inactive', 
               'active', 'inactive', 'active', 'active', 'inactive'],
    'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19',
             '2024-01-20', '2024-01-21', '2024-01-22', '2024-01-23', '2024-01-24']
}

df = pd.DataFrame(data)

# Save to Excel file
df.to_excel('test_sales_data.xlsx', index=False)
print("Test Excel file created: test_sales_data.xlsx")
print(f"Total rows: {len(df)}")
print(f"Active items: {len(df[df['status'] == 'active'])}")