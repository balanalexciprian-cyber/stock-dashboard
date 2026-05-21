import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE - Dashboard Personal")

st.caption(f"Ultima actualizare: {datetime.now().strftime('%H:%M:%S')}")

if st.button("🔄 Refresh Manual"):
    st.rerun()

# ====================== GRUPE ======================
groups = {
    "🤖 AI TECH": ["NVDA", "TSM", "AVGO", "ASML", "AMAT", "MU", "INTC"],
    "💰 PIE OT Investimental": ["AMZN", "MSFT", "META", "GOOG", "JPM"],
    "📈 Alex PIE 20": ["AAPL", "NVDA", "MSFT", "AMZN", "META", "GOOG", "TSLA", "ORCL", "AVGO"]
}

for group_name, tickers in groups.items():
    st.subheader(group_name)
    cols = st.columns(4)
    
    for i, tick in enumerate(tickers):
        try:
            info = yf.Ticker(tick).info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            change_pct = info.get('regularMarketChangePercent', 0)
            
            emoji = "🟢" if change_pct >= 0 else "🔴"
            
            with cols[i % 4]:
                st.metric(
                    label=f"**{tick}**",
                    value=f"${price:.2f}" if price else "N/A",
                    delta=f"{emoji} {change_pct:.2f}%"
                )
        except:
            with cols[i % 4]:
                st.metric(label=f"**{tick}**", value="Eroare", delta="")
    
    st.markdown("---")

st.caption("Date furnizate de Yahoo Finance")
