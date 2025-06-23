
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("BTC 趨勢圖：黑底＋進出場提示")

# 🚀 使用你測試成功的 URL
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
r = requests.get(url)
data = r.json()

df = pd.DataFrame(data, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "num_trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

# 畫圖
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df["timestamp"], open=df["open"], high=df["high"],
    low=df["low"], close=df["close"],
    name="K線"
))

# 趨勢線（近20根線性）
x = np.arange(20)
y = df["close"][-20:].values
coef = np.polyfit(x, y, 1)
trend = np.poly1d(coef)(x)
fig.add_trace(go.Scatter(
    x=df["timestamp"][-20:],
    y=trend,
    mode="lines",
    name="趨勢線",
    line=dict(color="yellow", width=2)
))

# 判斷訊號
latest_price = df["close"].iloc[-1]
latest_trend = trend[-1]
signal = None
if latest_price > latest_trend * 1.01:
    signal = "📈 進場訊號！"
    fig.add_trace(go.Scatter(
        x=[df["timestamp"].iloc[-1]], y=[latest_price],
        mode="markers", marker=dict(color="lime", size=12), name="進場"
    ))
elif latest_price < latest_trend * 0.99:
    signal = "⚠️ 出場訊號！"
    fig.add_trace(go.Scatter(
        x=[df["timestamp"].iloc[-1]], y=[latest_price],
        mode="markers", marker=dict(color="red", size=12), name="出場"
    ))

# 顯示
fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

if signal:
    st.markdown(f"### 🔔 {signal}")
