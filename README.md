# AI-Powered KPI Interpreter
### Automated Business Performance Analysis and Insight Generation

## Project Overview

The AI-Powered KPI Interpreter is a Python-based data analytics application that transforms business data into meaningful insights using data analysis, interactive visualizations, and Generative AI.

Users can upload business datasets, calculate key performance indicators (KPIs), explore business trends, and generate AI-powered reports with recommendations.

The project combines traditional data analytics with Google's Gemini AI to make business performance analysis easier to understand.

## Key Features

- **Dataset Upload:** Supports CSV, XLS, and XLSX files.
- **Data Validation:** Checks required columns, missing values, and data types.
- **Interactive Filters:** Filter data by category, region, and order date.
- **KPI Calculation:** Calculates total sales, total profit, total orders, quantity sold, average discount, and profit margin.
- **Category Analysis:** Compares sales and profitability across categories and subcategories.
- **Trend Analysis:** Examines monthly sales and profit trends.
- **Data Visualization:** Presents business performance through charts.
- **AI-Powered Insights:** Uses Google Gemini to interpret filtered business metrics and generate recommendations.
- **Report Generation:** Generates downloadable Markdown and PDF reports.
- **KPI Verification:** Independently verifies dashboard calculations using Python.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Streamlit | Interactive dashboard |
| Google Gemini API | Generative AI insights |
| ReportLab | PDF report generation |
| python-dotenv | Environment variable management |
| Git and GitHub | Version control |

## Project Workflow

1. Upload a business dataset.
2. Validate and prepare the dataset.
3. Apply category, region, and date filters.
4. Calculate key business performance indicators.
5. Analyze category-wise and monthly performance.
6. Generate visualizations.
7. Send filtered analytical results to Gemini.
8. Generate business findings and recommendations.
9. Download the AI-generated report in Markdown or PDF format.
10. Independently verify KPI calculations.

## Key Performance Indicators

The application calculates:

- Total Sales
- Total Profit
- Total Orders
- Total Quantity Sold
- Average Discount Percentage
- Profit Margin Percentage

## Dataset

This project uses the **Tableau Sample Superstore** dataset for demonstration and analysis.

- Records: 10,194
- Columns: 21
- Data includes order details, customer information, product categories, sales, quantity, discount, and profit.

Dataset source: [Tableau Sample Superstore](https://public.tableau.com/app/sample-data/sample_-_superstore.xls)

This is a sample dataset, not real company transaction data.

## Project Structure

```text
AI_Powered_KPI_Interpreter/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── sample_-_superstore.xls
│   └── cleaned_superstore.csv
│
├── src/
│   ├── load_dataset.py
│   ├── clean_data.py
│   ├── kpi_calculation.py
│   ├── visualize_kpis.py
│   ├── test_gemini.py
│   ├── generate_ai_insights.py
│   ├── generate_pdf_report.py
│   ├── test_libraries.py
│   └── verify_dashboard_kpis.py
│
├── reports/
│   ├── AI_Business_Performance_Report.pdf
│   ├── ai_business_performance_report.md
│   ├── latest_ai_generated_report.md
│   ├── monthly_kpi_report.csv
│   ├── monthly_sales_trend.png
│   └── monthly_profit_trend.png
│
└── notebooks/
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/kavyasreekaparthi-hub/AI-Powered-KPI-Interpreter.git
cd AI-Powered-KPI-Interpreter
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Gemini API key

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Obtain an API key through [Google AI Studio](https://aistudio.google.com/).

**Important:** Never upload your `.env` file or expose your API key publicly.

### 6. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## Example Business Analysis

The project was tested using category-based filters.

**Technology Category**

- Total Sales: $839,893.28
- Total Profit: $146,543.38
- Total Orders: 1,560
- Profit Margin: 17.45%

**Office Supplies Category**

- Total Sales: $731,893.31
- Total Profit: $126,023.44
- Total Orders: 3,812
- Profit Margin: 17.22%

These KPI values were independently verified using Python.

## Generative AI Integration

Google Gemini analyzes calculated business metrics and generates:

- Business performance summaries
- Category and subcategory insights
- Monthly trend observations
- Identification of loss-making areas
- Actionable business recommendations

The AI analysis uses calculated results from the selected filters. Recommendations are based on the supplied data; potential causes are not treated as confirmed facts without supporting evidence.

## Future Enhancements

- PDF business report data extraction.
- Automated anomaly detection.
- Advanced chart and visual analysis.
- Support for additional business datasets and KPI definitions.
- Improved AI-generated explanations and recommendations.

## Project Information

**Project:** AI-Powered KPI Interpreter

**Domain:** Data Analytics and Generative AI

**Purpose:** Hands-on portfolio project demonstrating Python, data analytics, dashboard development, business intelligence, and Generative AI integration.