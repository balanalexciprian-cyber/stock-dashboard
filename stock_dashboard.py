import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Investimental Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f5f5f7 0%, #ffffff 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #111111;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 16px;
    color: #6e6e73;
    margin-bottom: 28px;
}

.apple-card {
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 28px;
    padding: 24px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.07);
    backdrop-filter: blur(18px);
    margin-bottom: 22px;
}

.pie-title {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.8px;
    color: #111111;
    margin-bottom: 6px;
}

.pie-subtitle {
    font-size: 14px;
    color: #6e6e73;
    margin-bottom: 18px;
}

.investment-title {
    font-size: 20px;
    font-weight: 700;
    color: #111111;
    margin-top: 14px;
    margin-bottom: 12px;
}

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.06);
    border-radius: 22px;
    padding: 18px 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

[data-testid="stMetricLabel"] {
    color: #6e6e73;
    font-size: 13px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #111111;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.8px;
}

[data-testid="stMetricDelta"] {
    font-size: 14px;
    font-weight: 700;
}

.stDataFrame {
    border-radius: 22px;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
}

hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

@media screen and (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.2rem;
    }

    .main-title {
        font-size: 31px;
        line-height: 1.05;
    }

    .subtitle {
        font-size: 14px;
        margin-bottom: 18px;
    }

    .apple-card {
        padding: 18px;
        border-radius: 24px;
    }

    .pie-title {
        font-size: 23px;
    }

    [data-testid="stMetric"] {
        padding: 14px;
        border-radius: 18px;
    }

    [data-testid="stMetricValue"] {
        font-size: 22px;
    }
}
</style>
""", unsafe_allow_html=True)


pies = {
    "Alex Pai OT": {
        "symbols": [
            "LIN", "AMZN", "JPM", "PLD", "WMT",
            "LLY", "NEE", "META", "XOM", "MSFT"
        ],
        "investments": [
            {"date": "2024-07-22", "amount": 374.21},
            {"date": "2026-04-28", "amount": 74.07},
            {"date": "2026-05-22", "amount": 59.83}
        ]
    },

    "Alex Pai 20": {
        "symbols": [
            "NVDA", "AAPL", "AMZN", "META", "COST",
            "WMT", "BRK-B", "JPM", "V", "MA",
            "LLY", "JNJ", "CAT", "GOOGL", "AVGO",
            "XOM", "MSFT", "TSLA", "ORCL", "HD"
        ],
        "investments": [
            {"date": "2026-04-28", "amount": 1100.00}
        ]
    },

    "AiTech": {
        "symbols": [
            "AMD", "MRVL", "NTNX", "SMCI", "TSM",
            "INTC", "MU", "SNDK", "ON", "ASML",
            "AVGO", "AMAT", "SNPS", "CDNS"
        ],
        "investments": [
            {"date": "2026-05-22", "amount": 1100.00}
        ]
    }
}


@st.cache_data(ttl=600)
def get_price_on_or_after(symbol, date):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=10)

    data = yf.download(
        symbol,
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        return None

    return data["Close"].iloc[0].item()


@st.cache_data(ttl=600)
def get_current_price(symbol):
    data = yf.download(
        symbol,
        period="5d",
        progress=False,
        auto_adjust=True
    )

    if data.empty:
        return None

    return data["Close"].iloc[-1].item()


def color_profit_loss(value):
    if value > 0:
        return "color: #00a651; font-weight: 800"
    elif value < 0:
        return "color: #ff3b30; font-weight: 800"
    else:
        return "color: #8e8e93; font-weight: 700"


def color_percent(value):
    if value > 0:
        return "color: #00a651; font-weight: 800"
    elif value < 0:
        return "color: #ff3b30; font-weight: 800"
    else:
        return "color: #8e8e93; font-weight: 700"


def format_money(value):
    return f"${value:,.2f}"


def format_percent(value):
    return f"{value:.2f}%"


st.markdown('<div class="main-title">Investimental Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Portofoliul tău organizat pe pai-uri, cu profit/pierdere live și prețuri actuale.</div>', unsafe_allow_html=True)

grand_total_invested = 0
grand_total_current_value = 0

portfolio_rows = []

tabs = st.tabs(["📌 Overview", "Alex Pai OT", "Alex Pai 20", "AiTech"])

pie_results = {}

for pie_name, pie in pies.items():

    total_invested = 0
    total_current_value = 0
    all_rows = []
    investment_summaries = []

    for investment in pie["investments"]:

        date = investment["date"]
        amount = investment["amount"]
        symbols = pie["symbols"]

        amount_per_stock = amount / len(symbols)
        investment_current_value = 0
        rows_for_this_investment = []

        for symbol in symbols:

            buy_price = get_price_on_or_after(symbol, date)
            current_price = get_current_price(symbol)

            if buy_price is None or current_price is None:
                rows_for_this_investment.append({
                    "Data": date,
                    "Symbol": symbol,
                    "Investit": amount_per_stock,
                    "Buy": 0,
                    "Now": 0,
                    "Valoare": 0,
                    "P/L": 0,
                    "%": 0
                })
                continue

            shares_bought = amount_per_stock / buy_price
            current_value = shares_bought * current_price
            profit_loss = current_value - amount_per_stock
            percent_change = (profit_loss / amount_per_stock) * 100

            investment_current_value += current_value
            total_invested += amount_per_stock
            total_current_value += current_value

            rows_for_this_investment.append({
                "Data": date,
                "Symbol": symbol,
                "Investit": round(amount_per_stock, 2),
                "Buy": round(buy_price, 2),
                "Now": round(current_price, 2),
                "Valoare": round(current_value, 2),
                "P/L": round(profit_loss, 2),
                "%": round(percent_change, 2)
            })

        investment_profit_loss = investment_current_value - amount
        investment_percent = (investment_profit_loss / amount) * 100

        investment_summaries.append({
            "date": date,
            "amount": amount,
            "current_value": investment_current_value,
            "profit_loss": investment_profit_loss,
            "percent": investment_percent
        })

        all_rows.extend(rows_for_this_investment)

    total_profit_loss = total_current_value - total_invested
    total_percent = (total_profit_loss / total_invested) * 100 if total_invested else 0

    grand_total_invested += total_invested
    grand_total_current_value += total_current_value

    portfolio_rows.append({
        "Pai": pie_name,
        "Investit": round(total_invested, 2),
        "Valoare actuală": round(total_current_value, 2),
        "Profit/Pierdere": round(total_profit_loss, 2),
        "Procent %": round(total_percent, 2)
    })

    pie_results[pie_name] = {
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "total_profit_loss": total_profit_loss,
        "total_percent": total_percent,
        "rows": all_rows,
        "investment_summaries": investment_summaries
    }


with tabs[0]:
    grand_profit_loss = grand_total_current_value - grand_total_invested
    grand_percent = (grand_profit_loss / grand_total_invested) * 100 if grand_total_invested else 0

    st.markdown('<div class="apple-card">', unsafe_allow_html=True)
    st.markdown('<div class="pie-title">📌 Total General Portofoliu</div>', unsafe_allow_html=True)
    st.markdown('<div class="pie-subtitle">Rezumat complet pentru toate cele trei pai-uri.</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total investit", format_money(grand_total_invested))
    col2.metric("Valoare actuală", format_money(grand_total_current_value))
    col3.metric("Profit/Pierdere", format_money(grand_profit_loss), delta=format_money(grand_profit_loss))
    col4.metric("Procent total", format_percent(grand_percent), delta=format_percent(grand_percent))

    st.markdown('</div>', unsafe_allow_html=True)

    overview_df = pd.DataFrame(portfolio_rows)

    styled_overview = overview_df.style.map(
        color_profit_loss,
        subset=["Profit/Pierdere"]
    ).map(
        color_percent,
        subset=["Procent %"]
    )

    st.dataframe(
        styled_overview,
        use_container_width=True,
        hide_index=True
    )

    chart_df = overview_df[["Pai", "Profit/Pierdere"]].set_index("Pai")
    st.bar_chart(chart_df, use_container_width=True)


for index, pie_name in enumerate(["Alex Pai OT", "Alex Pai 20", "AiTech"], start=1):

    with tabs[index]:

        result = pie_results[pie_name]

        st.markdown('<div class="apple-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="pie-title">{pie_name}</div>', unsafe_allow_html=True)
        st.markdown('<div class="pie-subtitle">Profit, pierdere, procent și prețuri actuale pentru fiecare simbol.</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total investit", format_money(result["total_invested"]))
        col2.metric("Valoare actuală", format_money(result["total_current_value"]))
        col3.metric(
            "Profit/Pierdere",
            format_money(result["total_profit_loss"]),
            delta=format_money(result["total_profit_loss"])
        )
        col4.metric(
            "Procent total",
            format_percent(result["total_percent"]),
            delta=format_percent(result["total_percent"])
        )

        st.markdown('</div>', unsafe_allow_html=True)

        for summary in result["investment_summaries"]:

            st.markdown(
                f'<div class="investment-title">Investiție {summary["date"]}</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Investit", format_money(summary["amount"]))
            c2.metric("Valoare actuală", format_money(summary["current_value"]))
            c3.metric(
                "Profit/Pierdere",
                format_money(summary["profit_loss"]),
                delta=format_money(summary["profit_loss"])
            )
            c4.metric(
                "Procent",
                format_percent(summary["percent"]),
                delta=format_percent(summary["percent"])
            )

        df = pd.DataFrame(result["rows"])

        styled_df = df.style.map(
            color_profit_loss,
            subset=["P/L"]
        ).map(
            color_percent,
            subset=["%"]
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

        pie_chart_df = df[["Symbol", "P/L"]].groupby("Symbol").sum()
        st.bar_chart(pie_chart_df, use_container_width=True)
