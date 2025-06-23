
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("BTC 趨勢圖：黑底＋進出場提示")

@st.cache_data
def fetch_data():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    df["close"] = df["close"].astype(float)
    return df

df = fetch_data()

fig = go.Figure()
fig.update_layout(template="plotly_dark", title="BTC 價格趨勢圖")

# 畫出收盤價線
fig.add_trace(go.Scatter(x=df['time'], y=df['close'], mode='lines', name='Close'))

# 線性回歸趨勢線
x = np.arange(len(df))
y = df["close"].values

if len(x) == len(y):
    coef = np.polyfit(x, y, 1)
    trend = coef[0] * x + coef[1]
    fig.add_trace(go.Scatter(x=df["time"], y=trend, mode="lines", name="Trend Line"))
else:
    st.warning("資料長度不一致，無法計算趨勢線。")

# 進出場提示 (簡化版)
entry_price = df["close"].iloc[-2]
latest_price = df["close"].iloc[-1]

if latest_price > entry_price * 1.01:
    st.success("📈 出場訊號（漲超過 1%）")
elif latest_price < entry_price * 0.99:
    st.error("📉 進場訊號（跌超過 1%）")
else:
    st.info("⏳ 尚未出現明確訊號")

st.plotly_chart(fig, use_container_width=True)
