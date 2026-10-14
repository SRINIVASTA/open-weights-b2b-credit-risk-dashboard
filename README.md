# ⚡ Open-Weights B2B Credit Risk Intelligence Workspace

An enterprise-grade B2B risk intelligence workspace built with **Streamlit**, **Plotly**, and **ReportLab**. The application evaluates merchant credit worthiness under a high-vigilance compliance framework using live multi-engine LLM background processing (via concurrent processing pools) or rapid local baseline infrastructure logging mocks.

---

## 📊 Core Workspace Features
* **Multi-Engine Pipeline Streams:** Executes corporate lending due diligence using parallel runtime threads querying `Qwen`, `GPT-OSS`, and `Gemma` topologies.
* **Dual-Axis Performance Grid:** Live tracking of structural inference computational profiles comparing Generation Throughput (TPS) against Inference Latency (Seconds).
* **Working Capital Risk Modeling:** Interactive 30-day corporate distributor ledger curve plotting available ledger balances against compliance safety parameters.
* **Headless Vector PDF Exporter:** Compiles executive board credit analysis reports containing complete performance metrics grids and native, headless graphic charts dynamically exported via cloud-safe backends.

---

## 🛠️ Rapid Installation & Deploy Setup

### 1. Provision Virtual Environment
Clone your GitHub repository branch to your workspace and provision the local runtime container:
```bash
# Clone the repository
git clone https://github.com
cd open-weights-b2b-credit-risk-dashboard

# Create and execute virtual space isolation
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Configure App Dependencies
Install requirements directly via `pip`. Ensure your local `requirements.txt` maps the strict backend packages:
```bash
pip install -r requirements.txt
```

Verify your `requirements.txt` contains:
```text
streamlit
pandas
plotly
reportlab
matplotlib
groq
google-genai
```

### 3. Setup Secret Infrastructure Vault
To run the live pipeline modes, build your application credentials vault inside your dashboard runtime directory. Create a `.streamlit/secrets.toml` file:
```toml
# .streamlit/secrets.toml
[api_credentials]
GROQ_API_KEY = "your-groq-cloud-production-key"
GEMINI_API_KEY = "your-google-ai-studio-production-key"
```

---

## 🚀 Execution & Deployment Instructions

To spin up the web interface workspace locally, execute:
```bash
streamlit run app.py
```

### 🌐 Deploying to Streamlit Cloud
1. Push your finalized script blocks cleanly to your upstream GitHub repository branch (`main`).
2. Log into the **Streamlit Community Cloud Console** and connect your target repository.
3. In the advanced settings drawer, open the **Secrets** text console field and paste your production keys array exactly as formatted in your local `secrets.toml`.
4. Click **Deploy**. The container layer builds automatically from your `requirements.txt` specification.

---

## 🛡️ Credit Compliance Framework Settings
* **Framework Mode:** Highly Conservative Credit Compliance Profile (DPDP Act 2026 Guardrails enabled).
* **Minimum Cash Reserve Covenants:** Retained cash ledger thresholds calculated at `≥ 15% of monthly operating expenses`.
* **Debt Service Target:** Targets a strict structural target threshold of `DSCR ≥ 1.5x`.
