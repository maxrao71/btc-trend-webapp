
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objs as go

st.title("BTC 趨勢圖：黑底＋進出場提示")

@st.cache_data
def fetch_data():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
    try:
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list):
            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_asset_volume", "number_of_trades",
                "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            df.dropna(subset=["close"], inplace=True)
            return df
        else:
            st.error("資料讀取失敗：API 回傳格式錯誤")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
        return pd.DataFrame()

df = fetch_data()
if df.empty:
    st.warning("無法取得資料，請稍後再試。")
else:
    st.subheader("BTC 收盤價走勢")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["close"], mode="lines", name="Close"))

    # 線性回歸趨勢線（如果資料夠）
    if len(df) > 10:
        x = np.arange(len(df))
        y = df["close"].values
        coef = np.polyfit(x, y, 1)
        trend = coef[0] * x + coef[1]
        fig.add_trace(go.Scatter(x=df["timestamp"], y=trend, mode="lines", name="Trend", line=dict(dash="dot")))

    fig.update_layout(xaxis_title="時間", yaxis_title="價格 (USDT)", height=500)
    st.plotly_chart(fig)
