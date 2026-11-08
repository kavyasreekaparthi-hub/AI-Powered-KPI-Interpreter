import pandas as pd

# Load dataset
file_path = "data/sample_-_superstore.xls"
df = pd.read_excel(file_path, engine="xlrd")

# Remove exact duplicate rows
df = df.drop_duplicates()

# Convert date columns to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Display cleaned dataset information
print("Data Cleaning Completed!")
print("Dataset Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())
# Save cleaned dataset
output_path = "data/cleaned_superstore.csv"

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("File location:", output_path)