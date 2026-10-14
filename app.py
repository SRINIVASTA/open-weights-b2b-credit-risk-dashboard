# app.py (Four-Model Benchmarking Workspace)
import streamlit as st
import pandas as pd
import concurrent.futures
from src.config import DEFAULT_PROMPT, MOCK_TEXT_RESPONSE
from src.engine_clients import call_groq_live, call_gemini_live
from src.visualizer import generate_performance_chart, generate_ledger_chart

# Executive Page Formatting
st.set_page_config(
    page_title="Open-Weights Risk Cockpit", 
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
    user_query = st.text_area("Enter your merchant transaction scenario description below:", value=DEFAULT_PROMPT, height=100)
    submit_btn = st.button("🚀 Process Automated Analysis", type="primary", use_container_width=True)

if submit_btn:
    latencies, throughputs, tokens_count = [], [], []
    final_text_report = ""
    
    if execution_mode == "Live Production APIs":
        # Pulling directly from Streamlit secrets infrastructure safely
        try:
            groq_api_key = st.secrets["api_credentials"]["GROQ_API_KEY"]
            google_api_key = st.secrets["api_credentials"]["GEMINI_API_KEY"]
        except KeyError:
            st.error("❌ Configuration Error: Missing `[api_credentials]` variables inside your Streamlit Secrets vault setup.")
            st.stop()
            
        st.info("🔄 Querying 4 cloud engine streams concurrently via background threads...")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Running all four open-weights models in parallel
            future_qwen = executor.submit(call_groq_live, groq_api_key, "qwen3.8-27b", user_query)
            future_gpt = executor.submit(call_groq_live, groq_api_key, "gpt-oss-20b", user_query)
            future_gemma_31b = executor.submit(call_gemini_live, google_api_key, "gemma-4-31b-it", user_query)
            future_gemma_26b = executor.submit(call_gemini_live, google_api_key, "gemma-4-26b-a4b-it", user_query)
            
            res_qwen = future_qwen.result()
            res_gpt = future_gpt.result()
            res_gemma_31b = future_gemma_31b.result()
            res_gemma_26b = future_gemma_26b.result()

        if "error" in [res_qwen["status"], res_gpt["status"], res_gemma_31b["status"], res_gemma_26b["status"]]:
            st.error(f"❌ API Rejection Flagged.\n\n"
                     f"**Qwen Status:** {res_qwen.get('error_msg', 'Success')}\n\n"
                     f"**GPT-OSS Status:** {res_gpt.get('error_msg', 'Success')}\n\n"
                     f"**Gemma-4 31B Status:** {res_gemma_31b.get('error_msg', 'Success')}\n\n"
                     f"**Gemma-4 26B Status:** {res_gemma_26b.get('error_msg', 'Success')}")
            st.stop()
            
        latencies = [res_qwen['latency'], res_gpt['latency'], res_gemma_31b['latency'], res_gemma_26b['latency']]
        throughputs = [res_qwen['tps'], res_gpt['tps'], res_gemma_31b['tps'], res_gemma_26b['tps']]
        tokens_count = [f"{res_qwen['tokens']:,}", f"{res_gpt['tokens']:,}", f"{res_gemma_31b['tokens']:,}", f"{res_gemma_26b['tokens']:,}"]
        final_text_report = res_gpt['response']
        st.success(f"⚡ Live execution complete. Optimal latency registered in {res_gpt['latency']:.3f}s.")
        
    else:
        # Load Baseline Static Mock Performance Metric Snaps (Updated for 4 metrics)
        latencies = [2.926, 2.685, 87.412, 85.194]
        throughputs = [395.4, 413.0, 8.9, 9.3]
        tokens_count = ["1,157", "1,109", "782", "796"]
        final_text_report = MOCK_TEXT_RESPONSE
        st.success("✅ Mock environment generated instantly from baseline infrastructure logs.")

    # --- DISPLAY BLOCK 1: HARDWARE SYSTEM BENCHMARK COCKPIT ---
    st.markdown("### 📊 Section 1: LLM Engine Performance & Comparison Grid")
    
    # Dynamically generated metrics mapping explicitly to correct array locations
    df_metrics = pd.DataFrame({
        "Metric / Feature": ["Target Architecture", "Engine Infrastructure", "Inference Latency", "Generation Throughput", "Generated Tokens", "Compliance Matrix"],
        "Variant 1: Qwen": ["qwen3.8-27b", "Groq Cloud", f"{latencies[0]:.3f}s", f"{throughputs[0]:.1f} TPS", tokens_count[0], "100% Isolated"],
        "Variant 2: GPT-OSS (Fastest)": ["gpt-oss-20b", "Groq Cloud", f"{latencies[1]:.3f}s", f"{throughputs[1]:.1f} TPS", tokens_count[1], "100% Isolated"],
        "Variant 3: Gemma 4 (31B)": ["gemma-4-31b-it", "Google AI Studio", f"{latencies[2]:.3f}s", f"{throughputs[2]:.1f} TPS", tokens_count[2], "100% Isolated"],
        "Variant 4: Gemma 4 (26B)": ["gemma-4-26b-a4b-it", "Google AI Studio", f"{latencies[3]:.3f}s", f"{throughputs[3]:.1f} TPS", tokens_count[3], "100% Isolated"]
    })
    st.table(df_metrics)
    st.plotly_chart(generate_performance_chart(latencies, throughputs), use_container_width=True)

    # --- DISPLAY BLOCK 2: DYNAMIC COMPLIANCE MATRIX AND RISK OUTCOME REPORT ---
    st.markdown("---")
    st.markdown("### 📋 Section 2: Credit Evaluation Report & Cash Flow Risk Model")
    
    col_out1, col_out2 = st.columns(2, gap="large")
    with col_out1:
        st.markdown("#### 🔍 Structural Risk Matrix & Model Text Output")
        st.markdown(f"""
        <div style="background-color: #ffffff; padding: 25px; border: 1px solid #e2e8f0; border-radius: 8px; color: #1a202c; font-size:14px; line-height:1.6;">
            {final_text_report}
        </div>
        """, unsafe_allow_html=True)
        
    with col_out2:
        st.markdown("#### 📉 Intramonth Ledger Simulation (Plotly Visualization)")
        st.plotly_chart(generate_ledger_chart(), use_container_width=True)
