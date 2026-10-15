# src/visualizer.py
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# ... Keep your existing generate_performance_chart and generate_ledger_chart functions exactly the same ...

def generate_pdf_report(execution_mode, report_text, labels, latencies, throughputs):
    """
    Compiles live architecture execution statistics and risk analytical metrics 
    into a production-grade binary PDF report stream.
    """
    buffer = BytesIO()
    
    # 1. Initialize Document Canvas (With 1-inch uniform margin boundaries)
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=72, leftMargin=72, 
        topMargin=72, bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom Brand Colors Mapping
    PRIMARY_COLOR = colors.HexColor("#1A365D")   # Deep Corporate Navy
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") # Pipeline Slate Blue
    TEXT_COLOR = colors.HexColor("#2D3748")      # Charcoal Body Text
    
    # 2. Configure Robust Text Topography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY_COLOR,
        spaceAfter=12
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#718096"),
        spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'DocSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=SECONDARY_COLOR,
        spaceBefore=14,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=TEXT_COLOR,
        spaceAfter=10
    )

    # 3. Build Document Header Section
    story.append(Paragraph("B2B Credit Risk Compliance Audit Report", title_style))
    story.append(Paragraph(f"Data Pipeline Mode: {execution_mode} | Compliance Evaluation Run: Active State", meta_style))
    story.append(Spacer(1, 10))
    
    # 4. Generate Telemetry Metrics Infrastructure Table Grid
    story.append(Paragraph("System Execution Performance Telemetry", section_style))
    
    table_data = [
        ["Model Variant Architecture", "Latency Profile", "Throughput Metrics"],
        [labels[0], f"{latencies[0]:.3f}s" if latencies[0] > 0 else "Offline", f"{throughputs[0]:.1f} TPS"],
        [labels[1], f"{latencies[1]:.3f}s" if latencies[1] > 0 else "Offline", f"{throughputs[1]:.1f} TPS"],
        [labels[2], f"{latencies[2]:.3f}s" if latencies[2] > 0 else "Offline", f"{throughputs[2]:.1f} TPS"],
        [labels[3], f"{latencies[3]:.3f}s" if latencies[3] > 0 else "Offline", f"{throughputs[3]:.1f} TPS"]
    ]
    
    perf_table = Table(table_data, colWidths=[220, 120, 120])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(perf_table)
    story.append(Spacer(1, 20))
    
    # 5. Parse, Sanitize and Clean Credit Board Text Output
    story.append(Paragraph("Executive Credit Risk Valuation & Findings", section_style))
    
    # Clean text strings formatting to safely match PDF canvas boundaries
    cleaned_report_text = report_text.replace("###", "").replace("####", "").replace("*", "-")
    for line in cleaned_report_text.split('\n'):
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
            
    # 6. Render Completed Document Stream Pipeline
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
