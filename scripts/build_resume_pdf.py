"""Script to generate a pristine, professional, ATS-friendly PDF resume
from Nithin's official AI Engineer resume document.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

def generate_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.45 * inch,
        bottomMargin=0.45 * inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    name_style = ParagraphStyle(
        'DocName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=2
    )

    tagline_style = ParagraphStyle(
        'DocTagline',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#ea580c'), # Vibrant Coral/Orange accent
        spaceAfter=3
    )

    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569')
    )

    section_heading = ParagraphStyle(
        'DocSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f172a'),
        textTransform='uppercase',
        spaceBefore=7,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b')
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        leftIndent=12,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=1.5
    )

    item_title_left = ParagraphStyle(
        'ItemTitleLeft',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0f172a')
    )

    item_title_right = ParagraphStyle(
        'ItemTitleRight',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=TA_RIGHT,
        textColor=colors.HexColor('#64748b')
    )

    item_subtitle = ParagraphStyle(
        'ItemSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#ea580c'),
        spaceAfter=2
    )

    story = []

    # Header
    story.append(Paragraph("NITHIN DHARAVATHU", name_style))
    story.append(Paragraph("Agentic AI Engineer | Python, FastAPI, LLMs &amp; RAG", tagline_style))

    contact_line = (
        "Hyderabad, India &bull; +91 6304801278 &bull; "
        "<a href='mailto:nithindharavath01@gmail.com' color='#0284c7'>nithindharavath01@gmail.com</a> &bull; "
        "<a href='https://linkedin.com/in/nithin-dharavathu' color='#0284c7'>LinkedIn</a> &bull; "
        "<a href='https://github.com/Nithin-dharavath' color='#0284c7'>GitHub</a> &bull; "
        "<a href='https://portfolio-website-phi-three-52.vercel.app' color='#0284c7'>Portfolio</a>"
    )
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=4))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = (
        "AI &amp; ML graduate and Python backend developer (FastAPI, Flask) building Agentic AI applications with "
        "LLMs, RAG pipelines, semantic search, and LangChain/LangGraph agents. Built an end-to-end AI-powered incident "
        "management platform with vector search (Qdrant), tool-calling agents, and Dockerized CI/CD, and integrated ML "
        "models into production-style REST APIs during Microsoft and EY internships. Seeking an Agentic AI Engineer role "
        "to build intelligent, production-ready AI applications."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceBefore=4, spaceAfter=4))

    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", section_heading))
    skills = [
        ("Agentic AI:", "LLM APIs (OpenAI-compatible, Ollama), RAG, Semantic Search, Qdrant, HuggingFace Embeddings, AI Agents, Prompt Engineering, Tool Calling, HITL, MCP."),
        ("AI Frameworks:", "LangChain, LangGraph, HuggingFace, ML fundamentals."),
        ("Backend & APIs:", "Python, FastAPI, REST APIs, Pydantic, SQLAlchemy, JWT/OAuth2, RBAC."),
        ("Databases:", "PostgreSQL, MySQL, SQLite, Qdrant (Vector DB)."),
        ("Cloud & DevOps:", "AWS (EC2, S3), Docker, GitHub Actions (CI/CD), Railway, Vercel."),
        ("Tools & Practices:", "Git, GitHub, Pytest, n8n, SDLC, Debugging &amp; Performance Optimization."),
        ("Languages:", "Python, JavaScript, SQL.")
    ]
    for label, desc in skills:
        line = f"<b>{label}</b> {desc}"
        story.append(Paragraph(line, body_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceBefore=4, spaceAfter=4))

    # Projects
    story.append(Paragraph("PROJECTS", section_heading))

    # Project 1
    t1 = Table([
        [Paragraph("AI-Powered Incident &amp; Management Support System", item_title_left),
         Paragraph("Personal Project", item_title_right)]
    ], colWidths=[5.2 * inch, 2.3 * inch])
    t1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
    story.append(t1)
    story.append(Paragraph("Python, FastAPI, PostgreSQL, LangChain, LangGraph, Qdrant, HuggingFace", item_subtitle))
    story.append(Paragraph("&bull; Designed and built a backend AI platform to report, track, and resolve IT incidents, with LLM-powered classification of category, severity, priority, and assigned team, plus AI-generated incident summaries.", bullet_style))
    story.append(Paragraph("&bull; Developed a LangGraph support agent with tool calling and human-in-the-loop review, with AI root-cause analysis.", bullet_style))
    story.append(Paragraph("&bull; Containerized with Docker, automated testing and deployment through GitHub Actions CI/CD, with Pytest coverage.", bullet_style))
    story.append(Spacer(1, 3))

    # Project 2
    t2 = Table([
        [Paragraph("Online Voting System", item_title_left),
         Paragraph("Personal Project", item_title_right)]
    ], colWidths=[5.2 * inch, 2.3 * inch])
    t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
    story.append(t2)
    story.append(Paragraph("Python, FastAPI, MySQL, JWT, Jinja2", item_subtitle))
    story.append(Paragraph("&bull; Built a secure voting platform with JWT authentication, RBAC, and CSRF protection for Admin and Student roles.", bullet_style))
    story.append(Paragraph("&bull; Developed 10+ backend modules (election management, vote verification, result publication, one-vote-per-user enforcement) on a normalized MySQL schema with 6+ relational tables, secure file uploads, and audit verification.", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceBefore=4, spaceAfter=4))

    # Experience
    story.append(Paragraph("EXPERIENCE", section_heading))

    # Exp 1
    te1 = Table([
        [Paragraph("Freelance Web Developer", item_title_left),
         Paragraph("2026 &ndash; Present", item_title_right)]
    ], colWidths=[5.2 * inch, 2.3 * inch])
    te1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
    story.append(te1)
    story.append(Paragraph("&bull; Build AI-integrated websites and online booking systems for local businesses using Python backends, REST APIs, and modern web technologies.", bullet_style))
    story.append(Paragraph("&bull; Handle requirements gathering, development, deployment, and client communication end to end.", bullet_style))
    story.append(Spacer(1, 2))

    # Exp 2
    te2 = Table([
        [Paragraph("AI Azure Virtual Intern, Microsoft", item_title_left),
         Paragraph("May 2025 &ndash; June 2025", item_title_right)]
    ], colWidths=[5.2 * inch, 2.3 * inch])
    te2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
    story.append(te2)
    story.append(Paragraph("&bull; Integrated Random Forest and XGBoost models into a FastAPI backend, exposing secure REST APIs for real-time insurance premium prediction.", bullet_style))
    story.append(Paragraph("&bull; Validated model performance with ML metrics and added Pydantic validation and exception handling, improving prediction reliability and API efficiency.", bullet_style))
    story.append(Spacer(1, 2))

    # Exp 3
    te3 = Table([
        [Paragraph("NextGen Intern, EY (Spendly &ndash; Personal Expense Tracker)", item_title_left),
         Paragraph("Feb 2025 &ndash; March 2025", item_title_right)]
    ], colWidths=[5.2 * inch, 2.3 * inch])
    te3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
    story.append(te3)
    story.append(Paragraph("&bull; Developed a Flask application (HTML/CSS/JS) with REST API integration, CRUD operations, authentication, and session handling using clean application architecture.", bullet_style))
    story.append(Paragraph("&bull; Managed relational data with SQLite and SQLAlchemy in a database-driven application.", bullet_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceBefore=4, spaceAfter=4))

    # Education
    story.append(Paragraph("EDUCATION", section_heading))
    tedu = Table([
        [Paragraph("<b>B.Tech, Computer Engineering (AI &amp; ML)</b> &ndash; Vaagdevi College of Engineering, Warangal", body_style),
         Paragraph("2026", item_title_right)]
    ], colWidths=[6.2 * inch, 1.3 * inch])
    tedu.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
    story.append(tedu)
    story.append(Paragraph("CGPA/Percentage: 74.6% &nbsp;&bull;&nbsp; Languages: English, Hindi, Telugu", body_style))

    doc.build(story)
    print(f"Successfully generated {output_path}")

if __name__ == '__main__':
    generate_pdf("static/resume/nithin-resume.pdf")
