import streamlit as st
import yfinance as yf
from datetime import date

# ====================== CONFIG ======================
st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")
st.title("📊 Prețuri LIVE - Dashboard Personal")

# ====================== GRUPE ======================
groups = {
    "🤖 AI TECH": ["NTNX", "MSTR", "TSM", "INTC", "MU", "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
    "💰 PIE OT Investimental": ["AMZN", "JPM", "PLD", "WMT", "LLY", "NEE", "META", "XOM", "MSFT"],
    "📈 Alex PIE 20 (19 Mai 2026)": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", "BRK-B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", "GOOG", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"]
}

pie_ot_date = date(2024, 7, 22)
alex_pie_date = date(2025, 5, 19)

total_pie20 = 1100.00
alimentare1 = 371.21
alimentare2 = 74.70
total_pie_ot = alimentare1 + alimentare2

# ====================== UI ======================
st.sidebar.header("⚙️ Setări")

if st.sidebar.button("🔄 Refresh Manual"):
    st.cache_data.clear()
    st.rerun()


# ====================== CACHE DATA ======================
@st.cache_data(ttl=300)
def fetch_history(tick):
    try:
        stock = yf.Ticker(tick)
        hist = stock.history(period="3y")
        return hist
    except:
        return None


def get_data(tick, group_name):
    try:
        hist = fetch_history(tick)

        if hist is None or hist.empty:
            return None

        current_price = hist["Close"].iloc[-1]

        # reference price logic
        if group_name == "🤖 AI TECH":
            ref_price = hist["Close"].iloc[-2] if len(hist) > 1 else current_price
        else:
            target_date = pie_ot_date if group_name == "💰 PIE OT Investimental" else alex_pie_date
            past = hist[hist.index.date <= target_date]

            if not past.empty:
                ref_price = past["Close"].iloc[-1]
            else:
                ref_price = hist["Close"].iloc[0]

        change_pct = ((current_price - ref_price) / ref_price) * 100 if ref_price else 0

        return {
            "price": float(current_price),
            "change_pct": float(change_pct),
            "ref_price": float(ref_price)
        }

    except Exception as e:
        st.warning(f"{tick}: {e}")
        return None


# ====================== DISPLAY ======================
for group_name, ticks in groups.items():
    st.markdown(f"### {group_name}")
    cols = st.columns(4)

    total_current = 0.0

    for i, tick in enumerate(ticks):
        data = get_data(tick, group_name)

        if not data:
            continue

        emoji = "🟢" if data["change_pct"] >= 0 else "🔴"

        with cols[i % 4]:
            st.metric(
                label=tick,
                value=f"${data['price']:.2f}",
                delta=f"{emoji} {data['change_pct']:.2f}%"
            )

            # portfolio logic (only for non AI TECH)
            if group_name != "🤖 AI TECH":
                total_invested = total_pie20 if "PIE 20" in group_name else total_pie_ot
                amt_per = total_invested / len(ticks)

                current_val = amt_per * (data["price"] / data["ref_price"]) if data["ref_price"] else amt_per
                total_current += current_val

                st.caption(f"${amt_per:.2f} → ${current_val:.2f}")

    # ====================== TOTALS ======================
    if "PIE 20" in group_name:
        change = ((total_current - total_pie20) / total_pie20) * 100
        st.success(
            f"**TOTAL ALEX PIE 20**: {'🟢' if change >= 0 else '🔴'} "
            f"{change:.2f}% | ${total_pie20:,.0f} → ${total_current:,.0f}"
        )
        st.info("Referință: 19.05.2026")

    elif "PIE OT" in group_name:
        change = ((total_current - total_pie_ot) / total_pie_ot) * 100
        st.success(
            f"**TOTAL PIE OT**: {'🟢' if change >= 0 else '🔴'} "
            f"{change:.2f}% | ${total_pie_ot:,.2f} → ${total_current:,.2f}"
        )
        st.info(f"Alimentări: ${alimentare1:.2f} + ${alimentare2:.2f}")

    else:
        st.success(f"**Total {group_name} calculat live**")

    st.markdown("---")

st.caption("Data: Yahoo Finance • Streamlit Cloud ready 🚀")
