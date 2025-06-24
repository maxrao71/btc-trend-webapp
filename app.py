
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

st.set_page_config(page_title="BTC 趨勢進出場圖", layout="wide")
st.title("📉 BTC 趨勢進出場圖（CoinCap API 版）")

# 取得 CoinCap 歷史資料
url = "https://api.coincap.io/v2/assets/bitcoin/history?interval=h1"
try:
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()["data"]

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["time"], unit="ms")
    df["price"] = df["priceUsd"].astype(float)

    # 模擬策略：20 小時移動平均線
    df["sma_20"] = df["price"].rolling(20).mean()

    # 判斷進出場點（穿越均線）
    df["signal"] = 0
    df.loc[(df["price"] > df["sma_20"]) & (df["price"].shift(1) <= df["sma_20"].shift(1)), "signal"] = 1
    df.loc[(df["price"] < df["sma_20"]) & (df["price"].shift(1) >= df["sma_20"].shift(1)), "signal"] = -1

    # 畫圖
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["date"], y=df["price"], name="BTC 價格", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df["date"], y=df["sma_20"], name="20MA", line=dict(color="orange", dash="dash")))

    # 進出場點標記
    entries = df[df["signal"] == 1]
    exits = df[df["signal"] == -1]
    fig.add_trace(go.Scatter(x=entries["date"], y=entries["price"], mode="markers", name="進場", marker=dict(color="green", size=10, symbol="triangle-up")))
    fig.add_trace(go.Scatter(x=exits["date"], y=exits["price"], mode="markers", name="出場", marker=dict(color="red", size=10, symbol="triangle-down")))

    fig.update_layout(title="BTC 價格與進出場策略", xaxis_title="時間", yaxis_title="價格 (USD)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"資料讀取失敗：{e}")
    st.warning("⚠️ 無法取得資料，請稍後再試。")
