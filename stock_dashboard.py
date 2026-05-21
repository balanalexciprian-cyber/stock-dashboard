import streamlit as st
import yfinance as yf

st.title("🔍 Debug Dashboard")

if st.button("🔄 Refresh"):
    st.rerun()

tickers = ["NVDA", "AAPL", "TSM"]

for tick in tickers:
    try:
        info = yf.Ticker(tick).info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        change = info.get('regularMarketChangePercent', 0)
        
        st.success(f"**{tick}** → ${price:.2f} | {change:.2f}%")
        
    except Exception as e:
        st.error(f"**{tick}** → Eroare")
        st.write(str(e)[:300])   # arată eroarea exactă
