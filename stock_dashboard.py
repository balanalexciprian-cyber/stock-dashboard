import streamlit as st
import yfinance as yf
from datetime import date

st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE - Dashboard Personal")

# ====================== GRUPE ======================
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", 
                   "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    
    "💰 PIE OT Investimental": ["AMZN", "JPM", "PLD", "WMT", "LLY", 
                               "NEE", "META", "XOM", "MSFT"],
    
    "📈 Alex PIE 20 (19 Mai 2026)": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", 
                                    "BRK.B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", 
                                    "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

# Date fixe
pie_ot_date1 = date(2024, 7, 22)
pie_ot_date2 = date(2026, 4, 28)
alex_pie_date = date(2026, 5, 19)

total_pie20 = 1100.00
alimentare1_pieot = 371.21
alimentare2_pieot = 74.70
total_pie_ot = alimentare1_pieot + alimentare2_pieot

st.sidebar.header("⚙️ Setări")
if st.button("🔄 Refresh Manual"):
    st.rerun()

def get_data(tick, group_name):
    try:
        stock = yf.Ticker(tick)
        info = stock.info
        hist = stock.history(period="3y")
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
        
        if group_name == "🤖 AI TECH":
            prev_close = info.get('regularMarketPreviousClose') or (hist['Close'].iloc[-2] if len(hist) > 1 else current_price)
            ref_price = prev_close
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
    
    total_current_value = 0
    cols = st.columns(4)
    
    for i, tick in enumerate(ticks):
        data = get_data(tick, group_name)
        if data:
            emoji = "🟢" if data['change_pct'] >= 0 else "🔴"
            amount_per_stock = 0
            current_value = 0
            
            if group_name == "📈 Alex PIE 20 (19 Mai 2026)":
                amount_per_stock = total_pie20 / len(ticks)
                current_value = amount_per_stock * (data['price'] / data['ref_price']) if data['ref_price'] else amount_per_stock
                total_current_value += current_value
            elif group_name == "💰 PIE OT Investimental":
                amount_per_stock = total_pie_ot / len(ticks)
                current_value = amount_per_stock * (data['price'] / data['ref_price']) if data['ref_price'] else amount_per_stock
                total_current_value += current_value
            
            with cols[i % 4]:
                st.metric(
                    label=f"**{tick}**", 
                    value=f"${data['price']:.2f}", 
                    delta=f"{emoji} {data['change_pct']:.2f}%"
                )
                if group_name != "🤖 AI TECH":
                    st.caption(f"${amount_per_stock:.2f} → ${current_value:.2f}")
    
    # Totaluri
    if group_name == "📈 Alex PIE 20 (19 Mai 2026)":
        change = (total_current_value - total_pie20) / total_pie20 * 100
        st.success(f"**TOTAL PORTFOLIU PIE 20**: {'🟢' if change >= 0 else '🔴'} **{change:.2f}%** | ${total_pie20:,.0f} → ${total_current_value:,.0f}")
        st.info(f"Suma totală investită: **${total_pie20:.2f}** (19.05.2026)")
        
    elif group_name == "💰 PIE OT Investimental":
        change = (total_current_value - total_pie_ot) / total_pie_ot * 100
        st.success(f"**TOTAL PIE OT Investimental**: {'🟢' if change >= 0 else '🔴'} **{change:.2f}%** | ${total_pie_ot:,.2f} → ${total_current_value:,.2f}")
        st.info(f"Alimentări: ${alimentare1_pieot:.2f} (22.07.2024) + ${alimentare2_pieot:.2f} (28.04.2026)")
    
    else:
        avg_change = sum([get_data(t, group_name)['change_pct'] for t in ticks if get_data(t, group_name)]) / len(ticks)
        st.success(f"**Total {group_name}**: {'🟢' if avg_change >= 0 else '🔴'} **{avg_change:.2f}%**")
    
    st.markdown("---")

st.caption("Date de la Yahoo Finance • Actualizare live")
