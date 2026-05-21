import streamlit as st
import yfinance as yf
from datetime import date

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Prețuri LIVE - Dashboard Personal")

groups = {
    "🤖 AI TECH": ["NVDA", "TSM", "AVGO", "ASML", "AMAT"],
    "💰 PIE OT": ["AMZN", "MSFT", "META", "GOOG"],
    "📈 Alex PIE 20": ["AAPL", "NVDA", "MSFT", "AMZN", "META", "GOOG", "TSLA"]
}

st.sidebar.header("Setări")
if st.button("🔄 Refresh"):
    st.rerun()

for name, ticks in groups.items():
    st.subheader(name)
    cols = st.columns(4)
    for i, tick in enumerate(ticks):
        try:
            data = yf.Ticker(tick).info
            price = data.get('currentPrice') or data.get('regularMarketPrice')
            change = data.get('regularMarketChangePercent', 0)
            emoji = "🟢" if change >= 0 else "🔴"
            with cols[i % 4]:
                st.metric(label=f"**{tick}**", value=f"${price:.2f}" if price else "N/A", 
                         delta=f"{emoji} {change:.2f}%")
        except:
            with cols[i % 4]:
                st.metric(label=f"**{tick}**", value="Eroare", delta="")
    st.markdown("---")

st.caption("Actualizat live cu Yahoo Finance")
