
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(layout="wide")
st.title("📊 BTC 策略進出場圖表 - Plotly 版")

# 取得 Bybit K 線資料（模擬替代）
url = "https://api.bybit.com/v5/market/kline?category=linear&symbol=BTCUSDT&interval=60&limit=100"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()["result"]["list"]
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume", "turnover"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df = df.astype({"open": "float", "high": "float", "low": "float", "close": "float"})

    # 假設策略進出場點（例如：低點進場，高點出場）
    entry_points = df.iloc[::15]
    exit_points = df.iloc[10::15]

    fig = go.Figure()

    # 畫K線圖
    fig.add_trace(go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="K線"
    ))

    # 畫進場點
    fig.add_trace(go.Scatter(
        x=entry_points["timestamp"],
        y=entry_points["low"],
        mode="markers",
        marker=dict(color="green", size=10),
        name="🟢 進場點"
    ))

    # 畫出場點
    fig.add_trace(go.Scatter(
        x=exit_points["timestamp"],
        y=exit_points["high"],
        mode="markers",
        marker=dict(color="red", size=10),
        name="🔴 出場點"
    ))

    fig.update_layout(
        xaxis_title="時間",
        yaxis_title="價格 (USDT)",
        template="plotly_dark",
        hovermode="x unified",
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error(f"資料讀取失敗：{response.status_code} {response.reason}")
