# app.py (Fault-Tolerant High-Availability Architecture)
import streamlit as st
import pandas as pd
import concurrent.futures
from src.config import DEFAULT_PROMPT, MOCK_TEXT_RESPONSE
from src.engine_clients import call_groq_live, call_gemini_live
from src.visualizer import generate_performance_chart, generate_ledger_chart

# Executive Page Formatting
st.set_page_config(
    page_title="Open-Weights B2B Risk Intelligence Dashboard", 
    page_icon="🛡️", 
    layout="wide"
)

st.title("⚡ Open-Weights B2B Credit Risk Intelligence Workspace")
st.markdown("Execute corporate lending due diligence using live multi-engine processing or mock test environments.")

# Sidebar Mode Configuration Controller
st.sidebar.title("🛡️ Core System Controls")
st.sidebar.markdown("---")
execution_mode = st.sidebar.radio("Data Source Mode Selector", ["Mock Simulation Data", "Live Production APIs"])
st.sidebar.markdown("---")
st.sidebar.info("💡 **Security Notice:** Live mode automatically hooks into tokens configured inside your Streamlit cloud management panel.")

# User prompt container block
with st.container(border=True):
    st.subheader("📥 Live Chat Prompt Input")
    user_query = st.text_area("Enter scenario description below:", value=DEFAULT_PROMPT, height=100)
    submit_btn = st.button("🚀 Process Automated Analysis", type="primary", use_container_width=True)

if submit_btn:
    # Diagnostic arrays initialize with fallback values
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
            st.error("❌ Configuration Error: Missing `[api_credentials]` parameters inside your Streamlit Secret setup.")
            st.stop()
            
        st.info("🔄 Querying 4 cloud engine streams concurrently via background threads...")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_qwen = executor.submit(call_groq_live, groq_api_key, "qwen/qwen3.8-27b", user_query)
            future_gpt = executor.submit(call_groq_live, groq_api_key, "openai/gpt-oss-20b", user_query)
            future_gemma_31b = executor.submit(call_gemini_live, google_api_key, "gemma-4-31b-it", user_query)
            future_gemma_26b = executor.submit(call_gemini_live, google_api_key, "gemma-4-26b-a4b-it", user_query)
            
            res_qwen = future_qwen.result()
            res_gpt = future_gpt.result()
            res_gemma_31b = future_gemma_31b.result()
            res_gemma_26b = future_gemma_26b.result()

        # --- REWRITE: Fault-Tolerant Metrics Extraction Block ---
        responses = [res_qwen, res_gpt, res_gemma_31b, res_gemma_26b]
        
        for idx, res in enumerate(responses):
            if res["status"] == "success":
                latencies[idx] = res['latency']
                throughputs[idx] = res['tps']
                tokens_count[idx] = f"{res['tokens']:,}"
                # Save the first successful response to act as our core credit text analysis
                if not final_text_report:
                    final_text_report = res['response']
            else:
                latencies[idx] = 0.0
                throughputs[idx] = 0.0
                tokens_count[idx] = "⚠️ 500 Server Error"
                compliance_status[idx] = "Failed Connection"
        
        # If all 4 models fail completely, then abort
        if not final_text_report:
            st.error("❌ Critical Infrastructure Failure: All targeted model clusters are currently offline.")
            st.stop()
        else:
            st.success("⚡ Live processing complete. Data generated using available cloud clusters.")
        
    else:
        # Load Baseline Static Mock Performance Metric Snaps
        latencies = [2.926, 2.685, 87.412, 85.194]
        throughputs = [395.4, 413.0, 8.9, 9.3]
        tokens_count = ["1,157", "1,109", "782", "796"]
        final_text_report = MOCK_TEXT_RESPONSE
        st.success("✅ Mock environment generated instantly from baseline infrastructure logs.")

    # --- DISPLAY BLOCK 1: HARDWARE SYSTEM BENCHMARK COCKPIT ---
    st.markdown("### 📊 Section 1: LLM Engine Performance & Comparison Grid")
    
    df_metrics = pd.DataFrame({
        "Metric / Feature": ["Target Architecture", "Engine Infrastructure", "Inference Latency", "Generation Throughput", "Generated Tokens", "Compliance Matrix"],
        "Variant 1: Qwen": [models_labels[0], "Groq Cloud", f"{latencies[0]:.3f}s" if latencies[0] > 0 else "0.0s", f"{throughputs[0]:.1f} TPS", tokens_count[0], compliance_status[0]],
        "Variant 2: GPT-OSS": [models_labels[1], "Groq Cloud", f"{latencies[1]:.3f}s" if latencies[1] > 0 else "0.0s", f"{throughputs[1]:.1f} TPS", tokens_count[1], compliance_status[1]],
        "Variant 3: Gemma 4 (31B)": [models_labels[2], "Google AI Studio", f"{latencies[2]:.3f}s" if latencies[2] > 0 else "0.0s", f"{throughputs[2]:.1f} TPS", tokens_count[2], compliance_status[2]],
        "Variant 4: Gemma 4 (26B)": [models_labels[3], "Google AI Studio", f"{latencies[3]:.3f}s" if latencies[3] > 0 else "0.0s", f"{throughputs[3]:.1f} TPS", tokens_count[3], compliance_status[3]]
    })
    st.table(df_metrics)
    
    # Render performance graphics safely passing arrays directly
    st.plotly_chart(generate_performance_chart(latencies, throughputs), use_container_width=True)

    # --- DISPLAY BLOCK 2: DYNAMIC COMPLIANCE MATRIX AND RISK OUTCOME REPORT ---
    st.markdown("---")
    st.markdown("### 📋 Section 2: Credit Evaluation Report & Cash Flow Risk Model")
    
    col_out1, col_out2 = st.columns(2, gap="large")
    with col_out1:
        st.markdown("#### 🔍 Credit Risk Matrix & Executive Text Output")
        st.markdown(f"""
        <div style="background-color: #ffffff; padding: 25px; border: 1px solid #e2e8f0; border-radius: 8px; color: #1a202c; font-size:14px; line-height:1.6; min-height: 400px;">
            {final_text_report}
        </div>
        """, unsafe_allow_html=True)
        
    with col_out2:
        st.markdown("#### 📉 Intramonth Ledger Simulation (Plotly Visualization)")
        st.plotly_chart(generate_ledger_chart(), use_container_width=True)
