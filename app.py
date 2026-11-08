import json
import os
from io import BytesIO
from xml.sax.saxutils import escape

import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from google import genai

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)


# ==================================================
# 1. CONFIGURATION
# ==================================================

load_dotenv()

st.set_page_config(
    page_title="AI-Powered KPI Interpreter",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered KPI Interpreter")

st.write(
    "Automated Business Performance Analysis "
    "and AI-Generated Business Insights"
)

st.divider()

st.subheader("Business Performance Dashboard")

st.info(
    "This dashboard analyzes business KPIs and uses "
    "Google Gemini to generate business insights "
    "and recommendations."
)


# ==================================================
# 2. PDF GENERATION FUNCTION
# ==================================================

def create_pdf_report(report_text):

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7
    )

    story = []

    story.append(
        Paragraph(
            "AI-Powered KPI Interpreter",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Business Performance Analysis Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#4472C4")
        )
    )

    story.append(Spacer(1, 15))

    for line in report_text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        if line.startswith("---"):

            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=colors.grey
                )
            )

            continue

        if line.startswith("### "):

            story.append(
                Paragraph(
                    escape(line[4:]),
                    heading_style
                )
            )

        elif line.startswith("## "):

            story.append(
                Paragraph(
                    escape(line[3:]),
                    heading_style
                )
            )

        elif line.startswith("# "):

            story.append(
                Paragraph(
                    escape(line[2:]),
                    title_style
                )
            )

        elif line.startswith("- ") or line.startswith("* "):

            bullet_text = escape(line[2:])
            bullet_text = bullet_text.replace("**", "")

            story.append(
                Paragraph(
                    "&#8226; " + bullet_text,
                    body_style
                )
            )

        else:

            paragraph_text = escape(line)
            paragraph_text = paragraph_text.replace("**", "")

            story.append(
                Paragraph(
                    paragraph_text,
                    body_style
                )
            )

    document.build(story)

    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()


# ==================================================
# 3. DATASET UPLOAD
# ==================================================

st.divider()

st.subheader("📁 Upload Your Business Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    try:

        if uploaded_file.name.lower().endswith(".csv"):
            original_df = pd.read_csv(uploaded_file)

        else:
            original_df = pd.read_excel(uploaded_file)

        st.success("Dataset uploaded successfully!")

    except Exception as e:

        st.error(f"Unable to read the uploaded file: {e}")
        st.stop()

else:

    try:

        original_df = pd.read_csv(
            "data/cleaned_superstore.csv"
        )

        st.info("Using the default Superstore dataset.")

    except FileNotFoundError:

        st.error(
            "Default dataset not found. "
            "Please upload a CSV or Excel file."
        )

        st.stop()


# ==================================================
# 4. DATASET VALIDATION AND CLEANING
# ==================================================

required_columns = [
    "Sales",
    "Profit",
    "Order ID",
    "Category",
    "Sub-Category",
    "Order Date"
]

missing_columns = [
    column for column in required_columns
    if column not in original_df.columns
]

if missing_columns:

    st.error(
        f"Your dataset is missing these required columns: "
        f"{missing_columns}"
    )

    st.stop()


if "Postal Code" in original_df.columns:

    original_df["Postal Code"] = (
        original_df["Postal Code"].astype("string")
    )


for column in ["Sales", "Profit"]:

    original_df[column] = pd.to_numeric(
        original_df[column],
        errors="coerce"
    )


original_df["Order Date"] = pd.to_datetime(
    original_df["Order Date"],
    errors="coerce"
)


original_df = original_df.dropna(
    subset=[
        "Sales",
        "Profit",
        "Order Date",
        "Order ID",
        "Category",
        "Sub-Category"
    ]
).copy()


if original_df.empty:

    st.error("No valid business records found in the dataset.")
    st.stop()


st.success("Dataset structure validated successfully!")


# ==================================================
# 5. CATEGORY FILTER
# ==================================================

st.divider()

st.subheader("🔎 Filter Business Data")

categories = (
    ["All Categories"]
    + sorted(
        original_df["Category"].dropna().unique().tolist()
    )
)

selected_category = st.selectbox(
    "Select Product Category",
    categories
)


# ==================================================
# 6. REGION FILTER
# ==================================================

if "Region" in original_df.columns:

    regions = (
        ["All Regions"]
        + sorted(
            original_df["Region"].dropna().unique().tolist()
        )
    )

    selected_region = st.selectbox(
        "Select Business Region",
        regions
    )

else:

    selected_region = "Region column not available"


# ==================================================
# 7. DATE FILTER
# ==================================================

st.subheader("📅 Filter by Order Date")

min_date = original_df["Order Date"].min().date()
max_date = original_df["Order Date"].max().date()

selected_dates = st.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="order_date_filter"
)


if isinstance(selected_dates, (tuple, list)):

    if len(selected_dates) == 2:

        start_date, end_date = selected_dates

    elif len(selected_dates) == 1:

        start_date = selected_dates[0]
        end_date = selected_dates[0]

    else:

        start_date = min_date
        end_date = max_date

else:

    start_date = selected_dates
    end_date = selected_dates


if start_date > end_date:

    st.error("Start date cannot be after end date.")
    st.stop()


# ==================================================
# 8. APPLY ALL FILTERS AND TRACK RECORD COUNTS
# ==================================================

df = original_df.copy()

original_record_count = len(df)

# Apply Category filter

if selected_category != "All Categories":

    df = df[
        df["Category"] == selected_category
    ].copy()


category_record_count = len(df)


# Apply Region filter

if (
    selected_region != "All Regions"
    and "Region" in df.columns
):

    df = df[
        df["Region"] == selected_region
    ].copy()


region_record_count = len(df)


# Apply Date filter

df = df[
    df["Order Date"].dt.date.between(
        start_date,
        end_date
    )
].copy()


date_record_count = len(df)


# Display applied filters

st.caption(
    f"Applied filters: Category: {selected_category} | "
    f"Region: {selected_region} | "
    f"Dates: {start_date} to {end_date}"
)


if df.empty:

    st.warning("No records found for the selected filters.")
    st.stop()


# ==================================================
# 9. FILTER DIAGNOSTICS
# ==================================================

st.divider()

st.subheader("🔍 Filter Diagnostics")

st.write("Original dataset records:", original_record_count)

st.write("Records after Category filter:", category_record_count)

st.write("Records after Region filter:", region_record_count)

st.write("Records after Date filter:", date_record_count)

st.write("Original dataset minimum date:", min_date)

st.write("Original dataset maximum date:", max_date)

st.write("Selected start date:", start_date)

st.write("Selected end date:", end_date)

st.write(
    "Actual minimum date in filtered data:",
    df["Order Date"].min().date()
)

st.write(
    "Actual maximum date in filtered data:",
    df["Order Date"].max().date()
)


# ==================================================
# 10. DATASET OVERVIEW
# ==================================================

st.divider()

st.subheader("📋 Dataset Overview")

st.write("Total Records:", df.shape[0])

st.write("Total Columns:", df.shape[1])

st.write("Sample Business Data")

st.dataframe(
    df.head(10),
    width="stretch"
)


# ==================================================
# 11. KPI CALCULATIONS
# ==================================================

total_sales = df["Sales"].sum()

total_profit = df["Profit"].sum()

total_orders = df["Order ID"].nunique()

total_quantity = (
    int(df["Quantity"].sum())
    if "Quantity" in df.columns else None
)

average_discount = (
    round(float(df["Discount"].mean() * 100), 2)
    if "Discount" in df.columns else None
)

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0 else 0
)


st.divider()

st.subheader("📊 Key Performance Indicators (KPIs)")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

with col2:

    st.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

with col3:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col4:

    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )


# ==================================================
# 12. CATEGORY-WISE SALES ANALYSIS
# ==================================================

st.divider()

st.subheader("Category-wise Sales Performance")

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

st.bar_chart(
    category_sales,
    x="Category",
    y="Sales",
    x_label="Product Category",
    y_label="Total Sales ($)"
)


# ==================================================
# 13. CATEGORY-WISE PROFIT ANALYSIS
# ==================================================

st.subheader("Category-wise Profit Performance")

category_profit = (
    df.groupby("Category")["Profit"]
    .sum()
    .reset_index()
)

st.bar_chart(
    category_profit,
    x="Category",
    y="Profit",
    x_label="Product Category",
    y_label="Total Profit ($)"
)


# ==================================================
# 14. MONTHLY SALES TREND
# ==================================================

st.divider()

st.subheader("Monthly Sales Trend")

monthly_sales = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = (
    monthly_sales["Order Date"].astype(str)
)

st.line_chart(
    monthly_sales,
    x="Order Date",
    y="Sales",
    x_label="Month",
    y_label="Total Sales ($)"
)


# ==================================================
# 15. MONTHLY PROFIT TREND
# ==================================================

st.divider()

st.subheader("Monthly Profit Trend")

monthly_profit = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )["Profit"]
    .sum()
    .reset_index()
)

monthly_profit["Order Date"] = (
    monthly_profit["Order Date"].astype(str)
)

st.line_chart(
    monthly_profit,
    x="Order Date",
    y="Profit",
    x_label="Month",
    y_label="Total Profit ($)"
)


# ==================================================
# 16. LOSS-MAKING SUBCATEGORY ANALYSIS
# ==================================================

st.divider()

st.subheader("Loss-Making Product Subcategories")

subcategory_profit = (
    df.groupby("Sub-Category")["Profit"]
    .sum()
    .reset_index()
)

loss_making = subcategory_profit[
    subcategory_profit["Profit"] < 0
].sort_values(
    by="Profit"
)


if not loss_making.empty:

    st.bar_chart(
        loss_making,
        x="Sub-Category",
        y="Profit",
        x_label="Product Subcategory",
        y_label="Total Loss ($)"
    )

else:

    st.success(
        "No loss-making subcategories found in this selection."
    )


# ==================================================
# 17. PREVIOUSLY GENERATED AI REPORT
# ==================================================

st.divider()

st.subheader("📄 Previously Generated AI Business Report")

report_path = "reports/ai_business_performance_report.md"

try:

    with open(
        report_path,
        "r",
        encoding="utf-8"
    ) as file:

        previous_report = file.read()

    st.markdown(previous_report)

except FileNotFoundError:

    st.info(
        "No previously generated AI report was found. "
        "Generate a new report below."
    )


# ==================================================
# 18. GEMINI AI INTEGRATION
# ==================================================

st.divider()

st.subheader("🤖 Generate AI Business Insights")

api_key = os.getenv("GEMINI_API_KEY")


if not api_key:

    st.error(
        "Gemini API key not found. Please check your .env file."
    )

else:

    client = genai.Client(api_key=api_key)

    if st.button("Generate AI Insights"):

        with st.spinner(
            "Gemini is analyzing your filtered business data..."
        ):

            try:

                # CATEGORY PERFORMANCE

                category_data = (
                    df.groupby("Category")
                    .agg(
                        Total_Sales=("Sales", "sum"),
                        Total_Profit=("Profit", "sum")
                    )
                    .reset_index()
                )

                category_data["Profit_Margin"] = (
                    category_data["Total_Profit"]
                    / category_data["Total_Sales"].replace(
                        0, float("nan")
                    )
                ) * 100


                # SUBCATEGORY PERFORMANCE

                subcategory_data = (
                    df.groupby("Sub-Category")
                    .agg(
                        Total_Sales=("Sales", "sum"),
                        Total_Profit=("Profit", "sum")
                    )
                    .reset_index()
                )

                subcategory_data["Profit_Margin"] = (
                    subcategory_data["Total_Profit"]
                    / subcategory_data["Total_Sales"].replace(
                        0, float("nan")
                    )
                ) * 100


                # LOSS-MAKING SUBCATEGORIES

                loss_making_data = subcategory_data[
                    subcategory_data["Total_Profit"] < 0
                ]


                # MONTHLY PERFORMANCE

                monthly_data = (
                    df.groupby(
                        df["Order Date"].dt.to_period("M")
                    )
                    .agg(
                        Monthly_Sales=("Sales", "sum"),
                        Monthly_Profit=("Profit", "sum")
                    )
                    .reset_index()
                )

                monthly_data["Month"] = (
                    monthly_data["Order Date"].astype(str)
                )

                monthly_data = monthly_data.drop(
                    columns=["Order Date"]
                )


                # FILTERED KPI SUMMARY

                business_data = {

                    "Applied Filters": {
                        "Category": selected_category,
                        "Region": selected_region,
                        "Start Date": str(start_date),
                        "End Date": str(end_date)
                    },

                    "Filtered Business KPIs": {
                        "Total Records": int(len(df)),
                        "Total Sales": round(float(total_sales), 2),
                        "Total Profit": round(float(total_profit), 2),
                        "Total Orders": int(total_orders),
                        "Profit Margin Percentage": round(
                            float(profit_margin), 2
                        ),
                        "Total Quantity Sold": total_quantity,
                        "Average Discount Percentage": average_discount
                    },

                    "Category Performance":
                        category_data.round(2).to_dict(
                            orient="records"
                        ),

                    "Subcategory Performance":
                        subcategory_data.round(2).to_dict(
                            orient="records"
                        ),

                    "Loss Making Subcategories":
                        loss_making_data.round(2).to_dict(
                            orient="records"
                        ),

                    "Monthly Performance":
                        monthly_data.round(2).to_dict(
                            orient="records"
                        )
                }


                # GEMINI PROMPT

                prompt = f"""
You are an experienced business data analyst.

Analyze the following FILTERED business dataset.

BUSINESS DATA:

{json.dumps(business_data, indent=2, default=str)}

IMPORTANT ANALYSIS RULES:

1. Use ONLY the supplied filtered business data.
2. Do not use figures from previously generated reports.
3. Clearly mention the applied category, region and date filters.
4. Use the exact supplied KPI values.
5. Never invent facts, numbers, or business causes.
6. Distinguish observed facts from possible explanations.
7. Do not claim seasonality from isolated monthly observations.
8. Do not assume discounts caused losses without evidence.
9. Do not call negative profit an operating loss.
10. Tie every recommendation to an actual finding.
11. If the cause is unknown, recommend further investigation.
12. If a category or subcategory is absent, do not invent one.
13. Do not claim that all months or years show growth unless the data proves it.
14. Clearly distinguish partial months from complete months when possible.

GENERATE A PROFESSIONAL BUSINESS REPORT WITH THESE SECTIONS:

1. Applied Filters
2. Overall Filtered Business Performance
3. Category-wise Performance
4. Subcategory-wise Performance
5. Monthly Trend Analysis
6. Important Business Findings
7. Actionable Business Recommendations

Use clear headings, bullet points and simple professional language.
"""


                # SEND DATA TO GEMINI

                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt
                )

                ai_report = response.output_text

                if not ai_report:

                    st.error(
                        "Gemini returned an empty report. "
                        "Please try again."
                    )

                    st.stop()


                # DISPLAY AI REPORT

                st.success(
                    "Filtered AI Business Analysis Completed!"
                )

                st.subheader("📊 AI-Generated Business Analysis")

                st.markdown(ai_report)


                # SAVE AI REPORT

                os.makedirs("reports", exist_ok=True)

                latest_report_path = (
                    "reports/latest_ai_generated_report.md"
                )

                with open(
                    latest_report_path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(ai_report)

                st.success("Filtered AI report saved successfully!")


                # DOWNLOAD MARKDOWN REPORT

                st.download_button(
                    label="📥 Download AI Business Report (Markdown)",
                    data=ai_report,
                    file_name="AI_Business_Performance_Report.md",
                    mime="text/markdown"
                )


                # GENERATE PDF

                pdf_data = create_pdf_report(ai_report)


                # DOWNLOAD PDF

                st.download_button(
                    label="📄 Download AI Business Report (PDF)",
                    data=pdf_data,
                    file_name="AI_Business_Performance_Report.pdf",
                    mime="application/pdf"
                )

                st.success(
                    "Your AI business report is ready "
                    "in both Markdown and PDF formats!"
                )


            except Exception as e:

                st.error(
                    f"Unable to generate AI insights: {e}"
                )


# ==================================================
# 19. PROJECT FOOTER
# ==================================================

st.divider()

st.caption(
    "AI-Powered KPI Interpreter | "
    "Python • Pandas • Streamlit • Google Gemini • ReportLab"
)


# ==================================================
# RUN STREAMLIT
# ==================================================
# Run in terminal:
# streamlit run app.py
#Local URL: http://localhost:8502
#Network URL: http://192.168.1.10:8502
