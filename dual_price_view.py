
import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

def show_price_view():
    st.title("📈 BTC 即時價格與走勢（Bitstamp API）")

    try:
        ticker = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json()
        current_price = float(ticker['last'])
        st.subheader(f"目前 BTC 價格\n${current_price:,.2f}")

        history = requests.get("https://www.bitstamp.net/api/v2/transactions/btcusd/?time=hour").json()
        times = [datetime.fromtimestamp(int(tx['date'])) for tx in history]
        prices = [float(tx['price']) for tx in history]

        fig = go.Figure(data=go.Scatter(x=times, y=prices, mode='lines+markers', name='BTC Price'))
        fig.update_layout(xaxis_title='時間', yaxis_title='價格')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f"開盤：{float(ticker['open']):,.2f} | "
            f"最高：{float(ticker['high']):,.2f} | "
            f"最低：${float(ticker['low']):,.2f} | "
            f"24h 交易量：{float(ticker['volume']):.2f} BTC"
        )
    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
