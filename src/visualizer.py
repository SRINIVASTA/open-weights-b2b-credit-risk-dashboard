# src/visualizer.py
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Forces clean background headless server rendering mode
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_performance_chart(latencies, throughputs):
    """Generates the interactive Plotly workspace chart for the UI grid screen."""
    models = ['Qwen', 'GPT-OSS', 'Gemma 31B', 'Gemma 26B']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=models, y=latencies, name='Latency (s)', marker_color='#d9534f'))
    fig.add_trace(go.Bar(x=models, y=throughputs, name='Throughput (TPS)', marker_color='#5cb85c'))
    fig.update_layout(template='plotly_white', barmode='group', height=300)
    return fig

def generate_ledger_chart():
    """Generates the interactive Plotly workspace ledger timeline for the UI grid screen."""
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
    fig.add_trace(go.Scatter(x=[1, 30], y=[adlb, adlb], mode='lines', name='Actual ADLB', line=dict(color='#f0ad4e', dash='dash')))
    fig.add_trace(go.Scatter(x=[1, 30], y=[5000, 5000], mode='lines', name='Conservative Floor', line=dict(color='#d9534f', dash='dot')))
    fig.update_layout(title="30-Day Working Capital Volatility Curve", template='plotly_white', height=300)
    return fig

def _render_mpl_perf_chart(latencies, throughputs):
    """Generates a pure graphical image stream buffer using Matplotlib engine."""
    models = ['Qwen', 'GPT-OSS', 'Gemma 31B', 'Gemma 26B']
    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6.5, 3))
    ax.bar(x - width/2, latencies, width, label='Latency (s)', color='#d9534f')
    ax.bar(x + width/2, throughputs, width, label='Throughput (TPS)', color='#5cb85c')
    
    ax.set_title('Throughput Rate Profile (Tokens/Sec)', fontsize=11, fontweight='bold', color='#1A365D')
    ax.set_ylabel('Metrics Scale')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.legend(loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf

def _render_mpl_ledger_chart():
    """Generates a pure graphical image stream buffer using Matplotlib engine."""
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

    fig, ax = plt.subplots(figsize=(6.5, 3))
    ax.plot(days, daily_balances, marker='o', color='#1A365D', linewidth=2, label='Ledger Balance (INR)')
    ax.axhline(y=adlb, color='#f0ad4e', linestyle='--', label=f'Actual ADLB ({adlb:,.0f})')
    ax.axhline(y=5000, color='#d9534f', linestyle=':', label='Floor Limit (5,000)')
    
    ax.set_title('30-Day Working Capital Volatility Curve', fontsize=11, fontweight='bold', color='#1A365D')
    ax.set_xlabel('Billing Cycle Day')
    ax.set_ylabel('Ledger Value (INR)')
    ax.legend(loc='upper left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf

def generate_pdf_report(execution_mode, report_text, labels, latencies, throughputs):
    """Compiles complete metric structures and server-safe inline graphics into a PDF."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=45, leftMargin=45, topMargin=45, bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    PRIMARY_COLOR = colors.HexColor("#1A365D")   
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") 
    TEXT_COLOR = colors.HexColor("#2D3748")      
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold',
        fontSize=22, leading=26, textColor=PRIMARY_COLOR, spaceAfter=4, alignment=1 
    )
    meta_style = ParagraphStyle(
        'DocMeta', parent=styles['Normal'], fontName='Helvetica-Bold',
        fontSize=10, leading=14, textColor=SECONDARY_COLOR, spaceAfter=15, alignment=1
    )
    section_style = ParagraphStyle(
        'DocSection', parent=styles['Heading2'], fontName='Helvetica-Bold',
        fontSize=13, leading=17, textColor=PRIMARY_COLOR, spaceBefore=12, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'DocBody', parent=styles['Normal'], fontName='Helvetica',
        fontSize=9.5, leading=14, textColor=TEXT_COLOR, spaceAfter=6
    )

    # PAGE 1: Corporate Due Diligence Telemetry Dashboard
    story.append(Paragraph("B2B Risk Intelligence Due Diligence Export", title_style))
    story.append(Paragraph(f"Data Generation Profile: Executed via [{execution_mode}] Pipeline", meta_style))
    story.append(Spacer(1, 10))
    
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
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 15))
    
    # Securely append Performance Graphic (Pure Math Engine)
    img_perf_buf = _render_mpl_perf_chart(latencies, throughputs)
    story.append(Paragraph("Visual Asset: Compute Performance Model", section_style))
    story.append(Image(img_perf_buf, width=480, height=220))
    
    story.append(PageBreak()) # Clean jump to page 2 layout

    # PAGE 2+: Capital Volatility Curves & Audit Reporting
    img_ledger_buf = _render_mpl_ledger_chart()
    story.append(Paragraph("Visual Asset: Intramonth Ledger Simulation", section_style))
    story.append(Image(img_ledger_buf, width=480, height=220))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Executive Credit Risk Evaluation Report", section_style))
    
    # Process text output layout safely
    cleaned_text = report_text.replace("###", "").replace("####", "").replace("**", "").replace("*", "-")
    for line in cleaned_text.split('\n'):
        if line.strip():
            story.append(Paragraph(line.strip(), body_style))
            
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
