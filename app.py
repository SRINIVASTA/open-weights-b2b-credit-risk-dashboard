# app.py (Part 1 of 2: Infrastructure Configuration & Data Viz Engines)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import time
import concurrent.futures
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# ==========================================
# 1. PAGE AND ARCHITECTURE CONFIGURATIONS
# ==========================================
st.set_page_config(
    page_title="Open-Weights B2B Risk Intelligence Dashboard", 
    page_icon="🛡️", 
    layout="wide"
)

DEFAULT_PROMPT = (
    "We have a small electronics distributor requesting a ₹3,50,000 inventory expansion loan. "
    "Their digital transaction log shows consistent monthly sales spikes during holiday weeks, "
    "but their average daily ledger balance routinely falls below ₹5,000 due to recurring upfront "
    "hardware supplier invoices. Conduct an immediate B2B risk analysis under a highly conservative "
    "credit compliance framework."
)

MOCK_TEXT_RESPONSE = """
### B2B RISK ANALYSIS & CREDIT BOARD VERDICT: CONDITIONAL APPROVAL

Under a high-vigilance credit compliance framework, the application for a ₹3,50,000 inventory expansion loan is granted subject to strict structural covenants. 

#### Core Risk Identifiers:
1. Severe Cash Runway Strain (🔴 HIGH RISK): The average daily balance routinely falls below the ₹5,000 baseline. This indicates immediate cash-crunch exposure if any payment clearance delays happen.
2. Upfront Hardware Supplier Invoices (🟡 MEDIUM RISK): The distributor drains working capital before extracting downstream value.
3. Holiday Sales Volume Spikes (🟢 LOW RISK): Transaction logs reflect verifiable, predictable seasonal revenue waves that clear the structural debt capacity safely.

#### Programmatic Mitigations & Covenants:
* Direct Vendor Disbursal: Loan proceeds must bypass the merchant ledger and transfer directly to verified original equipment hardware manufacturers.
* Automated PoS Lockbox Sweep: Establish a programmatic 15% sweep on card/UPI terminal clearing cycles directly during holiday weeks into an isolated repayment escrow system.
* DPDP Act 2026 Guardrails: Ledger scanning pipelines utilize zero-retention runtime memory blocks to guarantee absolute isolation of consumer data.
"""

# ==========================================
# 2. DATA VISUALIZATION CONTROLLERS
# ==========================================
def generate_performance_chart(latencies, throughputs):
    """Creates a dual-axis interactive Plotly chart for 4-engine infrastructure analytics."""
    models_labels = ['qwen/qwen3.8-27b', 'openai/gpt-oss-20b', 'gemma-4-31b-it', 'gemma-4-26b-a4b-it']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=models_labels, 
            y=throughputs, 
            name="Throughput (TPS)", 
            marker_color=['#1f77b4', '#2ca02c', '#9467bd', '#d62728'],
            opacity=0.85
        ), 
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=models_labels, 
            y=latencies, 
            name="Latency (Seconds)", 
            mode="lines+markers+text", 
            marker=dict(size=12, color='orange'),
            text=[f"{l:.2f}s" if l > 0 else "Offline" for l in latencies],
            textposition="top center"
        ), 
        secondary_y=True
    )
    
    fig.update_layout(
        title_text="<b>Compute Performance Profile: Throughput vs Latency Delivery</b>",
        hovermode="x unified",
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=40, r=40, t=50, b=40),
        height=380
    )
    fig.update_yaxes(title_text="Throughput Rate (Tokens/Sec)", secondary_y=False)
    
    has_valid_latency = any(l > 0 for l in latencies)
    fig.update_yaxes(title_text="Latency (Seconds)", type="log" if has_valid_latency else "linear", secondary_y=True)
    return fig

def generate_ledger_chart():
    """Simulates a 30-day corporate merchant ledger cash pipeline."""
    days = [f"Day {i:02d}" for i in range(1, 31)]
    simulated_cash = [12000, 9500, 8000, 6200, 3500, 3800, 4100, 4200, 4000, 4500, 4300, 4800, 4600, 4900, 4700, 4800, 4600, 4900, 4800, 15000, 85000, 190000, 310000, 385000, 340000, 210000, 95000, 45000, 22000, 14000]
    critical_baseline = [5000] * 30
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=simulated_cash, name="Available Ledger Balance (INR)", mode="lines+markers", line=dict(color="#1f77b4", width=3)))
    fig.add_trace(go.Scatter(x=days, y=critical_baseline, name="Compliance Safety Limit (₹5,000)", mode="lines", line=dict(color="red", width=2, dash="dash")))
    
    fig.update_layout(
        title="<b>30-Day Distributor Working Capital Volatility Curve</b>",
        xaxis_title="Billing Cycle Day", 
        yaxis_title="Ledger Balance Value (₹)", 
        margin=dict(l=30, r=30, t=80, b=40),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.12, xanchor="right", x=1)
    )
    fig.add_annotation(
        x="Day 05", y=3500, text="Supplier Invoice Crash", 
        showarrow=True, arrowhead=2, arrowcolor="red", font=dict(color="red"), bgcolor="white"
    )
    return fig

def generate_pdf_report(execution_mode, text_report, models, latencies, throughputs, fig_perf, fig_ledger):
    """Generates a clean PDF file binary stream containing fully embedded static chart exports."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, title="B2B Risk Intelligence Export")
    styles = getSampleStyleSheet()
    story = []
    
    # Title Header
    story.append(Paragraph("<b>B2B Risk Intelligence Due Diligence Export</b>", styles['Title']))
    story.append(Spacer(1, 15))
    
    # Mode Context Indicator
    mode_style = ParagraphStyle('ModeStyle', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.HexColor('#1f77b4'))
    story.append(Paragraph(f"Data Generation Profile: Executed via [{execution_mode}] Pipeline", mode_style))
    story.append(Spacer(1, 15))
    
    # Metric Grid Data Table
    story.append(Paragraph("<b>Compute Performance Grid Metrics</b>", styles['Heading2']))
    table_data = [["Model Target Cluster", "Inference Latency", "Throughput Rate"]]
    for idx, model in enumerate(models):
        lat_text = f"{latencies[idx]:.3f}s" if latencies[idx] > 0 else "Offline"
        tps_text = f"{throughputs[idx]:.1f} TPS" if throughputs[idx] > 0 else "0.0 TPS"
        table_data.append([model, lat_text, tps_text])
        
    t = Table(table_data, colWidths=[250, 120, 120])
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
    
    # Render and embed Plotly Performance Chart into the PDF pipeline stream
    try:
        img_bytes_perf = pio.to_image(fig_perf, format='png', width=540, height=280)
        story.append(Paragraph("<b>Visual Asset: Compute Performance Model</b>", styles['Heading3']))
        story.append(Image(io.BytesIO(img_bytes_perf), width=480, height=250))
        story.append(Spacer(1, 15))
    except Exception as e:
        story.append(Paragraph(f"<i>Performance Graph Rendering Skipped: {str(e)}</i>", styles['Italic']))
        
    # Render and embed Plotly Ledger Volatility Chart into the PDF pipeline stream
    try:
        img_bytes_ledger = pio.to_image(fig_ledger, format='png', width=540, height=280)
        story.append(Paragraph("<b>Visual Asset: Intramonth Ledger Simulation</b>", styles['Heading3']))
        story.append(Image(io.BytesIO(img_bytes_ledger), width=480, height=250))
        story.append(Spacer(1, 25))
    except Exception as e:
        story.append(Paragraph(f"<i>Ledger Graph Rendering Skipped: {str(e)}</i>", styles['Italic']))
        
    # Executive Verdict Analysis Text Paragraphs
    story.append(Paragraph("<b>Executive Credit Risk Evaluation Report</b>", styles['Heading2']))
    clean_lines = text_report.strip().split('\n')
    for line in clean_lines:
        if line.strip():
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1, 6))
            
    # Legal / General Info Disclaimer Footnote
    story.append(Spacer(1, 25))
    footnote_style = ParagraphStyle('Footnote', parent=styles['Italic'], fontSize=8, textColor=colors.gray)
    story.append(Paragraph("This is for informational purposes only. For medical advice or diagnosis, consult a professional. AI responses may include mistakes.", footnote_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
# app.py (Part 2 of 2: API Request Clients & Interface Layout)

# ==========================================
# 3. LIVE BACKGROUND WORKER CLIENTS
# ==========================================
def call_groq_live(api_key, model_name, user_prompt):
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        start_time = time.perf_counter()
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": f"Provide an immediate B2B risk analysis under a highly conservative credit framework:\n{user_prompt}"}],
            temperature=0.1
        )
        latency = time.perf_counter() - start_time
        tokens = completion.usage.completion_tokens
        response_text = completion.choices.message.content
        return {"status": "success", "latency": latency, "tps": tokens / latency, "tokens": tokens, "response": response_text}
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}

def call_gemini_live(api_key, model_name, user_prompt):
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        start_time = time.perf_counter()
        response = client.models.generate_content(
            model=model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(temperature=0.1)
        )
        latency = time.perf_counter() - start_time
        try:
            tokens = response.usage_metadata.candidates_token_count
        except:
            tokens = len(response.text.split()) * 1.3
        return {"status": "success", "latency": latency, "tps": tokens / latency, "tokens": int(tokens), "response": response.text}
    except Exception as e:
        return {"status": "error", "error_msg": str(e)}

# ==========================================
# 4. MAIN USER INTERFACE ORCHESTRATION
# ==========================================
st.title("⚡ Open-Weights B2B Credit Risk Intelligence Workspace")

st.sidebar.title("🛡️ Core System Controls")
st.sidebar.markdown("---")
execution_mode = st.sidebar.radio("Data Source Mode Selector", ["Mock Simulation Data", "Live Production APIs"])
st.sidebar.markdown("---")

st.markdown(f"Execute corporate lending due diligence using **{execution_mode.lower()}** infrastructure pipelines.")

with st.container(border=True):
    st.subheader("📥 Live Chat Prompt Input")
    user_query = st.text_area("Enter scenario description below:", value=DEFAULT_PROMPT, height=100)
    submit_btn = st.button("🚀 Process Automated Analysis", type="primary", use_container_width=True)

if submit_btn:
    models_labels = ['qwen/qwen3.8-27b', 'openai/gpt-oss-20b', 'gemma-4-31b-it', 'gemma-4-26b-a4b-it']
    latencies = [0.0, 0.0, 0.0, 0.0]
    throughputs = [0.0, 0.0, 0.0, 0.0]
    tokens_count = ["Offline", "Offline", "Offline", "Offline"]
    compliance_status = ["Isolated", "Isolated", "Isolated", "Isolated"]
    final_text_report = ""
    
    if execution_mode == "Live Production APIs":
        try:
            groq_api_key = st.secrets["api_credentials"]["GROQ_API_KEY"]
            google_api_key = st.secrets["api_credentials"]["GEMINI_API_KEY"]
        except KeyError:
            st.error("❌ Configuration Error: Missing settings parameters inside your Streamlit secrets vault.")
            st.stop()
            
        st.info("🔄 Querying 4 cloud engine streams concurrently via background threads...")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_qwen = executor.submit(call_groq_live, groq_api_key, models_labels[0], user_query)
            future_gpt = executor.submit(call_groq_live, groq_api_key, models_labels[1], user_query)
            future_gemma_31b = executor.submit(call_gemini_live, google_api_key, models_labels[2], user_query)
            future_gemma_26b = executor.submit(call_gemini_live, google_api_key, models_labels[3], user_query)
            
            res_qwen = future_qwen.result()
            res_gpt = future_gpt.result()
            res_gemma_31b = future_gemma_31b.result()
            res_gemma_26b = future_gemma_26b.result()

        responses = [res_qwen, res_gpt, res_gemma_31b, res_gemma_26b]
        for idx, res in enumerate(responses):
            if res["status"] == "success":
                latencies[idx] = res['latency']
                throughputs[idx] = res['tps']
                tokens_count[idx] = f"{res['tokens']:,}"
                if not final_text_report:
                    final_text_report = res['response']
            else:
                latencies[idx] = 0.0
                throughputs[idx] = 0.0
                tokens_count[idx] = "⚠️ Server Error"
                compliance_status[idx] = "Failed Connection"
        
        if not final_text_report:
            st.error("❌ Critical Infrastructure Failure: All targeted model clusters are currently offline.")
            st.stop()
        else:
            st.success("⚡ Live processing complete. Data generated using available cloud clusters.")
        
    else:
        latencies = [2.926, 2.685, 87.412, 85.194]
        throughputs = [395.4, 413.0, 8.9, 9.3]
        tokens_count = ["1,157", "1,109", "782", "796"]
        final_text_report = MOCK_TEXT_RESPONSE
        st.success("✅ Mock environment generated instantly from baseline infrastructure logs.")

    # Generate Figures for View and PDF Export Pipelines
    fig_perf = generate_performance_chart(latencies, throughputs)
    fig_ledger = generate_ledger_chart()

    # Action Button Controller for PDF Export Payload Data Download
    pdf_bytes = generate_pdf_report(execution_mode, final_text_report, models_labels, latencies, throughputs, fig_perf, fig_ledger)
    st.download_button(
        label="📥 Download Executive Compliance Report (PDF)",
        data=pdf_bytes,
        file_name="B2B_Risk_Intelligence_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    # --- SECTION 1: SYSTEM ENGINE BENCHMARK TABLE ---
    st.markdown("### 📊 Section 1: LLM Engine Performance & Comparison Grid")
    
    df_metrics = pd.DataFrame({
        "Metric / Feature": ["Target Architecture", "Engine Infrastructure", "Inference Latency", "Generation Throughput", "Generated Tokens", "Compliance Matrix"],
        "Variant 1: Qwen": [models_labels[0], "Groq Cloud", f"{latencies[0]:.3f}s" if latencies[0] > 0 else "Offline", f"{throughputs[0]:.1f} TPS", tokens_count[0], compliance_status[0]],
        "Variant 2: GPT-OSS": [models_labels[1], "Groq Cloud", f"{latencies[1]:.3f}s" if latencies[1] > 0 else "Offline", f"{throughputs[1]:.1f} TPS", tokens_count[1], compliance_status[1]],
        "Variant 3: Gemma 4 (31B)": [models_labels[2], "Google AI Studio", f"{latencies[2]:.3f}s" if latencies[2] > 0 else "Offline", f"{throughputs[2]:.1f} TPS", tokens_count[2], compliance_status[2]],
        "Variant 4: Gemma 4 (26B)": [models_labels[3], "Google AI Studio", f"{latencies[3]:.3f}s" if latencies[3] > 0 else "Offline", f"{throughputs[3]:.1f} TPS", tokens_count[3], compliance_status[3]]
    })
    st.table(df_metrics)
    st.plotly_chart(fig_perf, use_container_width=True)

    # --- SECTION 2: CREDIT EVALUATION MATRIX & REPORT ---
    st.markdown("---")
    st.markdown("### 📋 Section 2: Credit Evaluation Report & Cash Flow Risk Model")
    
    col_out1, col_out2 = st.columns(2, gap="large")
    with col_out1:
        st.markdown("#### 🔍 Credit Risk Matrix & Executive Text Output")
        with st.container(border=True):
            st.markdown(final_text_report)
        
    with col_out2:
        st.markdown("#### 📉 Intramonth Ledger Simulation (Plotly Visualization)")
        st.plotly_chart(fig_ledger, use_container_width=True)
