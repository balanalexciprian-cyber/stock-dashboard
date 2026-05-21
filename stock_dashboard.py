import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Prețuri LIVE - Dashboard Personal")

# Grupe
groups = {
    "🤖 AI TECH": ["NVDA", "TSM", "AVGO", "ASML", "AMAT", "MU"],
    "💰 PIE OT Investimental": ["AMZN", "MSFT", "META", "GOOG", "JPM"],
    "📈 Alex PIE 20": ["AAPL", "NVDA", "MSFT", "AMZN", "META", "GOOG", "TSLA", "AVGO"]
}

st.sidebar.header("⚙️ Setări")
if st.button("🔄 Refresh Manual"):
    st.rerun()

for group_name, tickers in groups.items():
    st.subheader(group_name)
    cols = st.columns(4)
    
    for i, tick in enumerate(tickers):
        try:
            ticker = yf.Ticker(tick)
            info = ticker.info
            price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
            change_pct = info.get('regularMarketChangePercent') or 0
            
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

st.caption("Actualizat live cu Yahoo Finance")
