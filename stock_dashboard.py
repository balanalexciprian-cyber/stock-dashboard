import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from twelvedata import TDClient

st.set_page_config(
    page_title="Investimental Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f5f5f7 0%, #ffffff 100%);
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #111111;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 16px;
    color: #6e6e73;
    margin-bottom: 28px;
}

.apple-card {
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 28px;
    padding: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.08);
    margin-bottom: 22px;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

[data-testid="stTabs"] button {
    color: #111111 !important;
    font-weight: 700 !important;
}

[data-testid="stTabs"] button p {
    color: #111111 !important;
}

@media screen and (max-width: 768px) {
    .main-title {
        font-size: 31px;
    }

    [data-testid="stMetricValue"] {
        font-size: 22px;
    }
}

@media (prefers-color-scheme: dark) {
    .stApp {
        background: linear-gradient(180deg, #0f0f10 0%, #1c1c1e 100%);
    }

    .main-title {
        color: #f5f5f7 !important;
    }

    .subtitle {
        color: #a1a1a6 !important;
    }

    .apple-card {
        background: rgba(28, 28, 30, 0.90);
        border: 1px solid rgba(255,255,255,0.12);
    }

    [data-testid="stMetric"] {
        background: rgba(44, 44, 46, 0.95);
        border: 1px solid rgba(255,255,255,0.10);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #f5f5f7 !important;
    }

    [data-testid="stTabs"] button,
    [data-testid="stTabs"] button p {
        color: #f5f5f7 !important;
    }
}
</style>
""", unsafe_allow_html=True)


try:
    API_KEY = st.secrets["TWELVE_DATA_API_KEY"]
except Exception:
    API_KEY = ""

if not API_KEY:
    st.error("Lipsește TWELVE_DATA_API_KEY. Pune cheia în Streamlit Cloud → Settings → Secrets.")
    st.stop()

td = TDClient(apikey=API_KEY)


pies = {
    "Alex PIE OT": {
        "symbols": [
            "LIN", "AMZN", "JPM", "PLD", "WMT",
            "LLY", "NEE", "META", "XOM", "MSFT"
        ],
        "investments": [
            {"date": "2024-07-22", "amount": 374.21},
            {"date": "2026-04-28", "amount": 74.70},
            {"date": "2026-05-22", "amount": 59.83}
        ],
        "cash_flows": [
            {"date": "2025-03-12", "type": "Taxă PIEs", "amount": -3.00},

            {"date": "2025-09-02", "type": "Dividend WMT", "amount": 0.11},
            {"date": "2025-09-10", "type": "Dividend XOM", "amount": 0.29},
            {"date": "2025-09-10", "type": "Dividend LLY", "amount": 0.05},
            {"date": "2025-09-11", "type": "Dividend MSFT", "amount": 0.06},
            {"date": "2025-09-15", "type": "Dividend NEE", "amount": 0.26},
            {"date": "2025-09-18", "type": "Dividend LIN", "amount": 0.12},
            {"date": "2025-09-29", "type": "Dividend META", "amount": 0.04},
            {"date": "2025-09-30", "type": "Dividend PLD", "amount": 0.27},
            {"date": "2025-10-31", "type": "Dividend JPM", "amount": 0.24},

            {"date": "2025-12-10", "type": "Dividend XOM", "amount": 0.30},
            {"date": "2025-12-10", "type": "Dividend LLY", "amount": 0.05},
            {"date": "2025-12-11", "type": "Dividend MSFT", "amount": 0.07},
            {"date": "2025-12-15", "type": "Dividend NEE", "amount": 0.26},
            {"date": "2025-12-17", "type": "Dividend LIN", "amount": 0.12},
            {"date": "2025-12-23", "type": "Dividend META", "amount": 0.04},
            {"date": "2025-12-31", "type": "Dividend PLD", "amount": 0.27},

            {"date": "2026-01-05", "type": "Dividend WMT", "amount": 0.11},
            {"date": "2026-02-02", "type": "Dividend JPM", "amount": 0.24},

            {"date": "2026-03-10", "type": "Dividend XOM", "amount": 0.30},
            {"date": "2026-03-10", "type": "Dividend LLY", "amount": 0.06},
            {"date": "2026-03-12", "type": "Dividend MSFT", "amount": 0.07},
            {"date": "2026-03-16", "type": "Dividend NEE", "amount": 0.29},
            {"date": "2026-03-26", "type": "Dividend LIN", "amount": 0.12},
            {"date": "2026-03-26", "type": "Dividend META", "amount": 0.04},
            {"date": "2026-03-31", "type": "Dividend PLD", "amount": 0.29},

            {"date": "2026-04-07", "type": "Dividend WMT", "amount": 0.12},
            {"date": "2026-04-30", "type": "Dividend JPM", "amount": 0.24}
        ]
    },

    "Alex Pie20": {
        "symbols": [
            "NVDA", "AAPL", "AMZN", "META", "COST",
            "WMT", "BRK.B", "JPM", "V", "MA",
            "LLY", "JNJ", "CAT", "GOOGL", "AVGO",
            "XOM", "MSFT", "TSLA", "ORCL", "HD"
        ],
        "investments": [
            {"date": "2026-05-19", "amount": 1100.00}
        ],
        "cash_flows": []
    },

    "AI TECH": {
        "symbols": [
            "AMD", "MRVL", "NTNX", "SMCI", "TSM",
            "INTC", "MU", "SNDK", "ON", "ASML",
            "AVGO", "AMAT", "SNPS", "CDNS"
        ],
        "investments": [
            {"date": "2026-05-22", "amount": 1100.00}
        ],
        "cash_flows": []
    }
}


@st.cache_data(ttl=900)
def get_historical_price(symbol, date):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=10)

    try:
        ts = td.time_series(
            symbol=symbol,
            interval="1day",
            start_date=start.strftime("%Y-%m-%d"),
            end_date=end.strftime("%Y-%m-%d"),
            outputsize=30
        )

        df = ts.as_pandas()

        if df is None or df.empty:
            return None

        df = df.sort_index()

        return float(df["close"].iloc[0])

    except Exception:
        return None


@st.cache_data(ttl=900)
def get_current_price(symbol):
    try:
        ts = td.time_series(
            symbol=symbol,
            interval="1day",
            outputsize=5
        )

        df = ts.as_pandas()

        if df is None or df.empty:
            return None

        df = df.sort_index()

        return float(df["close"].iloc[-1])

    except Exception:
        return None


def format_money(value):
    return f"${value:,.2f}"


def format_percent(value):
    return f"{value:.2f}%"


def color_number(value):
    if value > 0:
        return "color: #00a651; font-weight: 800"
    elif value < 0:
        return "color: #ff3b30; font-weight: 800"
    return "color: #8e8e93; font-weight: 700"


st.markdown('<div class="main-title">Investimental Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Dashboard cu Twelve Data, pai-uri, profit/pierdere, dividende și taxe.</div>',
    unsafe_allow_html=True
)


tabs = st.tabs(["📌 Overview", "Alex PIE OT", "Alex Pie20", "AI TECH"])

portfolio_rows = []
pie_results = {}

grand_total_invested = 0
grand_total_value = 0

for pie_name, pie in pies.items():
    total_invested = 0
    total_stock_value = 0
    rows = []
    investment_summaries = []

    cash_flows = pie.get("cash_flows", [])
    cash_total = sum(item["amount"] for item in cash_flows)
    dividends_total = sum(item["amount"] for item in cash_flows if item["amount"] > 0)
    fees_total = sum(item["amount"] for item in cash_flows if item["amount"] < 0)

    for investment in pie["investments"]:
        date = investment["date"]
        amount = investment["amount"]
        symbols = pie["symbols"]
        amount_per_stock = amount / len(symbols)

        investment_current_value = 0

        for symbol in symbols:
            buy_price = get_historical_price(symbol, date)
            current_price = get_current_price(symbol)

            if buy_price is None or current_price is None:
                rows.append({
                    "Data": date,
                    "Symbol": symbol,
                    "Investit": round(amount_per_stock, 2),
                    "Buy": 0,
                    "Now": 0,
                    "Valoare": 0,
                    "P/L": 0,
                    "%": 0,
                    "Status": "Eroare"
                })
                continue

            shares = amount_per_stock / buy_price
            current_value = shares * current_price
            profit_loss = current_value - amount_per_stock
            percent = (profit_loss / amount_per_stock) * 100

            total_invested += amount_per_stock
            total_stock_value += current_value
            investment_current_value += current_value

            rows.append({
                "Data": date,
                "Symbol": symbol,
                "Investit": round(amount_per_stock, 2),
                "Buy": round(buy_price, 2),
                "Now": round(current_price, 2),
                "Valoare": round(current_value, 2),
                "P/L": round(profit_loss, 2),
                "%": round(percent, 2),
                "Status": "OK"
            })

        investment_profit = investment_current_value - amount
        investment_percent = (investment_profit / amount) * 100 if amount else 0

        investment_summaries.append({
            "date": date,
            "amount": amount,
            "current_value": investment_current_value,
            "profit": investment_profit,
            "percent": investment_percent
        })

    total_value = total_stock_value + cash_total
    total_profit = total_value - total_invested
    total_percent = (total_profit / total_invested) * 100 if total_invested else 0

    grand_total_invested += total_invested
    grand_total_value += total_value

    portfolio_rows.append({
        "Pai": pie_name,
        "Investit": round(total_invested, 2),
        "Valoare acțiuni": round(total_stock_value, 2),
        "Dividende/Taxe": round(cash_total, 2),
        "Valoare totală": round(total_value, 2),
        "Profit/Pierdere": round(total_profit, 2),
        "Procent %": round(total_percent, 2)
    })

    pie_results[pie_name] = {
        "total_invested": total_invested,
        "total_stock_value": total_stock_value,
        "cash_total": cash_total,
        "dividends_total": dividends_total,
        "fees_total": fees_total,
        "total_value": total_value,
        "total_profit": total_profit,
        "total_percent": total_percent,
        "rows": rows,
        "investment_summaries": investment_summaries,
        "cash_flows": cash_flows
    }


with tabs[0]:
    grand_profit = grand_total_value - grand_total_invested
    grand_percent = (grand_profit / grand_total_invested) * 100 if grand_total_invested else 0

    st.markdown('<div class="apple-card">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total investit", format_money(grand_total_invested))
    col2.metric("Valoare totală", format_money(grand_total_value))
    col3.metric("Profit/Pierdere", format_money(grand_profit), delta=format_money(grand_profit))
    col4.metric("Procent total", format_percent(grand_percent), delta=format_percent(grand_percent))

    st.markdown('</div>', unsafe_allow_html=True)

    overview_df = pd.DataFrame(portfolio_rows)

    styled = overview_df.style.map(color_number, subset=["Profit/Pierdere"]).map(color_number, subset=["Procent %"])

    st.dataframe(styled, use_container_width=True, hide_index=True)

    chart_df = overview_df[["Pai", "Profit/Pierdere"]].set_index("Pai")
    st.bar_chart(chart_df, use_container_width=True)


for index, pie_name in enumerate(["Alex PIE OT", "Alex Pie20", "AI TECH"], start=1):
    with tabs[index]:
        result = pie_results[pie_name]

        st.markdown('<div class="apple-card">', unsafe_allow_html=True)

        st.subheader(pie_name)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total investit", format_money(result["total_invested"]))
        col2.metric("Valoare totală", format_money(result["total_value"]))
        col3.metric("Profit/Pierdere", format_money(result["total_profit"]), delta=format_money(result["total_profit"]))
        col4.metric("Procent total", format_percent(result["total_percent"]), delta=format_percent(result["total_percent"]))

        st.markdown('</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Valoare acțiuni", format_money(result["total_stock_value"]))
        c2.metric("Dividende", format_money(result["dividends_total"]))
        c3.metric("Taxe", format_money(result["fees_total"]))

        for summary in result["investment_summaries"]:
            st.subheader(f"Investiție {summary['date']}")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Investit", format_money(summary["amount"]))
            c2.metric("Valoare actuală", format_money(summary["current_value"]))
            c3.metric("Profit/Pierdere", format_money(summary["profit"]), delta=format_money(summary["profit"]))
            c4.metric("Procent", format_percent(summary["percent"]), delta=format_percent(summary["percent"]))

        df = pd.DataFrame(result["rows"])
        styled_df = df.style.map(color_number, subset=["P/L"]).map(color_number, subset=["%"])

        st.dataframe(styled_df, use_container_width=True, hide_index=True)

        if result["cash_flows"]:
            st.subheader("Dividende și taxe")
            cash_df = pd.DataFrame(result["cash_flows"])
            st.dataframe(cash_df, use_container_width=True, hide_index=True)

        chart_df = df[["Symbol", "P/L"]].groupby("Symbol").sum()
        st.bar_chart(chart_df, use_container_width=True)
