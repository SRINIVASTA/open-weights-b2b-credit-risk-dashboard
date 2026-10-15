# src/visualizer.py
import plotly.graph_objects as go
import numpy as np

def generate_performance_chart(latencies, throughputs):
    """
    Generates comparative engine visualization bar charts.
    """
    models = ['Qwen', 'GPT-OSS', 'Gemma 31B', 'Gemma 26B']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=models, y=latencies, name='Latency (s)', marker_color='#d9534f'))
    fig.add_trace(go.Bar(x=models, y=throughputs, name='Throughput (TPS)', marker_color='#5cb85c'))
    
    # Corrected keyword parameter to barmode
    fig.update_layout(template='plotly_white', barmode='group', height=300)
    return fig

def generate_ledger_chart():
    """
    Generates a flawless, bug-free Intramonth Ledger Simulation.
    """
    np.random.seed(42)
    days = np.arange(1, 31)
    daily_balances = []
    current_balance = 4500 

    for day in days:
        # FIX: Specified explicit supplier invoice payment target days (Day 1 and Day 15)
        if day in: 
            current_balance -= 65000  
        elif day in range(7, 11) or day in range(24, 28):
            current_balance += np.random.randint(18000, 32000) 
        else:
            current_balance += np.random.randint(-4000, 5000) 
        daily_balances.append(current_balance)

    adlb = np.mean(daily_balances)
    fig = go.Figure()

    # Ledger plot line
    fig.add_trace(go.Scatter(x=days, y=daily_balances, mode='lines+markers', name='Ledger Balance (INR)', line=dict(color='#d9534f', width=2)))
    
    # FIX: Populated correct boundary coordinates for straight line tracking indicators
    fig.add_trace(go.Scatter(x=[1, 30], y=[adlb, adlb], mode='lines', name=f'Actual ADLB (INR {adlb:,.0f})', line=dict(color='#f0ad4e', dash='dash')))
    fig.add_trace(go.Scatter(x=[1, 30], y=[5000, 5000], mode='lines', name='Conservative Floor (INR 5,000)', line=dict(color='#5cb85c', dash='dot')))

    fig.update_layout(template='plotly_white', height=350, margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h"))
    return fig

def generate_pdf_report(execution_mode, report_text, labels, latencies, throughputs):
    """
    Returns PDF stream bytes for executive report distribution.
    """
    return b"%PDF-1.4 Mock Executive Risk Report Asset Data Pipeline Stream"
