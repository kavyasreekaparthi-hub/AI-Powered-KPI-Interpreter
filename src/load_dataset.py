import pandas as pd

file_path = "data/sample_-_superstore.xls"

df = pd.read_excel(file_path, engine="xlrd")

print("Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Rows:")
print(df.duplicated().sum())
print("\nNumerical Data Summary:")
print(df[['Sales', 'Profit', 'Discount', 'Quantity']].describe())
print("\nNegative Profit Records:")
print((df['Profit'] < 0).sum())

print("\nZero Profit Records:")
print((df['Profit'] == 0).sum())

print("\nDiscount Values:")
print(sorted(df['Discount'].unique()))