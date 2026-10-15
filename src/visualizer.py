# src/visualizer.py
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_performance_chart(latencies, throughputs):
    """Generates comparative engine visualization bar charts."""
    models = ['Qwen', 'GPT-OSS', 'Gemma 31B', 'Gemma 26B']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=models, y=latencies, name='Latency (s)', marker_color='#3182ce'))
    fig.add_trace(go.Bar(x=models, y=throughputs, name='Throughput (TPS)', marker_color='#e53e3e'))
    fig.update_layout(
        title="Throughput Rate Profile (Tokens/Sec)",
        template='plotly_white', 
        barmode='group', 
        height=240,
        margin=dict(l=40, r=40, t=40, b=30)
    )
    return fig

def generate_ledger_chart():
    """Generates an Intramonth Ledger Simulation for working capital tracking."""
    np.random.seed(42)
    days = np.arange(1, 31)
    daily_balances = []
    current_balance = 4500 

    for day in days:
        if day == 1 or day == 15: 
            current_balance -= 65000  
        elif (7 <= day <= 10) or (24 <= day <= 27):
            current_balance += np.random.randint(18000, 32000) 
        else:
            current_balance += np.random.randint(-4000, 5000) 
        daily_balances.append(current_balance)

    adlb = np.mean(daily_balances)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=list(days), y=daily_balances, mode='lines+markers', name='Ledger Balance (INR)', line=dict(color='#2b6cb0', width=2)))
    # Fixed: Passing clean index lists to maintain robust syntax compiling
    fig.add_trace(go.Scatter(x=[1, 30], y=[adlb, adlb], mode='lines', name=f'Actual ADLB', line=dict(color='#dd6b20', dash='dash')))
    fig.add_trace(go.Scatter(x=[1, 30], y=[5000, 5000], mode='lines', name='Conservative Floor', line=dict(color='#e53e3e', dash='dot')))

    fig.update_layout(
        title="30-Day Working Capital Volatility Curve",
        template='plotly_white', 
        height=240, 
        margin=dict(l=40, r=40, t=40, b=30), 
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def generate_pdf_report(execution_mode, report_text, labels, latencies, throughputs):
    """Compiles a professional, multi-page regulatory credit portfolio PDF dossier."""
    buffer = BytesIO()
    
    # Page Canvas Bounds Initialization
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=54, leftMargin=54, 
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    PRIMARY_COLOR = colors.HexColor("#1A365D")   
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") 
    TEXT_COLOR = colors.HexColor("#2D3748")      
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
        fontSize=24, leading=28, textColor=PRIMARY_COLOR, spaceAfter=8, alignment=1 
    )
    meta_style = ParagraphStyle(
        'DocMeta', parent=styles['Normal'], fontName='Helvetica-Bold',
        fontSize=10, leading=14, textColor=SECONDARY_COLOR, spaceAfter=20, alignment=1
    )
    section_style = ParagraphStyle(
        'DocSection', parent=styles['Heading2'], fontName='Helvetica-Bold',
        fontSize=14, leading=18, textColor=PRIMARY_COLOR, spaceBefore=15, spaceAfter=10
    )
    body_style = ParagraphStyle(
        'DocBody', parent=styles['Normal'], fontName='Helvetica',
        fontSize=10, leading=15, textColor=TEXT_COLOR, spaceAfter=10
    )

    # ================= PAGE 1: TELEMETRY RUN REPORT =================
    story.append(Paragraph("B2B Risk Intelligence Due Diligence Export", title_style))
    story.append(Paragraph(f"Data Generation Profile: Executed via [{execution_mode}] Pipeline", meta_style))
    story.append(Spacer(1, 15))
    
    # Telemetry Table Creation
    table_data = [["Model Target Cluster", "Inference Latency", "Throughput Rate"]]
    for i in range(len(labels)):
        lat_val = f"{latencies[i]:.3f}s" if latencies[i] > 0 else "Offline"
        tps_val = f"{throughputs[i]:.1f} TPS" if throughputs[i] > 0 else "0.0 TPS"
        table_data.append([labels[i], lat_val, tps_val])
        
    perf_table = Table(table_data, colWidths=[200, 150, 150])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F7FAFC")),
        ('TEXTCOLOR', (0, 0), (-1, 0), SECONDARY_COLOR),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 20))
    
    # Render Inline Telemetry Vector Graphic
    try:
        fig_perf = generate_performance_chart(latencies, throughputs)
        img_perf = fig_perf.to_image(format="png", width=600, height=250)
        story.append(Paragraph("Visual Asset: Compute Performance Model", section_style))
        story.append(Image(BytesIO(img_perf), width=500, height=210))
    except Exception:
        story.append(Paragraph("[Performance Visualization Block Influx Transient]", body_style))
        
    story.append(PageBreak()) # Split to Page 2

    # ================= PAGE 2: LEDGER RISK CURVE ANALYSIS =================
    try:
        fig_ledger = generate_ledger_chart()
        img_ledger = fig_ledger.to_image(format="png", width=600, height=250)
        story.append(Paragraph("Visual Asset: Intramonth Ledger Simulation", section_style))
        story.append(Spacer(1, 10))
        story.append(Image(BytesIO(img_ledger), width=500, height=210))
    except Exception:
        story.append(Paragraph("[Ledger Visualization Block Influx Transient]", body_style))
        
    story.append(Spacer(1, 25))
    story.append(Paragraph("Executive Credit Risk Evaluation Report", section_style))
    story.append(Spacer(1, 5))
    
    # ================= PAGES 3+: NARRATIVE CONTEXT & METRICS MATRIX =================
    # Clean text markup structures to map smoothly within PDF constraints
    cleaned_text = report_text.replace("###", "").replace("####", "").replace("**", "").replace("*", "-")
    for line in cleaned_text.split('\n'):
        if line.strip():
            if "Risk Factor" in line or "Metric | Status" in line:
                story.append(PageBreak()) # Move structural matrices to their own page safely
            story.append(Paragraph(line.strip(), body_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
