import streamlit as st
import yfinance as yf
from datetime import date

st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE - Dashboard Personal")

# ====================== GRUPE ======================
groups = {
    "🤖 AI TECH": ["NVDA", "TSM", "AVGO", "ASML", "AMAT", "MU", "INTC"],
    "💰 PIE OT Investimental": ["AMZN", "MSFT", "META", "GOOG", "JPM"],
    "📈 Alex PIE 20": ["AAPL", "NVDA", "MSFT", "AMZN", "META", "GOOG", "TSLA", "AVGO", "ORCL"]
}

# Date de referință
pie_ot_date = date(2024, 7, 22)
alex_pie_date = date(2025, 1, 1)

total_pie20 = 1100.0
total_pie_ot = 371.21 + 74.70

st.sidebar.header("⚙️ Setări")
if st.button("🔄 Refresh Manual"):
    st.rerun()

def get_data(tick, group_name):
    try:
        stock = yf.Ticker(tick)
        info = stock.info
        hist = stock.history(period="2y")
        
        current = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
        
        if group_name == "🤖 AI TECH":
            ref = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2]
        elif group_name == "💰 PIE OT Investimental":
            ref = hist[hist.index.date <= pie_ot_date].iloc[-1]['Close']
        else:
            ref = hist[hist.index.date <= alex_pie_date].iloc[-1]['Close']
        
        change_pct = (current - ref) / ref * 100
        return {'price': current, 'change_pct': change_pct}
    except:
        return None

# Afișare
for group_name, ticks in groups.items():
    st.markdown(f"### {group_name}")
    cols = st.columns(4)
    total_current = 0.0
    
    for i, tick in enumerate(ticks):
        data = get_data(tick, group_name)
        if data:
            emoji = "🟢" if data['change_pct'] >= 0 else "🔴"
            with cols[i % 4]:
                st.metric(
                    label=f"**{tick}**",
                    value=f"${data['price']:.2f}",
                    delta=f"{emoji} {data['change_pct']:.2f}%"
                )
        else:
            with cols[i % 4]:
                st.metric(label=f"**{tick}**", value="Eroare", delta="")
    
    st.markdown("---")

st.caption("Date de la Yahoo Finance • Actualizare live")
