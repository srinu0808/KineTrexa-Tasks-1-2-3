"""
Project Report PDF Generator for Task 1: Student Management System
Internship: Python Development Internship
Applicant: KASARABOINA SRINU (ID: KTS020260716223)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_report(output_pdf_path="Student_Management_System_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1a365d"),
        alignment=1, # Center
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

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Code'],
        fontSize=8.5,
        leading=11,
        fontName='Courier',
        textColor=colors.HexColor("#1a202c"),
        backColor=colors.HexColor("#edf2f7"),
        borderColor=colors.HexColor("#cbd5e0"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    story = []

    # Title Banner
    story.append(Paragraph("<b>INTERNSHIP PROJECT REPORT</b>", title_style))
    story.append(Paragraph("<b>Task 1: Student Management System (Python OOP & Persistence)</b>", subtitle_style))
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
        "The Student Management System is a modular, production-ready Python application engineered "
        "to streamline academic record keeping. The solution adheres strictly to Object-Oriented "
        "Programming (OOP) principles, clean architecture patterns, defensive validation, robust exception "
        "handling, dual persistence layers (JSON & CSV), and provides an interactive terminal user interface."
    )
    story.append(Paragraph(summary_text, body_style))

    # Key Features
    story.append(Paragraph("2. Key Architectural Features & Capabilities", h1_style))
    features = [
        "<b>Object-Oriented Design (OOP):</b> Domain models (<code>Student</code>, <code>Course</code>) featuring properties, private member encapsulation, and custom serialization methods.",
        "<b>Complete CRUD Operations:</b> Create, Read, Update, and Delete operations for student records with rollback safety.",
        "<b>GPA & Academic Tracking:</b> Dynamic weighted GPA computation based on course credit hours and numerical grade points.",
        "<b>Search & Multi-criteria Filtering:</b> Instant substring search across roll numbers, names, departments, and emails, with GPA and status filters.",
        "<b>Defensive Validation & Custom Exceptions:</b> Regex-based email and phone verification, non-empty checks, and custom error classes (<code>DuplicateRollNumberError</code>, <code>ValidationError</code>).",
        "<b>Dual Persistence Engine:</b> Atomic JSON file operations with temporary swap protection and CSV import/export capabilities.",
        "<b>Automated Test Suite:</b> Comprehensive Pytest unit tests achieving high coverage of domain and service layer logic."
    ]
    for feat in features:
        story.append(Paragraph(f"• {feat}", bullet_style))

    # System Architecture Diagram / Component Table
    story.append(Paragraph("3. Module Structure", h1_style))
    arch_data = [
        ["Layer / Module", "File Path", "Responsibility"],
        ["Domain Models", "src/models/student.py", "Encapsulates Student state, GPA computation, course enrollment."],
        ["Course Entity", "src/models/course.py", "Course definitions, credit weighting, and grade points."],
        ["Storage Layer", "src/storage/json_storage.py", "Atomic JSON persistence with crash recovery mechanism."],
        ["Export / Import", "src/storage/csv_storage.py", "Bulk CSV data import and export operations."],
        ["Service Layer", "src/services/student_service.py", "Core business logic, search, filter, and analytics."],
        ["CLI Interface", "src/ui/cli.py", "Interactive menu-driven terminal interface with styled tables."],
        ["Test Suite", "tests/test_student_service.py", "Automated validation for CRUD, duplicates, and edge cases."]
    ]
    arch_table = Table(arch_data, colWidths=[100, 160, 270])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2b6cb0")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 15))

    # Verification and Test Results
    story.append(Paragraph("4. Verification & Testing", h1_style))
    story.append(Paragraph(
        "The project was verified using Pytest. All unit tests covering student registration, duplicate prevention, "
        "data format validation, GPA calculation, search/filter algorithms, and storage persistence executed successfully.",
        body_style
    ))

    # Conclusion & Learning Outcomes
    story.append(Paragraph("5. Learning Outcomes & Conclusion", h1_style))
    conclusion = (
        "During this assignment, industry best practices in Python development were implemented, including "
        "modular project architecture, SOLID principles, type annotations, unit testing, and automated documentation. "
        "The application is fully extensible for future database (SQL/NoSQL) and REST API integrations."
    )
    story.append(Paragraph(conclusion, body_style))

    doc.build(story)
    print(f"Report generated successfully at: {os.path.abspath(output_pdf_path)}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    generate_report(os.path.join(out_dir, "Student_Management_System_Project_Report.pdf"))
