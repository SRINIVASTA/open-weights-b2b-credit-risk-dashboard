# src/visualizer.py
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_performance_chart(latencies, throughputs):
    """
    Generates comparative engine visualization bar charts.
    """
    models = ['Qwen', 'GPT-OSS', 'Gemma 31B', 'Gemma 26B']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=models, y=latencies, name='Latency (s)', marker_color='#d9534f'))
    fig.add_trace(go.Bar(x=models, y=throughputs, name='Throughput (TPS)', marker_color='#5cb85c'))
    fig.update_layout(
        title="Throughput Rate Profile (Tokens/Sec)",
        template='plotly_white', 
        barmode='group', 
        height=260,
        margin=dict(l=40, r=40, t=40, b=30)
    )
    return fig

def generate_ledger_chart():
    """
    Generates an Intramonth Ledger Simulation.
    """
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

    fig.add_trace(go.Scatter(x=list(days), y=daily_balances, mode='lines+markers', name='Ledger Balance (INR)', line=dict(color='#1A365D', width=2)))
    fig.add_trace(go.Scatter(x=[1, 30], y=[adlb, adlb], mode='lines', name=f'Actual ADLB (INR {adlb:,.0f})', line=dict(color='#f0ad4e', dash='dash')))
    fig.add_trace(go.Scatter(x=[1, 30], y=[5000, 5000], mode='lines', name='Conservative Floor (INR 5,000)', line=dict(color='#d9534f', dash='dot')))

    fig.update_layout(
        title="30-Day Working Capital Volatility Curve",
        template='plotly_white', 
        height=260, 
        margin=dict(l=40, r=40, t=40, b=30), 
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def generate_pdf_report(execution_mode, report_text, labels, latencies, throughputs):
    """
    Compiles data metrics and translates Plotly layout visual vector figures 
    directly into embedded flowable image nodes within the final PDF asset.
    """
    buffer = BytesIO()
    
    # Initialize Document Canvas (0.5-inch compact margin mapping to prevent overflow)
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=36, leftMargin=36, 
        topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    PRIMARY_COLOR = colors.HexColor("#1A365D")   
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") 
    TEXT_COLOR = colors.HexColor("#2D3748")      
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY_COLOR,
        spaceAfter=4,
        alignment=1 
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=SECONDARY_COLOR,
        spaceAfter=15,
        alignment=1
    )
    
    section_style = ParagraphStyle(
        'DocSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY_COLOR,
        spaceBefore=12,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_COLOR,
        spaceAfter=6
    )

    # 1. Document Title Headers
    story.append(Paragraph("B2B Risk Intelligence Due Diligence Export", title_style))
    story.append(Paragraph(f"Data Generation Profile: Executed via [{execution_mode}] Pipeline", meta_style))
    story.append(Spacer(1, 8))
    
    # 2. Performance Comparison Metrics Grid Table
    table_data = [["Model Target Cluster", "Inference Latency", "Throughput Rate"]]
    for i in range(len(labels)):
        lat_val = f"{latencies[i]:.3f}s" if latencies[i] > 0 else "Offline"
        tps_val = f"{throughputs[i]:.1f} TPS" if throughputs[i] > 0 else "0.0 TPS"
        table_data.append([labels[i], lat_val, tps_val])
        
    perf_table = Table(table_data, colWidths=[200, 160, 160])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F7FAFC")),
        ('TEXTCOLOR', (0, 0), (-1, 0), SECONDARY_COLOR),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 15))
    
    # 3. PIPELINE GRAPH CONVERSION 1: Compute Performance Model Chart
    try:
        fig_perf = generate_performance_chart(latencies, throughputs)
        img_bytes_perf = fig_perf.to_image(format="png", width=520, height=240)
        story.append(Paragraph("Visual Asset: Compute Performance Model", section_style))
        story.append(Image(BytesIO(img_bytes_perf), width=480, height=220))
        story.append(Spacer(1, 15))
    except Exception:
        pass # Graceful fallback if image compilation initialization lags

    # 4. PIPELINE GRAPH CONVERSION 2: Volatility Capital Curve Chart
    try:
        fig_ledger = generate_ledger_chart()
        img_bytes_ledger = fig_ledger.to_image(format="png", width=520, height=240)
        story.append(Paragraph("Visual Asset: Intramonth Ledger Simulation", section_style))
        story.append(Image(BytesIO(img_bytes_ledger), width=480, height=220))
        story.append(Spacer(1, 15))
    except Exception:
        pass

    # 5. Narrative Text Section
    story.append(Paragraph("Executive Credit Risk Evaluation Report", section_style))
    cleaned_report_text = report_text.replace("###", "").replace("####", "").replace("**", "").replace("*", "-")
    for line in cleaned_report_text.split('\n'):
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
            
    # Compile and stream binary vector arrays
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
