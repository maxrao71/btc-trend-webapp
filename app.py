
import streamlit as st
import requests
import numpy as np
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("BTC 趨勢圖：黑底＋進出場提示")

def fetch_data():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=100"
    try:
        res = requests.get(url)
        data = res.json()
        closes = [float(item[4]) for item in data]
        if not closes:
            st.error("無法取得有效的 BTC 收盤價數據，請稍後再試。")
            st.stop()
        return closes
    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
        st.stop()

closes = fetch_data()
x = np.arange(len(closes))
y = np.array(closes)

if len(x) == 0 or len(y) == 0:
    st.error("線性趨勢擬合失敗，因為輸入資料為空。")
    st.stop()

coef = np.polyfit(x, y, 1)
trend = coef[0] * x + coef[1]

fig = go.Figure()
fig.add_trace(go.Scatter(y=closes, mode="lines", name="收盤價"))
fig.add_trace(go.Scatter(y=trend, mode="lines", name="趨勢線"))

# 判斷進出場訊號
if coef[0] > 0:
    fig.add_annotation(text="進場點", x=len(x)-1, y=closes[-1], showarrow=True, arrowhead=1, font=dict(color="green"))
else:
    fig.add_annotation(text="出場點", x=len(x)-1, y=closes[-1], showarrow=True, arrowhead=1, font=dict(color="red"))

fig.update_layout(template="plotly_dark", height=600)
st.plotly_chart(fig, use_container_width=True)
