# src/visualizer.py (Add or update this function)
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_performance_chart(latencies, throughputs):
    """Creates a dual-axis chart handling both live performance metrics and offline flags cleanly."""
    models_labels = ['qwen3.8-27b', 'gpt-oss-20b', 'gemma-4-31b-it', 'gemma-4-26b-a4b-it']
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Throughput Bars
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
    
    # Latency Line
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
        height=380
    )
    fig.update_yaxes(title_text="Throughput Rate (Tokens/Sec)", secondary_y=False)
    
    # Avoid applying log scale mathematically if values are 0.0 due to downtime
    has_valid_latency = any(l > 0 for l in latencies)
    fig.update_yaxes(title_text="Latency (Seconds)", type="log" if has_valid_latency else "linear", secondary_y=True)
    return fig
