
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("📈 BTC 趨勢進出場圖（TradingView 展示版）")

st.markdown("以下為 BTCUSDT 1小時圖表，來源：**TradingView**")

tradingview_widget = """
<iframe 
  src="https://www.tradingview.com/widgetembed/?frameElementId=tradingview_3c6ba&symbol=BINANCE:BTCUSDT&interval=60&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=light&style=1&timezone=Asia/Taipei&withdateranges=1&hideideas=1&watchlist=[]&locale=zh_TW" 
  width="100%" height="610" frameborder="0" allowtransparency="true" scrolling="no">
</iframe>
"""

components.html(tradingview_widget, height=630)
