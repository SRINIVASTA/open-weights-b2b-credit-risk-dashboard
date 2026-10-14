# In src/visualizer.py - Update this single function to process 4 items:
def generate_performance_chart(latencies, throughputs):
    """Creates a dual-axis interactive Plotly chart for 4-engine infrastructure analytics."""
    # Modified labels list to contain 4 distinct architecture definitions
    models_labels = ['qwen3.8-27b', 'gpt-oss-20b', 'gemma-4-31b-it', 'gemma-4-26b-a4b-it']
    
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
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
            text=[f"{l:.2f}s" for l in latencies],
            textposition="top center"
        ), 
        secondary_y=True
    )
    
    fig.update_layout(
        title_text="<b>Infrastructure Performance: Compute Throughput vs Token Latency</b>",
        hovermode="x unified",
        legend=dict(x=0.01, y=0.99),
        height=380
    )
    fig.update_yaxes(title_text="<b>Throughput Rate</b> (Tokens / Second)", secondary_y=False)
    fig.update_yaxes(title_text="<b>Inference Latency</b> (Seconds)", type="log", secondary_y=True)
    return fig
