import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE + Grafice Interactive")

# ====================== GRUPE ======================
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    "💰 PIE OT Investimental": ["AMZN", "JPM", "PLD", "WMT", "LLY", "NEE", "META", "XOM", "MSFT"],
    "📈 Alex PIE 20 (19 Mai 2026)": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", "BRK.B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

# Date referință
pie_ot_date = date(2024, 7, 22)
alex_pie_date = date(2025, 5, 19)

total_pie20 = 1100.00
total_pie_ot = 371.21 + 74.70

st.sidebar.header("⚙️ Setări")
period = st.sidebar.selectbox("Perioadă grafic", ["1mo", "3mo", "6mo", "1y", "2y"], index=3)

if st.button("🔄 Refresh Manual"):
    st.rerun()

def get_data(tick, group_name):
    try:
        stock = yf.Ticker(tick)
        info = stock.info
        hist = stock.history(period=period)
        
        current = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
        
        if group_name == "🤖 AI TECH":
            ref = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2] if len(hist) > 1 else current
        elif group_name == "💰 PIE OT Investimental":
            ref_row = hist[hist.index.date <= pie_ot_date].iloc[-1] if not hist.empty else None
            ref = ref_row['Close'] if ref_row is not None else current
        else:
            ref_row = hist[hist.index.date <= alex_pie_date].iloc[-1] if not hist.empty else None
            ref = ref_row['Close'] if ref_row is not None else current
        
        change_pct = (current - ref) / ref * 100 if ref else 0
        return {'price': current, 'change_pct': change_pct, 'hist': hist}
    except:
        return None

# ====================== AFISARE ======================
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
                
                if group_name != "🤖 AI TECH":
                    total_invested = total_pie20 if "PIE 20" in group_name else total_pie_ot
                    amt_per = total_invested / len(ticks)
                    current_val = amt_per * (data['price'] / data.get('ref_price', data['price']))
                    total_current += current_val
                    st.caption(f"${amt_per:.2f} → ${current_val:.2f}")
    
    # Total grup
    if "PIE 20" in group_name:
        change = (total_current - total_pie20) / total_pie20 * 100
        st.success(f"**TOTAL ALEX PIE 20**: {'🟢' if change >= 0 else '🔴'} **{change:.2f}%** | ${total_pie20:,.0f} → ${total_current:,.0f}")
    elif "PIE OT" in group_name:
        change = (total_current - total_pie_ot) / total_pie_ot * 100
        st.success(f"**TOTAL PIE OT**: {'🟢' if change >= 0 else '🔴'} **{change:.2f}%** | ${total_pie_ot:,.2f} → ${total_current:,.2f}")
    
    st.markdown("---")

    # ==================== GRAFICE INTERACTIVE ====================
    st.markdown("**Grafice Interactive**")
    chart_cols = st.columns(2)
    for i, tick in enumerate(ticks[:6]):   # primele 6 ca să nu fie prea multe
        data = get_data(tick, group_name)
        if data and not data['hist'].empty:
            hist = data['hist']
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=tick,
                increasing_line_color='#00ff88',
                decreasing_line_color='#ff4444'
            ))
            fig.update_layout(
                title=f"{tick} - {period}",
                height=350,
                template="plotly_dark",
                margin=dict(t=40, b=20),
                xaxis_rangeslider_visible=False
            )
            with chart_cols[i % 2]:
                st.plotly_chart(fig, use_container_width=True)

st.caption("Date de la Yahoo Finance • Grafice interactive cu Plotly")
