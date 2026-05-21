import streamlit as st
import yfinance as yf
from datetime import date
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ================= AUTO REFRESH =================
st_autorefresh(interval=60000, key="refresh")

# ================= CONFIG =================
st.set_page_config(page_title="Stock Dashboard PRO", layout="wide", page_icon="📊")
st.title("📊 Dashboard LIVE PRO")

# ================= GRUPE =================
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    "💰 PIE OT Investimental": ["AMZN", "JPM", "PLD", "WMT", "LLY", "NEE", "META", "XOM", "MSFT"],
    "📈 Alex PIE 20": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", "BRK-B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

pie_ot_date = date(2024, 7, 22)
alex_pie_date = date(2025, 5, 19)

total_pie20 = 1100.00
alimentare1 = 371.21
alimentare2 = 74.70
total_pie_ot = alimentare1 + alimentare2

# ================= CACHE =================
@st.cache_data(ttl=300)
def get_history(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        return hist
    except:
        return None

# ================= CHART =================
def plot_chart(hist, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        name=ticker
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=20, b=0)
    )

    return fig

# ================= PRICE LOGIC =================
def get_data(ticker, group_name):
    try:
        hist = get_history(ticker)

        if hist is None or hist.empty:
            return None

        current = hist["Close"].iloc[-1]

        if group_name == "🤖 AI TECH":
            ref = hist["Close"].iloc[-2] if len(hist) > 1 else current
        else:
            target = pie_ot_date if group_name == "💰 PIE OT Investimental" else alex_pie_date
            past = hist[hist.index.date <= target]

            ref = past["Close"].iloc[-1] if not past.empty else hist["Close"].iloc[0]

        change = ((current - ref) / ref) * 100 if ref else 0

        return current, change, hist

    except:
        return None

# ================= UI =================
for group_name, ticks in groups.items():
    st.markdown(f"## {group_name}")

    cols = st.columns(3)
    total_current = 0.0

    for i, tick in enumerate(ticks):
        data = get_data(tick, group_name)

        if not data:
            continue

        price, change, hist = data
        emoji = "🟢" if change >= 0 else "🔴"

        with cols[i % 3]:
            st.metric(tick, f"${price:.2f}", f"{emoji} {change:.2f}%")

            st.plotly_chart(
                plot_chart(hist.tail(100), tick),
                use_container_width=True,
                key=f"chart_{group_name}_{tick}_{i}"
            )

            if group_name != "🤖 AI TECH":
                total_invested = total_pie20 if "PIE 20" in group_name else total_pie_ot
                amt_per = total_invested / len(ticks)

                current_val = amt_per * (price / ref) if ref else amt_per
                total_current += current_val

                st.caption(f"${amt_per:.2f} → ${current_val:.2f}")

    # ================= TOTALS =================
    if "PIE 20" in group_name:
        change = ((total_current - total_pie20) / total_pie20) * 100
        st.success(f"PIE 20: {'🟢' if change >= 0 else '🔴'} {change:.2f}% | ${total_pie20:,.0f} → ${total_current:,.0f}")

    elif "PIE OT" in group_name:
        change = ((total_current - total_pie_ot) / total_pie_ot) * 100
        st.success(f"PIE OT: {'🟢' if change >= 0 else '🔴'} {change:.2f}% | ${total_pie_ot:,.2f} → ${total_current:,.2f}")

    else:
        st.success("AI TECH live tracking")

    st.markdown("---")

st.caption("LIVE PRO Dashboard • Streamlit Cloud Ready 🚀")
