import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# ================= AUTO REFRESH =================
st_autorefresh(interval=60000, key="refresh")  # 60 sec

# ================= CONFIG =================
st.set_page_config(page_title="Stock Dashboard PRO", layout="wide")
st.title("📊 Dashboard LIVE PRO")

# ================= GRUPE =================
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    "💰 PIE OT": ["AMZN", "JPM", "PLD", "WMT", "LLY", "NEE", "META", "XOM", "MSFT"],
    "📈 PIE 20": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", "BRK-B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

# ================= CACHE =================
@st.cache_data(ttl=300)
def get_history(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1y")

# ================= CHART =================
def plot_chart(hist, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist["Close"],
        mode="lines",
        name=ticker
    ))
    fig.update_layout(height=250, margin=dict(l=0,r=0,t=20,b=0))
    return fig

# ================= DATA =================
def get_price_data(ticker):
    try:
        hist = get_history(ticker)
        if hist.empty:
            return None

        current = hist["Close"].iloc[-1]
        prev = hist["Close"].iloc[-2] if len(hist) > 1 else current

        change = ((current - prev) / prev) * 100

        return current, change, hist

    except:
        return None

# ================= UI =================
for group, ticks in groups.items():
    st.markdown(f"## {group}")
    cols = st.columns(3)

    for i, t in enumerate(ticks):
        data = get_price_data(t)

        if not data:
            continue

        price, change, hist = data
        emoji = "🟢" if change >= 0 else "🔴"

        with cols[i % 3]:
            st.metric(t, f"${price:.2f}", f"{emoji} {change:.2f}%")
            st.plotly_chart(plot_chart(hist.tail(100), t), use_container_width=True)

    st.markdown("---")

st.caption("LIVE PRO Dashboard • Streamlit + Yahoo Finance")
