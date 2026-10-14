# src/visualizer.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
matplotlib.use('Agg')  # Headless mode protection for cloud servers
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

def generate_performance_chart(latencies, throughputs):
    models_labels = ['qwen/qwen3.8-27b', 'openai/gpt-oss-20b', 'gemma-4-31b-it', 'gemma-4-26b-a4b-it']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=models_labels, y=throughputs, name="Throughput (TPS)", 
            marker_color=['#1f77b4', '#2ca02c', '#9467bd', '#d62728'], opacity=0.85
        ), secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=models_labels, y=latencies, name="Latency (Seconds)", mode="lines+markers+text", 
            marker=dict(size=12, color='orange'),
            text=[f"{l:.2f}s" if l > 0 else "Offline" for l in latencies], textposition="top center"
        ), secondary_y=True
    )
    fig.update_layout(
        title_text="<b>Compute Performance Profile: Throughput vs Latency Delivery</b>",
        hovermode="x unified", legend=dict(x=0.01, y=0.99), margin=dict(l=40, r=40, t=50, b=40), height=380
    )
    fig.update_yaxes(title_text="Throughput Rate (Tokens/Sec)", secondary_y=False)
    has_valid_latency = any(l > 0 for l in latencies)
    fig.update_yaxes(title_text="Latency (Seconds)", type="log" if has_valid_latency else "linear", secondary_y=True)
    return fig

def generate_ledger_chart():
    days = [f"Day {i:02d}" for i in range(1, 31)]
    # Fixed: Restored the complete dataset array sequence here
    simulated_cash = [12000, 9500, 8000, 6200, 3500, 3800, 4100, 4200, 4000, 4500, 4300, 4800, 4600, 4900, 4700, 4800, 4600, 4900, 4800, 15000, 85000, 190000, 310000, 385000, 340000, 210000, 95000, 45000, 22000, 14000]
    critical_baseline = [5000] * 30
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=simulated_cash, name="Available Ledger Balance (INR)", mode="lines+markers", line=dict(color="#1f77b4", width=3)))
    fig.add_trace(go.Scatter(x=days, y=critical_baseline, name="Compliance Safety Limit (INR 5,000)", mode="lines", line=dict(color="red", width=2, dash="dash")))
    
    fig.update_layout(
        title="<b>30-Day Distributor Working Capital Volatility Curve</b>",
        xaxis_title="Billing Cycle Day", yaxis_title="Ledger Balance Value (INR)", 
        margin=dict(l=30, r=30, t=80, b=40), height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.12, xanchor="right", x=1)
    )
    fig.add_annotation(
        x="Day 05", y=3500, text="Supplier Invoice Crash", 
        showarrow=True, arrowhead=2, arrowcolor="red", font=dict(color="red"), bgcolor="white"
    )
    return fig

def generate_pdf_report(execution_mode, text_report, models, latencies, throughputs):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title="B2B Risk Intelligence Export")
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("<b>B2B Risk Intelligence Due Diligence Export</b>", styles['Title']))
    story.append(Spacer(1, 15))
    
    mode_style = ParagraphStyle('ModeStyle', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.HexColor('#1f77b4'))
    story.append(Paragraph(f"Data Generation Profile: Executed via [{execution_mode}] Pipeline", mode_style))
    story.append(Spacer(1, 15))
    
    table_data = [["Model Target Cluster", "Inference Latency", "Throughput Rate"]]
    for idx, model in enumerate(models):
        lat_text = f"{latencies[idx]:.3f}s" if latencies[idx] > 0 else "Offline"
        tps_text = f"{throughputs[idx]:.1f} TPS" if throughputs[idx] > 0 else "0.0 TPS"
        table_data.append([model, lat_text, tps_text])
        
    t = Table(table_data, colWidths=[200, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTSIZE', (0,0), (-1,-1), 10),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))
    
    try:
        plt.figure(figsize=(6, 3))
        plt.bar(models, throughputs, color=['#1f77b4', '#2ca02c', '#9467bd', '#d62728'], alpha=0.8)
        plt.title("Throughput Rate Profile (Tokens/Sec)", fontsize=10, fontweight='bold')
        plt.ylabel("Throughput (TPS)", fontsize=8)
        plt.xticks(fontsize=8, rotation=15)
        plt.tight_layout()
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', dpi=200)
        img_buf.seek(0)
        plt.close()
        story.append(Paragraph("<b>Visual Asset: Compute Performance Model</b>", styles['Heading3']))
        story.append(Image(img_buf, width=450, height=225))
        story.append(Spacer(1, 15))
    except:
         pass
        
    try:
        # Fixed: Restored the matching 30-day data timeline array inside report image generation
        simulated_cash = [12000, 9500, 8000, 6200, 3500, 3800, 4100, 4200, 4000, 4500, 4300, 4800, 4600, 4900, 4700, 4800, 4600, 4900, 4800, 15000, 85000, 190000, 310000, 385000, 340000, 210000, 95000, 45000, 22000, 14000]
        plt.figure(figsize=(6, 3))
        plt.plot(range(1, 31), simulated_cash, marker='o', color='#1f77b4', linewidth=2)
        plt.axhline(y=5000, color='r', linestyle='--', label="Compliance Limit")
        plt.title("30-Day Working Capital Volatility Curve", fontsize=10, fontweight='bold')
        plt.xlabel("Billing Cycle Day", fontsize=8)
        plt.ylabel("Ledger Value (INR)", fontsize=8)
        plt.tight_layout()
        img_buf2 = io.BytesIO()
        plt.savefig(img_buf2, format='png', dpi=200)
        img_buf2.seek(0)
        plt.close()
        story.append(Paragraph("<b>Visual Asset: Intramonth Ledger Simulation</b>", styles['Heading3']))
        story.append(Image(img_buf2, width=450, height=225))
        story.append(Spacer(1, 25))
    except:
         pass
        
    story.append(Paragraph("<b>Executive Credit Risk Evaluation Report</b>", styles['Heading2']))
    for line in text_report.strip().split('\n'):
        if line.strip():
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1, 6))
            
    story.append(Spacer(1, 25))
    footnote_style = ParagraphStyle('Footnote', parent=styles['Italic'], fontSize=8, textColor=colors.gray)
    story.append(Paragraph("This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes.", footnote_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
