import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Prețuri LIVE - Dashboard Personal")

st.sidebar.header("Setări")
if st.button("🔄 Refresh"):
    st.rerun()

tickers = ["NVDA", "AAPL", "TSM", "AVGO", "MSFT", "AMZN", "META", "GOOG", "TSLA"]

for tick in tickers:
    try:
        with st.spinner(f"Se încarcă {tick}..."):
            ticker = yf.Ticker(tick)
            info = ticker.info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            change = info.get('regularMarketChangePercent', 0)
            
            emoji = "🟢" if change >= 0 else "🔴"
            
            st.metric(
                label=f"**{tick}**",
                value=f"${price:.2f}" if price else "N/A",
                delta=f"{emoji} {change:.2f}%"
            )
    except Exception as e:
        st.error(f"{tick} → Eroare de conexiune")

st.success("Dacă vezi prețuri = funcționează!")
st.caption(f"Ultima actualizare: {datetime.now().strftime('%H:%M:%S')}")
