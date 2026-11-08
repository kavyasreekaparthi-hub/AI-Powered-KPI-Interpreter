import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data/cleaned_superstore.csv")

# Convert Order Date into datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Calculate monthly sales and profit
monthly_performance = df.groupby(
    df['Order Date'].dt.to_period('M')
).agg(
    Monthly_Sales=('Sales', 'sum'),
    Monthly_Profit=('Profit', 'sum')
).reset_index()

# Convert monthly period into datetime
monthly_performance['Order Date'] = (
    monthly_performance['Order Date'].dt.to_timestamp()
)

# Monthly Sales Trend
plt.figure(figsize=(12, 5))

plt.plot(
    monthly_performance['Order Date'],
    monthly_performance['Monthly_Sales'],
    marker='o'
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig("reports/monthly_sales_trend.png")
plt.show()
# Monthly Profit Trend

plt.figure(figsize=(12, 5))

plt.plot(
    monthly_performance['Order Date'],
    monthly_performance['Monthly_Profit'],
    marker='o'
)

plt.title("Monthly Profit Trend")
plt.xlabel("Month")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig("reports/monthly_profit_trend.png")
plt.show()
# Automated Monthly Trend Insights

highest_profit_month = monthly_performance.loc[
    monthly_performance['Monthly_Profit'].idxmax()
]

lowest_profit_month = monthly_performance.loc[
    monthly_performance['Monthly_Profit'].idxmin()
]

print("\nAUTOMATED MONTHLY TREND INSIGHTS")

print(
    f"Highest profit month: "
    f"{highest_profit_month['Order Date'].strftime('%Y-%m')} "
    f"with profit of "
    f"${highest_profit_month['Monthly_Profit']:.2f}."
)

print(
    f"Lowest profit month: "
    f"{lowest_profit_month['Order Date'].strftime('%Y-%m')} "
    f"with profit of "
    f"${lowest_profit_month['Monthly_Profit']:.2f}."
)
# Export Monthly KPI Analysis

output_path = "reports/monthly_kpi_report.csv"

monthly_performance.to_csv(output_path, index=False)

print("\nMonthly KPI report saved successfully!")
print("File location:", output_path)
# Automated Monthly Business Recommendations

print("\nMONTHLY BUSINESS RECOMMENDATIONS")

loss_months = monthly_performance[
    monthly_performance['Monthly_Profit'] < 0
]

if not loss_months.empty:

    for _, row in loss_months.iterrows():

        print(
            f"{row['Order Date'].strftime('%Y-%m')} "
            f"recorded a loss of "
            f"${abs(row['Monthly_Profit']):.2f}."
        )

        print(
            "Recommendation: Investigate product costs, "
            "discounts and sales performance for this month."
        )

else:
    print("No loss-making months were identified.")
    # Calculate Month-over-Month Sales Growth

monthly_performance['Sales_Growth_%'] = (
    monthly_performance['Monthly_Sales'].pct_change() * 100
)

print("\nMONTH-OVER-MONTH SALES GROWTH")
print(
    monthly_performance[
        ['Order Date', 'Monthly_Sales', 'Sales_Growth_%']
    ].assign(
        Monthly_Sales=lambda x: x['Monthly_Sales'].round(2),
        Sales_Growth=lambda x: x['Sales_Growth_%'].round(2)
    )
)
# Save updated monthly KPI report

monthly_performance.to_csv(
    "reports/monthly_kpi_report.csv",
    index=False
)

print("\nUpdated monthly KPI report saved successfully!")
# Automated Sales Growth Insights

valid_growth = monthly_performance.dropna(
    subset=['Sales_Growth_%']
)

highest_growth = valid_growth.loc[
    valid_growth['Sales_Growth_%'].idxmax()
]

lowest_growth = valid_growth.loc[
    valid_growth['Sales_Growth_%'].idxmin()
]

increasing_months = (
    valid_growth['Sales_Growth_%'] > 0
).sum()

decreasing_months = (
    valid_growth['Sales_Growth_%'] < 0
).sum()

print("\nAUTOMATED SALES GROWTH INSIGHTS")

print(
    f"Highest sales growth: "
    f"{highest_growth['Order Date'].strftime('%Y-%m')} "
    f"({highest_growth['Sales_Growth_%']:.2f}%)."
)

print(
    f"Lowest sales growth: "
    f"{lowest_growth['Order Date'].strftime('%Y-%m')} "
    f"({lowest_growth['Sales_Growth_%']:.2f}%)."
)

print(f"Months with increasing sales: {increasing_months}")

print(f"Months with decreasing sales: {decreasing_months}")

# python src/visualize_kpis.py