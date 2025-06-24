
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import numpy as np

st.set_page_config(layout="wide", page_title="BTC 趨勢預測雙視圖")

@st.cache_data(ttl=300)
def fetch_data():
    url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=3600&limit=100"
    response = requests.get(url)
    data = response.json()["data"]["ohlc"]
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s") + pd.Timedelta(hours=8)
    df["close"] = df["close"].astype(float)
    return df

df = fetch_data()

# 策略判斷：簡單移動平均與 RSI
def calculate_signals(df):
    df["SMA20"] = df["close"].rolling(window=20).mean()
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    df["signal"] = np.where((df["close"] > df["SMA20"]) & (df["RSI"] < 70), "buy",
                     np.where((df["close"] < df["SMA20"]) & (df["RSI"] > 30), "sell", "hold"))
    return df

df = calculate_signals(df)

# 主圖：價格 + 進出場點
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=df["timestamp"], y=df["close"], mode="lines", name="價格"))
fig_price.add_trace(go.Scatter(
    x=df[df["signal"]=="buy"]["timestamp"],
    y=df[df["signal"]=="buy"]["close"],
    mode="markers",
    marker=dict(color="green", size=10, symbol="triangle-up"),
    name="進場點"
))
fig_price.add_trace(go.Scatter(
    x=df[df["signal"]=="sell"]["timestamp"],
    y=df[df["signal"]=="sell"]["close"],
    mode="markers",
    marker=dict(color="red", size=10, symbol="triangle-down"),
    name="出場點"
))
fig_price.update_layout(title="BTC 價格趨勢（台灣時間）")

# 副圖：RSI
fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=df["timestamp"], y=df["RSI"], mode="lines", name="RSI"))
fig_rsi.add_hline(y=70, line_dash="dot", line_color="red")
fig_rsi.add_hline(y=30, line_dash="dot", line_color="green")
fig_rsi.update_layout(title="RSI 指標（台灣時間）", yaxis=dict(range=[0, 100]))

# 雙視圖展示
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_price, use_container_width=True)
with col2:
    st.plotly_chart(fig_rsi, use_container_width=True)
