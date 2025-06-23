import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="BTC 趨勢圖", layout="wide")
st.title("📈 BTC 趨勢線判讀工具")

API_URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

@st.cache_data(ttl=600)
def fetch_data():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "_", "__", "___", "____", "_____", "______"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df["close"] = pd.to_numeric(df["close"])
        return df
    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
        return None

df = fetch_data()
if df is not None and not df.empty:
    st.success("✅ 成功取得資料")
    x = np.arange(len(df))
    y = df["close"].values
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)(x)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["timestamp"], y, label="收盤價", color="white")
    ax.plot(df["timestamp"], trend, "--", label="趨勢線", color="orange")
    ax.set_facecolor("black")
    ax.tick_params(colors="white")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("⚠️ 無法取得資料，請稍後再試")