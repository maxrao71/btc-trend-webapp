import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="BTC 趨勢線進出場與價格標示", layout="wide")
st.title("📈 BTC 趨勢線、進出場點 ＋ 價格標示（CryptoCompare 數據）")

@st.cache_data(ttl=600)
def fetch_data():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/histohour"
        params = {"fsym": "BTC", "tsym": "USD", "limit": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()["Data"]["Data"]
        df = pd.DataFrame(data)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.rename(columns={"close": "price"}, inplace=True)
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

    signals = []
    for i in range(1, len(y)):
        if y[i - 1] < trend[i - 1] and y[i] > trend[i]:
            signals.append(("entry", df["time"].iloc[i], y[i]))
        elif y[i - 1] > trend[i - 1] and y[i] < trend[i]:
            signals.append(("exit", df["time"].iloc[i], y[i]))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["time"], y, label="價格", color="white")
    ax.plot(df["time"], trend, "--", label="趨勢線", color="orange")

    for sig_type, t, p in signals:
        color = "green" if sig_type == "entry" else "red"
        label = "進場點" if sig_type == "entry" else "出場點"
        ax.scatter(t, p, color=color, s=60, zorder=5)
        ax.annotate(f"${p:.2f}", (t, p), textcoords="offset points", xytext=(0,10),
                    ha='center', color=color, fontsize=8, weight="bold")

    ax.set_facecolor("black")
    ax.tick_params(colors="white")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("⚠️ 無法取得資料，請稍後再試")