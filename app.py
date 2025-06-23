import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="BTC 趨勢線預測互動圖", layout="wide")
st.title("📈 BTC 趨勢線進出場提示（互動式圖表＋預測）")

@st.cache_data(ttl=600)
def fetch_data():
    try:
        url = "https://min-api.cryptocompare.com/data/v2/histohour"
        params = {"fsym": "BTC", "tsym": "USD", "limit": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()["Data"]["Data"]
        df = pd.DataFrame(data)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.rename(columns={"close": "price"}, inplace=True)
        return df
    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
        return None

df = fetch_data()
if df is not None and not df.empty:
    st.success("✅ 成功取得資料")
    x = np.arange(len(df))
    y = df["price"].values
    coef = np.polyfit(x, y, 1)
    trend = np.poly1d(coef)(x)

    # 計算進出場點
    signals = []
    for i in range(1, len(y)):
        if y[i - 1] < trend[i - 1] and y[i] > trend[i]:
            signals.append(("entry", df["time"].iloc[i], y[i]))
        elif y[i - 1] > trend[i - 1] and y[i] < trend[i]:
            signals.append(("exit", df["time"].iloc[i], y[i]))

    # 建立互動式圖表
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["time"], y=df["price"],
        mode='lines+markers',
        name='價格',
        line=dict(color='white'),
        hovertemplate='時間: %{x}<br>價格: $%{y:.2f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=df["time"], y=trend,
        mode='lines',
        name='趨勢線',
        line=dict(dash='dot', color='orange'),
        hoverinfo='skip'
    ))

    for sig_type, t, p in signals:
        fig.add_trace(go.Scatter(
            x=[t], y=[p],
            mode='markers+text',
            name='進場點' if sig_type == 'entry' else '出場點',
            marker=dict(color='green' if sig_type == 'entry' else 'red', size=10),
            text=[f"${p:.2f}"],
            textposition="top center",
            hovertemplate='類型: ' + ('進場點' if sig_type == 'entry' else '出場點') +
                          '<br>價格: $%{y:.2f}<br>時間: %{x}<extra></extra>'
        ))

    fig.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        title="BTC 價格走勢與進出場點",
        xaxis=dict(title='時間'),
        yaxis=dict(title='價格 (USD)'),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # 預留：未來加入多趨勢線預測
    st.markdown("🧠 *預測模組開發中，將提供下一波進場/出場時機分析*")
else:
    st.warning("⚠️ 無法取得資料，請稍後再試")