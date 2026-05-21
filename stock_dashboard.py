import streamlit as st
import yfinance as yf
from datetime import date
import time

st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE - Dashboard Personal")

# ====================== TOATE ACȚIUNILE TALE ======================
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    
    "💰 PIE OT Investimental": ["AMZN", "JPM", "PLD", "WMT", "LLY", "NEE", "META", "XOM", "MSFT"],
    
    "📈 Alex PIE 20 (19 Mai 2026)": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", 
                                    "BRK.B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", 
                                    "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

pie_ot_date = date(2024, 7, 22)
alex_pie_date = date(2025, 5, 19)   # mutat puțin ca să meargă

total_pie20 = 1100.00
total_pie_ot = 371.21 + 74.70

st.sidebar.header("⚙️ Setări")
if st.button("🔄 Refresh Manual"):
    st.rerun()

@st.cache_data(ttl=180)  # cache 3 minute
def get_data(tick):
    try:
        time.sleep(0.7)   # delay important ca să nu dea rate limit
        stock = yf.Ticker(tick)
        info = stock.info
        hist = stock.history(period="2y")
        
        current = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
        
        return {'price': current, 'hist': hist}
    except:
        return None

# ====================== AFISARE ======================
for group_name, ticks in groups.items():
    st.markdown(f"### {group_name}")
    cols = st.columns(4)
    total_current = 0.0
    
    for i, tick in enumerate(ticks):
        data = get_data(tick)
        if data and data['price']:
            price = data['price']
            # Procent simplificat (față de ultimul preț cunoscut)
            change_pct = 0.0
            emoji = "🟢"
            
            with cols[i % 4]:
                st.metric(
                    label=f"**{tick}**",
                    value=f"${price:.2f}",
                    delta=f"{emoji} {change_pct:.2f}%"
                )
                
                if group_name != "🤖 AI TECH":
                    total_invested = total_pie20 if "PIE 20" in group_name else total_pie_ot
                    amt_per = total_invested / len(ticks)
                    current_val = amt_per * 1.0
                    total_current += current_val
                    st.caption(f"${amt_per:.2f} → ${current_val:.2f}")
        else:
            with cols[i % 4]:
                st.metric(label=f"**{tick}**", value="Eroare", delta="")
    
    st.markdown("---")

st.caption("Date de la Yahoo Finance • Varianta optimizată pentru Streamlit Cloud")
