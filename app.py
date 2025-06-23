
import streamlit as st
import requests
import datetime
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="BTC 趨勢圖", layout="wide")
st.markdown("<h1 style='color:#2c64c8;'>BTC 趨勢圖：黑底＋進出場提示</h1>", unsafe_allow_html=True)

# 抓取實時資料
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
try:
    response = requests.get(url)
    data = response.json()
    if not data or not isinstance(data, list) or len(data[0]) < 5:
        st.error("資料格式異常或不足")
        st.stop()

    timestamps = [datetime.datetime.fromtimestamp(item[0]/1000) for item in data]
    closes = [float(item[4]) for item in data]

    # 計算線性趨勢線
    x = np.arange(len(closes))
    y = np.array(closes)
    coef = np.polyfit(x, y, 1)
    trend = coef[0] * x + coef[1]

    # 建立圖表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=closes, mode='lines', name='收盤價'))
    fig.add_trace(go.Scatter(x=timestamps, y=trend, mode='lines', name='趨勢線'))

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"資料讀取失敗：{e}")
