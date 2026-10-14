# app.py
import streamlit as st
import pandas as pd
import concurrent.futures
import sys
import os

# Appends the src directory to Python's system search runtime environment path 
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.config import DEFAULT_PROMPT, MOCK_TEXT_RESPONSE
from src.visualizer import generate_performance_chart, generate_ledger_chart, generate_pdf_report
from src.engine_clients import call_groq_live, call_gemini_live

# Custom CSS implementation: Restricts full width and gives a perfect 1-inch desktop layout border
st.markdown("""
    <style>
        .block-container {
            max-width: 1400px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 96px !important;  /* Exactly 1 inch padding from the sidebar */
            padding-right: 96px !important; /* Exactly 1 inch padding from the right monitor bezel */
        }
    </style>
""", unsafe_allow_html=True)

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

    fig_perf = generate_performance_chart(latencies, throughputs)
    fig_ledger = generate_ledger_chart()

    pdf_bytes = generate_pdf_report(execution_mode, final_text_report, models_labels, latencies, throughputs)
    st.download_button(
        label="📥 Download Executive Compliance Report (PDF)",
        data=pdf_bytes,
        file_name="B2B_Risk_Intelligence_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

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
