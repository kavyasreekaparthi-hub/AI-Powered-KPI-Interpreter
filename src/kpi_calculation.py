import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/cleaned_superstore.csv")

# Calculate KPIs
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_quantity = df['Quantity'].sum()
average_discount = df['Discount'].mean()

# Calculate profit margin
profit_margin = (total_profit / total_sales) * 100

# Display KPIs
print("BUSINESS KPI SUMMARY")

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Quantity Sold:", total_quantity)
print("Average Discount:", round(average_discount * 100, 2), "%")
print("Profit Margin:", round(profit_margin, 2), "%")
# Category-wise performance
category_performance = df.groupby('Category').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).reset_index()

print("\nCATEGORY-WISE PERFORMANCE")
print(category_performance.round(2))
# Calculate category-wise profit margin
category_performance['Profit_Margin'] = (
    category_performance['Total_Profit']
    / category_performance['Total_Sales']
) * 100

print("\nCATEGORY-WISE PROFIT MARGIN")
print(category_performance[
    ['Category', 'Profit_Margin']
].round(2))
# Sub-category-wise performance
subcategory_performance = df.groupby('Sub-Category').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum')
).reset_index()

subcategory_performance['Profit_Margin'] = (
    subcategory_performance['Total_Profit']
    / subcategory_performance['Total_Sales']
) * 100

print("\nSUB-CATEGORY PERFORMANCE")
print(subcategory_performance.round(2))
# Analyse discounts for loss-making sub-categories

loss_subcategories = ['Tables', 'Bookcases', 'Supplies']

loss_analysis = df[
    df['Sub-Category'].isin(loss_subcategories)
].groupby('Sub-Category').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Average_Discount=('Discount', 'mean'),
    Records=('Row ID', 'count')
).reset_index()

loss_analysis['Average_Discount'] = (
    loss_analysis['Average_Discount'] * 100
)

print("\nDISCOUNT ANALYSIS OF LOSS-MAKING SUB-CATEGORIES")
print(loss_analysis.round(2))
# Automated Business Insight Generation

print("\nAUTOMATED BUSINESS INSIGHTS")

# 1. Identify the biggest loss-making sub-category
worst_loss = loss_analysis.loc[
    loss_analysis['Total_Profit'].idxmin()
]

print(
    f"\n1. {worst_loss['Sub-Category']} is the biggest "
    f"loss-making sub-category, with a loss of "
    f"${abs(worst_loss['Total_Profit']):.2f}."
)

# 2. Identify all loss-making sub-categories
loss_making = subcategory_performance[
    subcategory_performance['Total_Profit'] < 0
]

print("\n2. LOSS-MAKING SUB-CATEGORIES")

for _, row in loss_making.iterrows():
    print(
        f"{row['Sub-Category']} has a loss of "
        f"${abs(row['Total_Profit']):.2f}."
    )

# 3. Identify the category with the highest profit
highest_profit_category = category_performance.loc[
    category_performance['Total_Profit'].idxmax()
]

print(
    f"\n3. {highest_profit_category['Category']} "
    f"generates the highest category profit of "
    f"${highest_profit_category['Total_Profit']:.2f}."
)

# 4. Identify the category with the lowest profit margin
lowest_margin_category = category_performance.loc[
    category_performance['Profit_Margin'].idxmin()
]

print(
    f"\n4. {lowest_margin_category['Category']} "
    f"has the lowest category profit margin of "
    f"{lowest_margin_category['Profit_Margin']:.2f}%."
)

# 5. Identify the sub-category with the highest profit margin
highest_margin_subcategory = subcategory_performance.loc[
    subcategory_performance['Profit_Margin'].idxmax()
]

print(
    f"\n5. {highest_margin_subcategory['Sub-Category']} "
    f"has the highest sub-category profit margin of "
    f"{highest_margin_subcategory['Profit_Margin']:.2f}%."
)
# Monthly Sales and Profit Trend Analysis

# Convert Order Date into datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Calculate monthly sales and profit
monthly_performance = df.groupby(
    df['Order Date'].dt.to_period('M')
).agg(
    Monthly_Sales=('Sales', 'sum'),
    Monthly_Profit=('Profit', 'sum')
).reset_index()

# Convert month period into string
monthly_performance['Order Date'] = (
    monthly_performance['Order Date'].astype(str)
)

print("\nMONTHLY SALES AND PROFIT ANALYSIS")
print(monthly_performance.round(2))

# Identify the highest sales month
highest_sales_month = monthly_performance.loc[
    monthly_performance['Monthly_Sales'].idxmax()
]

print(
    f"\nHighest sales month: {highest_sales_month['Order Date']}"
    f" with sales of ${highest_sales_month['Monthly_Sales']:.2f}."
)

# Identify the lowest sales month
lowest_sales_month = monthly_performance.loc[
    monthly_performance['Monthly_Sales'].idxmin()
]

print(
    f"Lowest sales month: {lowest_sales_month['Order Date']}"
    f" with sales of ${lowest_sales_month['Monthly_Sales']:.2f}."
)



# python src/kpi_calculation.py