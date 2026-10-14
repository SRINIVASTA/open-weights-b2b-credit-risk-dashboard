# src/visualizer.py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_performance_chart(latencies, throughputs):
    """Creates a dual-axis interactive Plotly chart for inference analytics."""
    models_labels = ['qwen3.8-27b', 'gpt-oss-20b', 'gemma-4-26b-a4b-it']
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Throughput Bars
    fig.add_trace(
        go.Bar(
            x=models_labels, 
            y=throughputs, 
            name="Throughput (TPS)", 
            marker_color=['#1f77b4', '#2ca02c', '#d62728'],
            opacity=0.85
        ), 
        secondary_y=False
    )
    
    # Latency Scatter Line
    fig.add_trace(
        go.Scatter(
            x=models_labels, 
            y=latencies, 
            name="Latency (Seconds)", 
            mode="lines+markers+text", 
            marker=dict(size=12, color='orange'),
            text=[f"{l:.2f}s" for l in latencies],
            textposition="top center"
        ), 
        secondary_y=True
    )
    
    # Styling Customizations
    fig.update_layout(
        title_text="<b>Infrastructure Profiles: Throughput Rates vs. Token Latency</b>",
        hovermode="x unified",
        legend=dict(x=0.01, y=0.99),
        margin=dict(l=50, r=50, t=60, b=40),
        height=380
    )
    
    fig.update_yaxes(title_text="<b>Throughput Rate</b> (Tokens / Second)", secondary_y=False)
    # Switch to log scale automatically if severe outliers exist (like Gemma at 85s)
    use_log = any(l > 10 for l in latencies)
    fig.update_yaxes(title_text="<b>Inference Latency</b> (Seconds)", type="log" if use_log else "linear", secondary_y=True)
    return fig

def generate_ledger_chart():
    """Simulates a 30-day corporate merchant ledger cash pipeline."""
    days = [f"Day {i:02d}" for i in range(1, 31)]
    
    # Simulated balance crashing early from supplier bills and surging during holiday weeks
    simulated_cash = [
        12000, 11000, 9500, 7000, 3500, 3800, 4100, 4200, 4000, 4300, 
        4500, 4200, 4600, 4800, 4700, 4900, 5200, 6000, 15000, 85000, 
        240000, 385000, 310000, 190000, 120000, 75000, 45000, 25000, 18000, 14000
    ]
    critical_baseline = [5000] * 30
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=simulated_cash, name="Available Ledger Balance (INR)", mode="lines+markers", line=dict(color="#1f77b4", width=3)))
    fig.add_trace(go.Scatter(x=days, y=critical_baseline, name="Compliance Safety Limit (₹5,000)", mode="lines", line=dict(color="red", width=2, dash="dash")))
    
    fig.update_layout(
        title="<b>30-Day Distributor Working Capital Volatility Curve</b>",
        xaxis_title="Billing Cycle Day", 
        yaxis_title="Ledger Balance Value (₹)", 
        margin=dict(l=30, r=30, t=50, b=40),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.add_annotation(x="Day 05", y=3500, text="Supplier Invoice Crash", showarrow=True, arrowhead=2, color="red", bgcolor="white")
    return fig
