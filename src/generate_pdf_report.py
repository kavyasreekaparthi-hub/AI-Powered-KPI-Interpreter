
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)


def generate_pdf_report(
    report_text,
    output_path="reports/AI_Business_Performance_Report.pdf"
):

    # Create reports folder if it does not exist
    os.makedirs("reports", exist_ok=True)

    # Create PDF document
    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom title style
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=15
    )

    # Heading style
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=12,
        spaceAfter=8
    )

    # Body text style
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=7
    )

    story = []

    # PDF title
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

    # Convert Gemini Markdown report into PDF paragraphs
    for line in report_text.split("\n"):

        line = line.strip()

        if not line:
            story.append(Spacer(1, 5))
            continue

        if line.startswith("# "):
            story.append(
                Paragraph(
                    line[2:],
                    title_style
                )
            )

        elif line.startswith("## "):
            story.append(
                Paragraph(
                    line[3:],
                    heading_style
                )
            )

        elif line.startswith("### "):
            story.append(
                Paragraph(
                    line[4:],
                    heading_style
                )
            )

        elif line.startswith("---"):
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=colors.grey
                )
            )

        else:
            # Basic Markdown formatting
            line = line.replace("&", "&amp;")
            line = line.replace("<", "&lt;")
            line = line.replace(">", "&gt;")

            line = line.replace("**", "")

            if line.startswith("- "):
                line = "&#8226; " + line[2:]

            elif line.startswith("* "):
                line = "&#8226; " + line[2:]

            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

    # Generate PDF
    document.build(story)

    print("PDF report generated successfully!")
    print("Saved at:", output_path)


if __name__ == "__main__":

    report_path = "reports/latest_ai_generated_report.md"

    with open(
        report_path,
        "r",
        encoding="utf-8"
    ) as file:

        report_text = file.read()

    generate_pdf_report(report_text)
    
    
    
    
    
    
    
    
    
    

# python src/generate_pdf_report.py