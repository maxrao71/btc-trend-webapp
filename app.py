
import streamlit as st
import requests
import pandas as pd
import time
import altair as alt

st.set_page_config(layout="centered")
st.title("📈 BTC 即時價格與走勢（Bitstamp API）")

@st.cache_data(ttl=10)
def get_btc_price_history():
    url = "https://www.bitstamp.net/api/v2/ticker_hour/btcusd/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return float(data["last"]), float(data["open"]), float(data["high"]), float(data["low"]), float(data["volume"])
    except Exception as e:
        return None, None, None, None, None

price, open_, high, low, vol = get_btc_price_history()

if price:
    st.metric("目前 BTC 價格", f"${price:,.2f}")
    st.write(f"📊 開盤：${open_:,.2f}｜最高：${high:,.2f}｜最低：${low:,.2f}｜24h 交易量：{vol:,.2f} BTC")

    # 模擬簡單的價格資料（Bitstamp 沒有提供 K 線歷史）
    history = pd.DataFrame({
        "時間": pd.date_range(end=pd.Timestamp.now(), periods=12, freq="5min"),
        "價格": [price - i*10 + (i % 2)*20 for i in range(12)]
    })

    chart = alt.Chart(history).mark_line(point=True).encode(
        x="時間:T",
        y="價格:Q",
        tooltip=["時間", "價格"]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

else:
    st.error("❌ 無法取得即時價格，請稍後再試。")
