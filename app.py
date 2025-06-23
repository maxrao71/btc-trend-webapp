
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import numpy as np

st.set_page_config(layout="wide")
st.title("BTC 趨勢圖（黑底風格＋趨勢線＋進出場點）")

@st.cache_data(ttl=300)
def fetch_proxy_data():
    url = "https://btc-mock-api.vercel.app/api/kline"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        '_1', '_2', '_3', '_4', '_5', '_6'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    return df

df = fetch_proxy_data()
fig = go.Figure()

# Candlestick chart
fig.add_trace(go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    increasing_line_color='lime',
    decreasing_line_color='red',
    name='K線'
))

# Trend line and signals
lookback = 20
if len(df) >= lookback:
    x = np.arange(lookback)
    y = df['close'][-lookback:].values
    if len(x) == len(y):
        coef = np.polyfit(x, y, 1)
        trend_line = np.poly1d(coef)(x)

        slope = coef[0]
        trend_desc = "上升趨勢 📈" if slope > 0 else "下降趨勢 📉"
        st.subheader(f"趨勢偵測結果：{trend_desc}（斜率：{slope:.2f}）")

        latest_price = df['close'].iloc[-1]
        latest_trend = trend_line[-1]
        signal_type = None
        if latest_price > latest_trend * 1.01:
            signal_type = 'buy'
        elif latest_price < latest_trend * 0.99:
            signal_type = 'sell'

        trend_x = df['timestamp'][-lookback:]
        fig.add_trace(go.Scatter(
            x=trend_x,
            y=trend_line,
            mode='lines',
            line=dict(color='yellow', width=3),
            name='趨勢線'
        ))

        if signal_type == 'buy':
            fig.add_trace(go.Scatter(
                x=[df['timestamp'].iloc[-1]],
                y=[latest_price],
                mode='markers',
                marker=dict(color='lime', size=12, symbol='circle'),
                name='進場點'
            ))
        elif signal_type == 'sell':
            fig.add_trace(go.Scatter(
                x=[df['timestamp'].iloc[-1]],
                y=[latest_price],
                mode='markers',
                marker=dict(color='red', size=12, symbol='circle'),
                name='出場點'
            ))

fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis_rangeslider_visible=False,
    title="BTC/USDT 每小時K線圖（含趨勢線與進出場提示）"
)

st.plotly_chart(fig, use_container_width=True)
