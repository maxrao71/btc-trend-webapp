
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📈 BTC 策略進出場圖表 - CoinCap API 版")

# 計算時間區間（24 小時）
end_time = int(time.mktime(datetime.utcnow().timetuple()) * 1000)
start_time = int(time.mktime((datetime.utcnow() - timedelta(hours=24)).timetuple()) * 1000)

url = f"https://api.coincap.io/v2/assets/bitcoin/history?interval=h1&start={start_time}&end={end_time}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()["data"]

    df = pd.DataFrame(data)
    df["priceUsd"] = df["priceUsd"].astype(float)
    df["time"] = pd.to_datetime(df["time"], unit="ms")

    # 畫圖
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], y=df["priceUsd"], mode="lines+markers", name="BTC Price (USD)"))

    fig.update_layout(title="BTC 小時價格走勢圖（CoinCap）", xaxis_title="時間", yaxis_title="價格 (USD)", height=600)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"資料讀取失敗：{e}")
