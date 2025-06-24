
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(layout="wide", page_title="BTC 趨勢預測雙視圖")

# 模擬資料（實際部署可替換為即時 API）
def load_data():
    now = datetime.utcnow()
    times = [now - timedelta(hours=i) for i in reversed(range(100))]
    prices = np.cumsum(np.random.randn(100)) + 27000
    ai_pred = prices + np.random.randn(100)
    return pd.DataFrame({
        "time": times,
        "price": prices,
        "ai_prediction": ai_pred
    })

df = load_data()

# 畫實價走勢圖
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df["time"], y=df["price"], mode="lines+markers", name="實際價格"))
fig1.update_layout(title="實際價格走勢圖", height=400)

# 畫 AI 預測圖
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["time"], y=df["ai_prediction"], mode="lines", name="AI 預測"))
fig2.update_layout(title="AI 趨勢預測", height=400)

# 畫面排版
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
