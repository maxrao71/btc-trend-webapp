import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="BTC 趨勢圖", layout="centered")
st.title("📉 BTC 趨勢圖：黑底＋進出場提示")

def fetch_data():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 100
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("API 回傳資料格式異常")
        return data
    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
        return []

def process_data(raw_data):
    try:
        df = pd.DataFrame(raw_data, columns=[
            "timestamp", "open", "high", "low", "close",
            "volume", "close_time", "quote_asset_volume",
            "number_of_trades", "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df.dropna(subset=["close"], inplace=True)
        return df
    except Exception as e:
        st.error(f"資料格式異常或不足：{e}")
        return pd.DataFrame()

def plot_trend(df):
    try:
        if df.empty:
            st.warning("無法取得資料，請稍後再試。")
            return

        x = np.arange(len(df))
        y = df["close"].values
        z = np.polyfit(x, y, 1)
        trend_line = np.poly1d(z)(x)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["timestamp"], df["close"], label="收盤價", color="white")
        ax.plot(df["timestamp"], trend_line, label="趨勢線", linestyle="--", color="cyan")
        ax.set_facecolor("black")
        fig.patch.set_facecolor("black")
        ax.tick_params(colors="white")
        ax.yaxis.label.set_color("white")
        ax.xaxis.label.set_color("white")
        ax.legend(facecolor="black", edgecolor="white", labelcolor="white")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"圖表產生錯誤：{e}")

raw_data = fetch_data()
df = process_data(raw_data)
plot_trend(df)
