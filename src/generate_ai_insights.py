
import pandas as pd
import json
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

# Connect to Gemini
client = genai.Client()

# Load cleaned dataset
df = pd.read_csv("data/cleaned_superstore.csv")

# Load monthly KPI report
monthly = pd.read_csv("reports/monthly_kpi_report.csv")
monthly['Order Date'] = pd.to_datetime(monthly['Order Date'])

# Calculate overall KPIs
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_quantity = df['Quantity'].sum()
average_discount = df['Discount'].mean() * 100
profit_margin = (total_profit / total_sales) * 100

# Category performance
category_performance = df.groupby('Category').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Total_Quantity=('Quantity', 'sum')
).reset_index()

category_performance['Profit_Margin'] = (
    category_performance['Total_Profit']
    / category_performance['Total_Sales']
) * 100

# Subcategory performance
subcategory_performance = df.groupby('Sub-Category').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum')
).reset_index()

subcategory_performance['Profit_Margin'] = (
    subcategory_performance['Total_Profit']
    / subcategory_performance['Total_Sales']
) * 100

# Identify loss-making subcategories
loss_making = subcategory_performance[
    subcategory_performance['Total_Profit'] < 0
]

# Monthly trend analysis
highest_profit_month = monthly.loc[
    monthly['Monthly_Profit'].idxmax()
]

lowest_profit_month = monthly.loc[
    monthly['Monthly_Profit'].idxmin()
]

valid_growth = monthly.dropna(subset=['Sales_Growth_%'])

highest_growth = valid_growth.loc[
    valid_growth['Sales_Growth_%'].idxmax()
]

lowest_growth = valid_growth.loc[
    valid_growth['Sales_Growth_%'].idxmin()
]

# Prepare business analysis data
business_data = {
    "overall_kpis": {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": int(total_orders),
        "total_quantity": int(total_quantity),
        "average_discount_percent": round(average_discount, 2),
        "profit_margin_percent": round(profit_margin, 2)
    },

    "category_performance":
        category_performance.round(2).to_dict(orient="records"),

    "loss_making_subcategories":
        loss_making.round(2).to_dict(orient="records"),

    "monthly_insights": {
        "highest_profit_month":
            highest_profit_month['Order Date'].strftime('%Y-%m'),
        "highest_monthly_profit":
            round(highest_profit_month['Monthly_Profit'], 2),

        "lowest_profit_month":
            lowest_profit_month['Order Date'].strftime('%Y-%m'),
        "lowest_monthly_profit":
            round(lowest_profit_month['Monthly_Profit'], 2),

        "highest_sales_growth_month":
            highest_growth['Order Date'].strftime('%Y-%m'),
        "highest_sales_growth_percent":
            round(highest_growth['Sales_Growth_%'], 2),

        "lowest_sales_growth_month":
            lowest_growth['Order Date'].strftime('%Y-%m'),
        "lowest_sales_growth_percent":
            round(lowest_growth['Sales_Growth_%'], 2)
    }
}

# Create prompt for Gemini

prompt = f"""
You are an experienced business data analyst.

Analyze the following business KPI data:

{json.dumps(business_data, indent=2)}

Generate a professional business performance report with:

1. Overall Business Performance
2. Category-wise Performance
3. Loss-making Areas
4. Monthly Trend Analysis
5. Important Business Findings
6. Actionable Business Recommendations

Important rules:
- Use only the information provided in the dataset.
- Never invent facts, numbers, business causes or trends.
- Clearly distinguish observed facts from possible explanations.
- Do not recommend changes to cash reserves, marketing budgets,
  supplier costs or inventory unless the provided data supports them.
- When the cause of a problem is unknown, recommend further
  investigation instead of claiming a cause.
- Base every recommendation on a specific KPI or finding.
- Include relevant numbers and percentages.
- Use simple, professional business language.
- Avoid repeating the same finding in multiple sections.
- Do not claim seasonality from isolated monthly observations.
- Do not assume that discounts caused losses without supporting analysis.
- Do not recommend immediate business changes when further investigation is needed.
- Do not describe a negative monthly profit as an operating loss unless operating costs are available.
"""

print("\nGenerating AI Business Insights...\n")

response = client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt
)

print("=" * 60)
print("AI-POWERED BUSINESS PERFORMANCE REPORT")
print("=" * 60)

print(response.output_text)
# Save AI report
output_path = "reports/ai_business_performance_report.md"

with open(output_path, "w", encoding="utf-8") as file:
    file.write(response.output_text)

print("\nAI report saved successfully!")
print("File location:", output_path)

# python src/generate_ai_insights.py