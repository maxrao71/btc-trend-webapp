
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objs as go

st.title("BTC 趨勢圖：黑底＋進出場提示")

# 抓取資料
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
try:
    response = requests.get(url)
    raw_data = response.json()

    if not isinstance(raw_data, list) or len(raw_data) == 0:
        st.error("資料格式異常或不足")
    else:
        df = pd.DataFrame(raw_data, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["close"] = df["close"].astype(float)
        df["time"] = pd.to_datetime(df["time"], unit='ms')

        x = np.arange(len(df))
        y = df["close"].values

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=y, mode='lines', name='BTC Price'))

        # 防呆檢查
        if len(x) > 0 and len(y) > 0:
            coef = np.polyfit(x, y, 1)
            trend = np.polyval(coef, x)
            fig.add_trace(go.Scatter(x=df["time"], y=trend, mode='lines', name='Trend'))
        else:
            st.error("資料不足，無法繪製趨勢線")

        st.plotly_chart(fig)

except Exception as e:
    st.error(f"資料讀取失敗：{str(e)}")
