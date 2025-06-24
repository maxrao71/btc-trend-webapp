
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 BTC 即時趨勢圖 (Binance API)")

# 1. 讀取 Binance API
try:
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 100
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    raw_data = res.json()

    # 2. 整理為 DataFrame
    df = pd.DataFrame(raw_data, columns=[
        "Open Time", "Open", "High", "Low", "Close", "Volume",
        "Close Time", "Quote Asset Volume", "Number of Trades",
        "Taker Buy Base Volume", "Taker Buy Quote Volume", "Ignore"
    ])
    df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
    df["Close"] = df["Close"].astype(float)

    # 3. 畫出互動式圖表
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Open Time"],
        y=df["Close"],
        mode="lines+markers",
        name="BTC 收盤價",
        hovertemplate="時間：%{x}<br>收盤價：%{y:$,.2f}"
    ))
    fig.update_layout(title="BTC 收盤價走勢", xaxis_title="時間", yaxis_title="價格 (USD)", template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ 資料讀取失敗：{e}")
