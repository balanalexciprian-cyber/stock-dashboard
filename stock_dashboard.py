import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="Stock Live Dashboard",
    layout="wide",
    page_icon="📈"
)

st.title("📊 Dashboard Investiții - Alex Balan")

# =========================
# GRUPE / PORTOFOLII
# =========================

groups = {
    "🤖 AI TECH": {
        "tickers": [
            "AMD", "MRVL", "NTNX", "SMCI", "TSM", "INTC", "MU",
            "SNDK", "ON", "ASML", "AVGO", "AMAT", "SNPS", "CDNS"
        ],
        "start_date": "2026-05-27",
        "initial_amount": 1100
    },

    "💰 Alex Pai OT": {
        "tickers": [
            "LIN", "AMZN", "JPM", "PLD", "WMT", "LLY",
            "NEE", "META", "XOM", "MSFT"
        ],
        "start_date": "2024-07-22",
        "initial_amount": 374.21 + 74.70 + 59.83
    },

    "📊 Alex Pai 20": {
        "tickers": [
            "NVDA", "AAPL", "AMZN", "META", "COST", "WMT",
            "BRK-B", "JPM", "V", "MA", "LLY", "JNJ",
            "CAT", "GOOGL", "AVGO", "XOM", "MSFT",
            "TSLA", "ORCL", "HD"
        ],
        "start_date": "2026-05-19",
        "initial_amount": 1100
    }
}

# =========================
# FUNCȚII
# =========================

@st.cache_data(ttl=900)
def get_price_data(tickers, start_date):
    """
    Ia prețurile de la Yahoo Finance.
    ttl=900 înseamnă refresh cam la 15 minute.
    """

    end_date = date.today() + timedelta(days=1)

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=True,
        group_by="ticker"
    )

    return data


def extract_close_prices(data, tickers):
    """
    Scoate prețurile Close pentru fiecare ticker.
    Funcționează și pentru un singur ticker, și pentru mai multe.
    """

    close_prices = pd.DataFrame()

    for ticker in tickers:
        try:
            if len(tickers) == 1:
                close_prices[ticker] = data["Close"]
            else:
                close_prices[ticker] = data[ticker]["Close"]
        except Exception:
            close_prices[ticker] = None

    close_prices = close_prices.dropna(how="all")
    return close_prices


def calculate_portfolio(close_prices, initial_amount):
    """
    Presupune că suma inițială este împărțită egal între acțiuni.
    Calculează evoluția portofoliului de la prima zi disponibilă.
    """

    valid_tickers = close_prices.columns.dropna()
    number_of_stocks = len(valid_tickers)

    if number_of_stocks == 0 or close_prices.empty:
        return None, None

    amount_per_stock = initial_amount / number_of_stocks

    first_prices = close_prices.iloc[0]
    shares = amount_per_stock / first_prices

    portfolio_values = close_prices * shares
    total_portfolio = portfolio_values.sum(axis=1)

    return total_portfolio, shares


# =========================
# UI
# =========================

selected_group_name = st.sidebar.selectbox(
    "Alege portofoliul:",
    list(groups.keys())
)

selected_group = groups[selected_group_name]

tickers = selected_group["tickers"]
start_date = selected_group["start_date"]
initial_amount = selected_group["initial_amount"]

st.sidebar.write("### Detalii portofoliu")
st.sidebar.write(f"Data de start: **{start_date}**")
st.sidebar.write(f"Suma inițială: **${initial_amount:,.2f}**")
st.sidebar.write(f"Număr acțiuni: **{len(tickers)}**")

st.subheader(selected_group_name)

st.write(
    f"Calculul pentru acest portofoliu începe din **{start_date}** "
    f"și presupune împărțirea egală a sumei de **${initial_amount:,.2f}** "
    f"între acțiunile din listă."
)

# =========================
# DATE
# =========================

data = get_price_data(tickers, start_date)
close_prices = extract_close_prices(data, tickers)

if close_prices.empty:
    st.error("Nu s-au putut încărca datele pentru acest portofoliu.")
    st.stop()

total_portfolio, shares = calculate_portfolio(close_prices, initial_amount)

if total_portfolio is None:
    st.error("Nu s-a putut calcula portofoliul.")
    st.stop()

# =========================
# REZULTATE
# =========================

start_value = total_portfolio.iloc[0]
current_value = total_portfolio.iloc[-1]
profit_loss = current_value - start_value
profit_loss_percent = (profit_loss / start_value) * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric("Valoare inițială", f"${start_value:,.2f}")
col2.metric("Valoare actuală", f"${current_value:,.2f}")
col3.metric("Profit / Pierdere", f"${profit_loss:,.2f}")
col4.metric("Performanță", f"{profit_loss_percent:.2f}%")

st.divider()

# =========================
# GRAFIC PORTOFOLIU
# =========================

st.write("### Evoluția portofoliului")

chart_data = total_portfolio.rename("Valoare portofoliu")
st.line_chart(chart_data)

# =========================
# TABEL ACȚIUNI
# =========================

st.write("### Performanță pe fiecare acțiune")

table_rows = []

for ticker in close_prices.columns:
    try:
        start_price = close_prices[ticker].iloc[0]
        current_price = close_prices[ticker].iloc[-1]
        change = current_price - start_price
        change_percent = (change / start_price) * 100

        table_rows.append({
            "Ticker": ticker,
            "Preț start": round(start_price, 2),
            "Preț actual": round(current_price, 2),
            "Diferență $": round(change, 2),
            "Diferență %": round(change_percent, 2),
            "Acțiuni estimate": round(shares[ticker], 6)
        })
    except Exception:
        pass

performance_df = pd.DataFrame(table_rows)

st.dataframe(
    performance_df,
    use_container_width=True,
    hide_index=True
)

# =========================
# LISTĂ TICKERE
# =========================

with st.expander("Vezi tickerele din acest portofoliu"):
    st.write(", ".join(tickers))

st.caption(
    "Datele sunt luate prin yfinance/Yahoo Finance și pot avea întârziere sau mici diferențe față de broker."
)
