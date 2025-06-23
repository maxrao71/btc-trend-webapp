
import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime

st.title("BTC 趨勢圖：黑底＋進出場提示")

# 抓取 Binance K線資料
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
response = requests.get(url)
raw_data = response.json()

try:
    # 解析資料
    timestamps = [datetime.fromtimestamp(item[0] / 1000) for item in raw_data]
    closes = [float(item[4]) for item in raw_data]

    df = pd.DataFrame({'timestamp': timestamps, 'close': closes})

    # 線性回歸
    x = np.arange(len(df))
    y = df['close'].values
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)(x)

    # 找出進場/出場點（例：突破趨勢線）
    entry_points = df[df['close'] > trend]
    exit_points = df[df['close'] < trend]

    # 畫圖
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='收盤價'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=trend, mode='lines', name='趨勢線'))
    fig.add_trace(go.Scatter(x=entry_points['timestamp'], y=entry_points['close'], mode='markers', name='進場', marker=dict(color='green', size=8)))
    fig.add_trace(go.Scatter(x=exit_points['timestamp'], y=exit_points['close'], mode='markers', name='出場', marker=dict(color='red', size=8)))
    fig.update_layout(template='plotly_dark', title='BTC 趨勢圖', xaxis_title='時間', yaxis_title='價格')
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"資料讀取失敗：{str(e)}")
