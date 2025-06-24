
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("📈 BTC 趨勢預測與互動圖表（CoinGecko）")

# 取得 BTC 歷史價格（近 24 小時，每小時資料）
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "1",
    "interval": "hourly"
}

try:
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()

    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # 簡易進出場策略：若當前價格 > 過去 6 小時平均 +1%，顯示出場；反之顯示進場
    df["ma6"] = df["price"].rolling(window=6).mean()
    df["signal"] = df.apply(lambda row: "進場" if row["price"] < row["ma6"] * 0.99 else ("出場" if row["price"] > row["ma6"] * 1.01 else ""), axis=1)

    # 畫圖
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["timestamp"], y=df["price"], mode='lines+markers', name="BTC Price", hovertemplate='時間: %{x}<br>價格: $%{y:.2f}<extra></extra>'))

    # 加上進出場標記
    entry_points = df[df["signal"] == "進場"]
    exit_points = df[df["signal"] == "出場"]

    fig.add_trace(go.Scatter(x=entry_points["timestamp"], y=entry_points["price"], mode='markers', marker=dict(color='green', size=10), name="進場"))
    fig.add_trace(go.Scatter(x=exit_points["timestamp"], y=exit_points["price"], mode='markers', marker=dict(color='red', size=10), name="出場"))

    fig.update_layout(title="Bitcoin Hourly Trend + Signal", xaxis_title="時間", yaxis_title="價格 (USD)", height=600)

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"❌ 資料讀取失敗：{e}")
