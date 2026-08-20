"""
Project Report PDF Generator for Task 2: Library Management System
Internship: Python Development Internship
Applicant: KASARABOINA SRINU (ID: KTS020260716223)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_report(output_pdf_path="Library_Management_System_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1a365d"),
        alignment=1,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4a5568"),
        alignment=1,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2b6cb0"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2d3748"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2d3748"),
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("<b>INTERNSHIP PROJECT REPORT</b>", title_style))
    story.append(Paragraph("<b>Task 2: Library Management System (Python OOP & Automation)</b>", subtitle_style))
    story.append(Spacer(1, 10))

    # Metadata Table
    meta_data = [
        [Paragraph("<b>Candidate Name:</b>", body_style), Paragraph("KASARABOINA SRINU", body_style)],
        [Paragraph("<b>Application ID:</b>", body_style), Paragraph("KTS020260716223", body_style)],
        [Paragraph("<b>Internship Track:</b>", body_style), Paragraph("Python Development Internship", body_style)],
        [Paragraph("<b>Duration:</b>", body_style), Paragraph("30 Days (20 July 2026 – 19 August 2026)", body_style)],
        [Paragraph("<b>Supervisor / HR:</b>", body_style), Paragraph("Prince Asthana (HR Executive)", body_style)],
    ]
    t = Table(meta_data, colWidths=[150, 380])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    summary_text = (
        "The Library Management System is an automated, Object-Oriented Python application engineered "
        "to manage book inventories, student/patron memberships, borrowing quotas, loan tracking, and "
        "automated overdue fine assessments. The solution provides complete transaction safety, atomic persistence, "
        "and rich analytics."
    )
    story.append(Paragraph(summary_text, body_style))

    # Key Features
    story.append(Paragraph("2. Key Architectural Features & Capabilities", h1_style))
    features = [
        "<b>Catalog Management:</b> Real-time inventory tracking with physical copy counts and automated stock decrementing.",
        "<b>Member Management:</b> Patron registration with max book borrowing constraints and active issue histories.",
        "<b>Automated Loan Lifecycle:</b> 14-day borrowing cycles with automatic due date computation and return processing.",
        "<b>Overdue Fine Engine:</b> Automatically computes late fees based on exact overdue return timestamps.",
        "<b>Search & Filter Engine:</b> Substring filtering across ISBN, title, author, and category.",
        "<b>Analytics:</b> Metrics on most borrowed books, active loans, and fine revenues.",
        "<b>Pytest Coverage:</b> 100% test pass rate for borrowing, return, and fine calculations."
    ]
    for feat in features:
        story.append(Paragraph(f"• {feat}", bullet_style))

    doc.build(story)
    print(f"Report generated successfully at: {os.path.abspath(output_pdf_path)}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    generate_report(os.path.join(out_dir, "Library_Management_System_Project_Report.pdf"))
