import streamlit as st
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Stock Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE - Dashboard Personal")

st.caption(f"Ultima actualizare: {datetime.now().strftime('%H:%M:%S')}")

if st.button("🔄 Refresh Manual"):
    st.rerun()

# Grupe complete
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    "💰 PIE OT Investimental": ["AMZN", "JPM", "PLD", "WMT", "LLY", "NEE", "META", "XOM", "MSFT"],
    "📈 Alex PIE 20": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", "BRK.B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

for group_name, ticks in groups.items():
    st.markdown(f"### {group_name}")
    cols = st.columns(4)
    
    for i, tick in enumerate(ticks):
        try:
            info = yf.Ticker(tick).info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            change = info.get('regularMarketChangePercent', 0)
            
            emoji = "🟢" if change >= 0 else "🔴"
            
            with cols[i % 4]:
                st.metric(
                    label=f"**{tick}**",
                    value=f"${price:.2f}" if price else "N/A",
                    delta=f"{emoji} {change:.2f}%"
                )
        except:
            with cols[i % 4]:
                st.metric(label=f"**{tick}**", value="Eroare", delta="")
    
    st.markdown("---")

st.caption("Date de la Yahoo Finance • Versiune stabilă")
