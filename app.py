import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("BTC 趨勢圖（黑底風格＋趨勢線＋進出場點）")

@st.cache_data
def fetch_proxy_data():
    url = "https://btc-mock-api.vercel.app/api/kline"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"])
    return df

df = fetch_proxy_data()

# 計算線性趨勢線
x = np.arange(len(df))
y = df["close"].values
coef = np.polyfit(x, y, 1)
trend = coef[0] * x + coef[1]

# 偵測進出場點
entry_points = []
exit_points = []
for i in range(2, len(df)):
    if df["close"][i-1] < trend[i-1] and df["close"][i] > trend[i]:
        entry_points.append((df["time"][i], df["close"][i]))
    elif df["close"][i-1] > trend[i-1] and df["close"][i] < trend[i]:
        exit_points.append((df["time"][i], df["close"][i]))

# 繪製圖表
fig = go.Figure()
fig.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(color='white'),
    title="BTC/USDT 每小時K線圖（含趨勢線與進出場提示）"
)

fig.add_trace(go.Scatter(x=df["time"], y=df["close"], mode="lines", name="收盤價", line=dict(color="white")))
fig.add_trace(go.Scatter(x=df["time"], y=trend, mode="lines", name="趨勢線", line=dict(color="yellow", dash="dash")))

if entry_points:
    fig.add_trace(go.Scatter(x=[x[0] for x in entry_points], y=[x[1] for x in entry_points],
                             mode="markers", name="進場", marker=dict(color="green", size=10)))
if exit_points:
    fig.add_trace(go.Scatter(x=[x[0] for x in exit_points], y=[x[1] for x in exit_points],
                             mode="markers", name="出場", marker=dict(color="red", size=10)))

st.plotly_chart(fig, use_container_width=True)

# 顯示模擬通知
if entry_points:
    st.markdown("### 📢 偵測到進場訊號，建議觀察趨勢是否延續")
elif exit_points:
    st.markdown("### ⚠️ 偵測到出場訊號，請注意風險控管")
