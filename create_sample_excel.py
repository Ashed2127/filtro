import pandas as pd

# Sample data from Contextures - office supply sales
data = {
    'OrderDate': ['1/6/2026', '1/23/2026', '2/9/2026', '2/26/2026', '3/15/2026', 
                  '4/1/2026', '4/18/2026', '5/5/2026', '5/22/2026', '6/8/2026',
                  '6/25/2026', '7/12/2026', '7/29/2026', '8/15/2026', '9/1/2026'],
    'Region': ['East', 'Central', 'Central', 'Central', 'West', 'East', 'Central', 
               'Central', 'West', 'East', 'Central', 'East', 'East', 'East', 'Central'],
    'Rep': ['Jones', 'Kivell', 'Jardine', 'Gill', 'Sorvino', 'Jones', 'Andrews',
            'Jardine', 'Thompson', 'Jones', 'Morgan', 'Howard', 'Parent', 'Jones', 'Smith'],
    'Item': ['Pencil', 'Binder', 'Pencil', 'Pen', 'Pencil', 'Binder', 'Pencil',
             'Pencil', 'Pencil', 'Binder', 'Pencil', 'Binder', 'Binder', 'Pencil', 'Desk'],
    'Units': [95, 50, 36, 27, 56, 60, 75, 90, 32, 60, 90, 29, 81, 35, 2],
    'UnitCost': [1.99, 19.99, 4.99, 19.99, 2.99, 4.99, 1.99, 4.99, 1.99, 8.99, 4.99, 1.99, 19.99, 4.99, 125.00],
    'Total': [189.05, 999.50, 179.64, 539.73, 167.44, 299.40, 149.25, 449.10, 63.68, 539.40, 449.10, 57.71, 1619.19, 174.65, 250.00]
}

df = pd.DataFrame(data)

# Add a status column based on total value (for testing filtering)
# Mark high-value orders as "active", low-value as "inactive"
df['status'] = df['Total'].apply(lambda x: 'active' if x > 200 else 'inactive')

# Add some more sample rows to have better testing data
additional_data = {
    'OrderDate': ['9/18/2026', '10/5/2026', '10/22/2026', '11/8/2026', '11/25/2026'],
    'Region': ['West', 'East', 'Central', 'West', 'East'],
    'Rep': ['Thompson', 'Howard', 'Smith', 'Sorvino', 'Jones'],
    'Item': ['Binder', 'Pen', 'Pencil', 'Desk', 'Binder'],
    'Units': [40, 55, 25, 3, 70],
    'UnitCost': [4.99, 2.99, 1.99, 125.00, 8.99],
    'Total': [199.60, 164.45, 49.75, 375.00, 629.30]
}

additional_df = pd.DataFrame(additional_data)
additional_df['status'] = additional_df['Total'].apply(lambda x: 'active' if x > 200 else 'inactive')

# Combine the data
df = pd.concat([df, additional_df], ignore_index=True)

# Save to Excel file
df.to_excel('sample_sales_data.xlsx', index=False)
print("✅ Sample Excel file created: sample_sales_data.xlsx")
print(f"📊 Total rows: {len(df)}")
print(f"📋 Columns: {list(df.columns)}")
print(f"🔍 Active (high-value) orders: {len(df[df['status'] == 'active'])}")
print(f"🔍 Inactive (low-value) orders: {len(df[df['status'] == 'inactive'])}")
print()
print("📋 Sample data preview:")
print(df.head(10))