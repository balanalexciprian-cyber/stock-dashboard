import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Prețuri LIVE - Test Simplu")

tickers = ["NVDA", "AAPL", "TSM", "AVGO", "MSFT", "AMZN", "META"]

for tick in tickers:
    try:
        info = yf.Ticker(tick).info
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        change = info.get('regularMarketChangePercent', 0)
        
        emoji = "🟢" if change >= 0 else "🔴"
        
        st.metric(
            label=f"**{tick}**",
            value=f"${price:.2f}" if price else "N/A",
            delta=f"{emoji} {change:.2f}%"
        )
    except Exception as e:
        st.error(f"{tick} → Eroare")

st.success("Dacă vezi prețuri = funcționează!")
st.caption("Test simplificat - 21 Mai 2026")
