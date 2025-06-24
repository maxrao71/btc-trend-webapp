
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def generate_mock_data():
    now = datetime.utcnow()
    times = [now - timedelta(minutes=60-i*5) for i in range(12)]
    prices = [100000 + random.uniform(-1000, 1000) for _ in times]
    signals = [random.choice(["buy", "sell", None]) for _ in times]
    return pd.DataFrame({"time": times, "price": prices, "signal": signals})

def show_strategy_view():
    st.title("📊 BTC 策略進出場圖表 - Plotly 互動圖")

    df = generate_mock_data()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['price'], mode='lines+markers', name='價格'))

    for i, row in df.iterrows():
        if row['signal'] == 'buy':
            fig.add_trace(go.Scatter(x=[row['time']], y=[row['price']], mode='markers',
                                     marker=dict(color='green', size=10),
                                     name='進場 Buy'))
        elif row['signal'] == 'sell':
            fig.add_trace(go.Scatter(x=[row['time']], y=[row['price']], mode='markers',
                                     marker=dict(color='red', size=10),
                                     name='出場 Sell'))

    fig.update_layout(title="策略預測圖", xaxis_title="時間", yaxis_title="價格")
    st.plotly_chart(fig, use_container_width=True)
