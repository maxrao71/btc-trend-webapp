
import streamlit as st
from dual_price_view import show_price_view
from dual_strategy_view import show_strategy_view

st.set_page_config(page_title="BTC 雙視圖：價格 + 策略預測", layout="wide")

st.sidebar.title("功能選單")
page = st.sidebar.radio("請選擇頁面：", ["📈 即時價格視圖", "📊 策略預測視圖"])

if page == "📈 即時價格視圖":
    show_price_view()
elif page == "📊 策略預測視圖":
    show_strategy_view()
