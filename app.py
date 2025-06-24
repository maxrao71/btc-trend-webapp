
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="BTC 趨勢預測雙視圖")

@st.cache_data(ttl=300)
def get_real_btc_data():
    url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/"
    params = {
        "step": "3600",
        "limit": "100"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()["data"]["ohlc"]
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df["close"] = df["close"].astype(float)
        return df[["timestamp", "close"]].rename(columns={"timestamp": "time", "close": "price"})
    except Exception as e:
        st.error(f"❌ 資料讀取失敗：{e}")
        return pd.DataFrame(columns=["time", "price"])

def calculate_indicators(df):
    df["SMA_10"] = df["price"].rolling(window=10).mean()
    df["RSI"] = compute_rsi(df["price"], 14)
    df["Signal"] = np.where((df["price"] > df["SMA_10"]) & (df["RSI"] < 70), "Buy",
                     np.where((df["price"] < df["SMA_10"]) & (df["RSI"] > 30), "Sell", "Hold"))
    return df

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df = get_real_btc_data()

if not df.empty:
    df = calculate_indicators(df)

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=df["time"], y=df["price"], mode="lines+markers", name="價格"))
    fig_price.add_trace(go.Scatter(x=df["time"], y=df["SMA_10"], mode="lines", name="SMA 10"))
    fig_price.update_layout(title="實際價格與移動平均", height=400)

    # 加入進出場點
    buy_signals = df[df["Signal"] == "Buy"]
    sell_signals = df[df["Signal"] == "Sell"]
    fig_price.add_trace(go.Scatter(x=buy_signals["time"], y=buy_signals["price"], mode="markers", name="進場", marker=dict(color="green", size=10)))
    fig_price.add_trace(go.Scatter(x=sell_signals["time"], y=sell_signals["price"], mode="markers", name="出場", marker=dict(color="red", size=10)))

    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df["time"], y=df["RSI"], mode="lines", name="RSI"))
    fig_rsi.update_layout(title="RSI 指標", height=400, yaxis_range=[0, 100])

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_price, use_container_width=True)
    with col2:
        st.plotly_chart(fig_rsi, use_container_width=True)
else:
    st.warning("暫時無法取得資料，請稍後再試。")
