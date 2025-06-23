
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.title("BTC 趨勢圖：黑底＋進出場提示")

def fetch_data():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
    response = requests.get(url)
    data = response.json()
    return data

def preprocess(data):
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)
    return df

def plot_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["close"], mode="lines", name="Close"))

    # 擬合線性趨勢線
    x = np.arange(len(df))
    y = df["close"].values
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)
    fig.add_trace(go.Scatter(x=df["timestamp"], y=trend(x), name="Trend"))

    st.plotly_chart(fig)

try:
    raw = fetch_data()
    df = preprocess(raw)
    plot_chart(df)
except Exception as e:
    st.error(f"資料讀取失敗：{e}")
