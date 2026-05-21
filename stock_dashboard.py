import streamlit as st
import yfinance as yf
from datetime import date, timedelta

st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE - Dashboard Personal")

# ====================== GRUPE ======================
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", 
                   "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    
    "💰 PIE OT Investimental": ["AMZN", "JPM", "PLD", "WMT", "LLY", 
                               "NEE", "META", "XOM", "MSFT"],
    
    "📈 Alex PIE 20": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", 
                       "BRK.B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", 
                       "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

# Date de referință (realiste)
pie_ot_date1 = date(2024, 7, 22)
alex_pie_date = date(2025, 5, 19)   # am mutat în trecut ca să funcționeze

total_pie20 = 1100.00
alimentare1 = 371.21
alimentare2 = 74.70
total_pie_ot = alimentare1 + alimentare2

st.sidebar.header("⚙️ Setări")
if st.button("🔄 Refresh Manual"):
    st.rerun()

def get_data(tick, group_name):
    try:
        stock = yf.Ticker(tick)
        info = stock.info
        hist = stock.history(period="max")
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
        
        if group_name == "🤖 AI TECH":
            ref_price = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2]
        elif group_name == "💰 PIE OT Investimental":
            ref_row = hist[hist.index.date <= pie_ot_date1].iloc[-1]
            ref_price = ref_row['Close']
        else:
            ref_row = hist[hist.index.date <= alex_pie_date].iloc[-1]
            ref_price = ref_row['Close']
        
        change_pct = (current_price - ref_price) / ref_price * 100 if ref_price else 0
        
        return {
            'price': current_price,
            'change_pct': change_pct,
            'ref_price': ref_price
        }
    except:
        return None

# ====================== AFISARE ======================
for group_name, ticks in groups.items():
    st.markdown(f"### {group_name}")
    cols = st.columns(4)
    total_current = 0
    
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
                
                if group_name != "🤖 AI TECH":
                    amt = (total_pie20 if "PIE 20" in group_name else total_pie_ot) / len(ticks)
                    curr = amt * (data['price'] / data['ref_price']) if data['ref_price'] else amt
                    st.caption(f"${amt:.2f} → ${curr:.2f}")
                    total_current += curr
    
    # Totaluri
    if "PIE 20" in group_name:
        change = (total_current - total_pie20) / total_pie20 * 100
        st.success(f"**TOTAL PIE 20**: {'🟢' if change >= 0 else '🔴'} **{change:.2f}%** | ${total_pie20:,.0f} → ${total_current:,.0f}")
    elif "PIE OT" in group_name:
        change = (total_current - total_pie_ot) / total_pie_ot * 100
        st.success(f"**TOTAL PIE OT**: {'🟢' if change >= 0 else '🔴'} **{change:.2f}%** | ${total_pie_ot:,.2f} → ${total_current:,.2f}")
    else:
        avg = sum(d['change_pct'] for d in [get_data(t, group_name) for t in ticks if get_data(t, group_name)]) / len(ticks)
        st.success(f"**Total {group_name}**: {'🟢' if avg >= 0 else '🔴'} **{avg:.2f}%**")
    
    st.markdown("---")

st.caption("Date de la Yahoo Finance • Actualizare live")
