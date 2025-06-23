
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="BTC 趨勢圖")
st.title("📉 BTC 趨勢圖（黑底風格＋趨勢線＋進出場點）")

# 取得 Binance K 線資料
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
try:
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)

    # 畫圖
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="K線"
    ))

    # 加入簡單趨勢線
    x = range(len(df))
    y = df["close"].values
    coef = pd.Series(y).rolling(window=20).mean()
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=coef,
        mode="lines",
        name="趨勢線",
        line=dict(color="cyan", width=2)
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(t=50, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ 無法載入資料：{e}")
