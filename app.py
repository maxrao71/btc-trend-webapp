import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="BTC 趨勢圖", layout="wide")
st.title("📉 BTC 趨勢圖：黑底＋進出場提示")

def fetch_binance_klines(symbol="BTCUSDT", interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = pd.to_numeric(df["close"])
        return df[["timestamp", "close"]]
    except Exception as e:
        st.error(f"❌ 資料讀取失敗：{e}")
        return None

df = fetch_binance_klines()

if df is not None and not df.empty:
    st.success("✅ 成功取得 BTC 資料")
    st.line_chart(df.rename(columns={"timestamp": "index"}).set_index("index"))

    # 線性趨勢擬合
    x = np.arange(len(df))
    y = df["close"].values
    if len(x) > 1:
        coef = np.polyfit(x, y, 1)
        trend = np.poly1d(coef)
        df["trend"] = trend(x)
        
        # 畫圖
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df["timestamp"], y, label="收盤價")
        ax.plot(df["timestamp"], df["trend"], linestyle="--", color="orange", label="趨勢線")
        ax.set_title("BTC 收盤價與趨勢線")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
else:
    st.warning("無法取得資料，請稍後再試。")