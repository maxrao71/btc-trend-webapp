
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

st.title("BTC 趨勢圖：黑底＋進出場提示")

try:
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1h",
        "limit": 100
    }
    response = requests.get(url, params=params)
    data = response.json()

    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
        df["close"] = pd.to_numeric(df["close"])

        st.line_chart(df[["timestamp", "close"]].set_index("timestamp"))

    else:
        st.error("資料格式異常或不足")

except Exception as e:
    st.error(f"資料讀取失敗：{str(e)}")
