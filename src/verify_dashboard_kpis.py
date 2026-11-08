import pandas as pd

# 1. Load cleaned dataset
df = pd.read_csv("data/cleaned_superstore.csv")

# 2. Convert Order Date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# 3. Apply the same filters as the Technology AI report
filtered_df = df[
    (df["Category"] == "Office Supplies")
    & (df["Order Date"].dt.date >= pd.to_datetime("2023-01-03").date())
    & (df["Order Date"].dt.date <= pd.to_datetime("2026-12-30").date())
].copy()

# 4. Calculate KPIs independently
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
average_discount = filtered_df["Discount"].mean() * 100

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0 else 0
)

# 5. Display verification results
print("\nOFFICE SUPPLIES CATEGORY KPI VERIFICATION")
print("--------------------------------------")

print("Total Records:", len(filtered_df))
print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Orders:", total_orders)
print("Total Quantity Sold:", total_quantity)
print("Average Discount:", round(average_discount, 2), "%")
print("Profit Margin:", round(profit_margin, 2), "%")

print("--------------------------------------")


#python src/verify_dashboard_kpis.py