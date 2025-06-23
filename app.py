import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="BTC 趨勢圖 - CoinGecko 版", layout="wide")
st.title("📈 BTC 趨勢線判讀工具（使用 CoinGecko 數據）")

@st.cache_data(ttl=600)
def fetch_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "3",
            "interval": "hourly"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        prices = response.json().get("prices", [])
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
        return None

df = fetch_data()
if df is not None and not df.empty:
    st.success("✅ 成功取得資料")
    x = np.arange(len(df))
    y = df["price"].values
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)(x)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["timestamp"], y, label="價格", color="white")
    ax.plot(df["timestamp"], trend, "--", label="趨勢線", color="orange")
    ax.set_facecolor("black")
    ax.tick_params(colors="white")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("⚠️ 無法取得資料，請稍後再試")