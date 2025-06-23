
import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="BTC 趨勢圖：黑底＋進出場提示", layout="wide")

st.title("📉 BTC 趨勢圖：黑底＋進出場提示")

API_URL = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"

@st.cache_data(ttl=600)
def fetch_data():
    try:
        response = requests.get(API_URL)
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
    st.line_chart(df.set_index("timestamp")["close"])

    try:
        x = np.arange(len(df))
        y = df["close"].values
        coef = np.polyfit(x, y, 1)
        trend = np.poly1d(coef)(x)
        st.line_chart(pd.DataFrame({"price": y, "trend": trend}, index=df["timestamp"]))
    except Exception as e:
        st.warning(f"趨勢線繪製失敗：{e}")
else:
    st.warning("無法取得資料，請稍後再試。")
