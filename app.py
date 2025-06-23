
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import numpy as np

st.set_page_config(layout="wide")
st.title("BTC 趨勢圖（資料除錯版）")

@st.cache_data(ttl=300)
def fetch_btc_ohlcv():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        '_1', '_2', '_3', '_4', '_5', '_6'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)
    return df

df = fetch_btc_ohlcv()

# Show data for debugging
st.subheader("✅ 抓到的 BTC/USDT 每小時資料（前 10 筆）")
st.dataframe(df.head(10))

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

fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis_rangeslider_visible=False,
    title="BTC/USDT 每小時K線圖"
)

st.plotly_chart(fig, use_container_width=True)
