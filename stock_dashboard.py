import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Investimental Dashboard", layout="wide")

st.title("📊 Dashboard Investimental - Alex")

pies = {
    "Alex Pai OT": {
        "symbols": ["LIN", "AMZN", "JPM", "PLD", "WMT", "LLY", "NEE", "META", "XOM", "MSFT"],
        "investments": [
            {"date": "2024-07-22", "amount": 374.21},
            {"date": "2026-04-28", "amount": 74.07},
            {"date": "2026-05-22", "amount": 59.83}
        ]
    },
    "Alex Pai 20": {
        "symbols": ["NVDA", "AAPL", "AMZN", "META", "COST", "WMT", "BRK-B", "JPM", "V", "MA", "LLY", "JNJ", "CAT", "GOOGL", "AVGO", "XOM", "MSFT", "TSLA", "ORCL", "HD"],
        "investments": [
            {"date": "2026-04-28", "amount": 1100.00}
        ]
    },
    "AiTech": {
        "symbols": ["AMD", "MRVL", "NTNX", "SMCI", "TSM", "INTC", "MU", "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"],
        "investments": [
            {"date": "2026-05-22", "amount": 1100.00}
        ]
    }
}

@st.cache_data(ttl=300)
def get_price_on_or_after(symbol, date):
    start = datetime.strptime(date, "%Y-%m-%d")
    end = start + timedelta(days=7)

    data = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)

    if data.empty:
        return None

    return data["Close"].iloc[0].item()

@st.cache_data(ttl=300)
def get_current_price(symbol):
    data = yf.download(symbol, period="5d", progress=False, auto_adjust=True)

    if data.empty:
        return None

    return data["Close"].iloc[-1].item()

for pie_name, pie in pies.items():
    st.header(pie_name)

    total_invested = 0
    total_current_value = 0
    all_rows = []

    for investment in pie["investments"]:
        date = investment["date"]
        amount = investment["amount"]
        amount_per_stock = amount / len(pie["symbols"])

        investment_current_value = 0

        for symbol in pie["symbols"]:
            buy_price = get_price_on_or_after(symbol, date)
            current_price = get_current_price(symbol)

            if buy_price is None or current_price is None:
                continue

            shares = amount_per_stock / buy_price
            current_value = shares * current_price
            profit_loss = current_value - amount_per_stock
            percent_change = (profit_loss / amount_per_stock) * 100

            investment_current_value += current_value
            total_invested += amount_per_stock
            total_current_value += current_value

            all_rows.append({
                "Data investiției": date,
                "Symbol": symbol,
                "Investit": round(amount_per_stock, 2),
                "Preț cumpărare": round(buy_price, 2),
                "Preț actual": round(current_price, 2),
                "Valoare actuală": round(current_value, 2),
                "Profit/Pierdere": round(profit_loss, 2),
                "Procent %": round(percent_change, 2)
            })

        investment_profit_loss = investment_current_value - amount
        investment_percent = (investment_profit_loss / amount) * 100

        st.subheader(f"Investiție {date}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Investit", f"${amount:.2f}")
        col2.metric("Valoare actuală", f"${investment_current_value:.2f}")
        col3.metric("Profit/Pierdere", f"${investment_profit_loss:.2f}")
        col4.metric("Procent", f"{investment_percent:.2f}%")

    total_profit_loss = total_current_value - total_invested
    total_percent = (total_profit_loss / total_invested) * 100

    st.subheader("Total Pai")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total investit", f"${total_invested:.2f}")
    col2.metric("Valoare actuală", f"${total_current_value:.2f}")
    col3.metric("Profit/Pierdere", f"${total_profit_loss:.2f}")
    col4.metric("Procent total", f"{total_percent:.2f}%")

    df = pd.DataFrame(all_rows)
    st.dataframe(df, use_container_width=True)

    st.divider()
