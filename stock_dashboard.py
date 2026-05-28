import streamlit as st
import yfinance as yf
from datetime import date

st.set_page_config(page_title="Stock Live Dashboard", layout="wide", page_icon="📈")

st.markdown("""
<style>
    .main > div {
        padding-top: 1.2rem;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #0b3b2e 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 26px 28px;
        margin-bottom: 18px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.22);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: white;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 0.98rem;
    }

    .summary-card {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.16);
        margin-bottom: 8px;
    }

    .summary-label {
        color: #94a3b8;
        font-size: 0.84rem;
        margin-bottom: 8px;
    }

    .summary-value {
        color: white;
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .summary-delta-pos {
        color: #22c55e;
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 600;
    }

    .summary-delta-neg {
        color: #ef4444;
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 600;
    }

    .section-box {
        background: linear-gradient(180deg, rgba(15,23,42,0.92) 0%, rgba(17,24,39,0.92) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 18px 18px 8px 18px;
        margin-bottom: 18px;
        box-shadow: 0 14px 28px rgba(0,0,0,0.14);
    }

    .section-title {
        color: white;
        font-size: 1.18rem;
        font-weight: 750;
        margin-bottom: 12px;
    }

    .mini-note {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: -2px;
        margin-bottom: 14px;
    }

    .legend-card {
        background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 14px 8px 14px;
        margin-top: 10px;
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 14px 14px 10px 14px;
        border-radius: 16px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.12);
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1;
    }

    div[data-testid="stMetricValue"] {
        color: white;
        font-weight: 800;
    }

    div[data-testid="stMetricDelta"] {
        font-weight: 700;
    }

    .info-strip {
        background: rgba(30, 64, 175, 0.16);
        border: 1px solid rgba(59,130,246,0.30);
        color: #dbeafe;
        border-radius: 14px;
        padding: 10px 12px;
        margin: 10px 0 8px 0;
        font-size: 0.92rem;
    }

    .footer-note {
        color: #94a3b8;
        font-size: 0.84rem;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">📊 Prețuri LIVE - Dashboard Personal</div>
    <div class="hero-subtitle">
        Monitorizare portofoliu, alocare pe zone, cash neinvestit și performanță pe fiecare poziție.
    </div>
</div>
""", unsafe_allow_html=True)

PORTFOLIOS = [
    {
        "name": "🤖 AI TECH",
        "tickers": [
            "AMAT", "MU", "MSTR", "AMD", "MRVL", "ASML", "TSM",
            "SNPS", "SNDK", "NTNX", "INTC", "AVGO", "CDNS", "ON"
        ],
        "buy_date": date(2026, 5, 27),
        "amount_per_stock": 78.44,
        "cash_additions": [],
    },
    {
        "name": "💰 PIE OT Investimental",
        "tickers": [
            "LIN", "XOM", "PLD", "NEE", "MSFT",
            "AMZN", "WMT", "META", "JPM", "LLY"
        ],
        "buy_date": date(2024, 7, 22),
        "amount_per_stock": 37.33,
        "cash_additions": [
            {"date": date(2026, 4, 28), "amount": 74.70},
            {"date": date(2026, 5, 22), "amount": 59.83},
        ],
    },
    {
        "name": "📈 Alex PIE 20 (19 Mai 2026)",
        "tickers": [
            "COST", "V", "ORCL", "JNJ", "HD", "XOM", "CAT", "MSFT", "WMT", "MA",
            "AMZN", "GOOG", "BRK-B", "NVDA", "TSLA", "JPM", "LLY", "META", "AVGO", "AAPL"
        ],
        "buy_date": date(2026, 5, 19),
        "amount_per_stock": 54.91,
        "cash_additions": [],
    },
]

st.sidebar.header("⚙️ Setări")
if st.sidebar.button("🔄 Refresh Manual", use_container_width=True):
    st.rerun()


def load_history(ticker: str):
    history = yf.Ticker(ticker).history(period="5y", auto_adjust=False)
    if history.empty:
        return history
    return history[["Close"]].dropna()


def get_price_on_or_before(history, target_date: date):
    rows = history[history.index.date <= target_date]
    if rows.empty:
        return None
    return float(rows["Close"].iloc[-1])


def get_ticker_data(ticker: str, buy_date: date):
    try:
        history = load_history(ticker)
        if history.empty:
            return None, "Nu există istoric pentru acest ticker."

        current_price = float(history["Close"].iloc[-1])
        buy_price = get_price_on_or_before(history, buy_date)

        if buy_price is None:
            return None, f"Nu există preț disponibil pentru data {buy_date:%d.%m.%Y}."

        return {
            "price": current_price,
            "buy_price": buy_price,
        }, None

    except Exception as e:
        return None, str(e)


def format_cash_additions(cash_additions):
    if not cash_additions:
        return "Fără cash suplimentar"
    return " + ".join(
        f"${item['amount']:.2f} din {item['date']:%d.%m.%Y}"
        for item in cash_additions
    )


portfolio_totals = []
total_cash_global = 0.0
all_profit_loss = []
best_position = None
worst_position = None
global_total_now = 0.0
global_total_in = 0.0

portfolio_results = []

for portfolio in PORTFOLIOS:
    buy_date = portfolio["buy_date"]
    tickers = portfolio["tickers"]
    amount_per_stock = portfolio["amount_per_stock"]
    cash_additions = portfolio["cash_additions"]

    invested_total = amount_per_stock * len(tickers)
    cash_total = sum(item["amount"] for item in cash_additions)

    positions = []
    failed_tickers = []
    total_positions_value = 0.0

    for ticker in tickers:
        data, error = get_ticker_data(ticker, buy_date)

        if error:
            failed_tickers.append(f"{ticker}: {error}")
            continue

        current_value = amount_per_stock * (data["price"] / data["buy_price"])
        profit_loss = current_value - amount_per_stock
        return_pct = (profit_loss / amount_per_stock) * 100 if amount_per_stock else 0

        position = {
            "ticker": ticker,
            "price": data["price"],
            "buy_price": data["buy_price"],
            "invested": amount_per_stock,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "return_pct": return_pct,
            "portfolio": portfolio["name"],
        }
        positions.append(position)

        total_positions_value += current_value
        all_profit_loss.append(position)

        if best_position is None or return_pct > best_position["return_pct"]:
            best_position = position

        if worst_position is None or return_pct < worst_position["return_pct"]:
            worst_position = position

    portfolio_total_now = total_positions_value + cash_total
    portfolio_total_in = invested_total + cash_total
    total_change_pct = (
        (portfolio_total_now - portfolio_total_in) / portfolio_total_in * 100
        if portfolio_total_in else 0
    )

    portfolio_totals.append({
        "Categorie": portfolio["name"],
        "Valoare": total_positions_value
    })
    total_cash_global += cash_total
    global_total_now += portfolio_total_now
    global_total_in += portfolio_total_in

    portfolio_results.append({
        "name": portfolio["name"],
        "buy_date": buy_date,
        "tickers": tickers,
        "amount_per_stock": amount_per_stock,
        "cash_additions": cash_additions,
        "invested_total": invested_total,
        "cash_total": cash_total,
        "positions": positions,
        "failed_tickers": failed_tickers,
        "total_positions_value": total_positions_value,
        "portfolio_total_now": portfolio_total_now,
        "portfolio_total_in": portfolio_total_in,
        "total_change_pct": total_change_pct,
    })

global_profit = global_total_now - global_total_in
global_profit_pct = (global_profit / global_total_in * 100) if global_total_in else 0

top1, top2, top3, top4 = st.columns(4)

with top1:
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-label">Valoare totală</div>
        <div class="summary-value">${global_total_now:,.2f}</div>
        <div class="{'summary-delta-pos' if global_profit >= 0 else 'summary-delta-neg'}">
            {'+' if global_profit >= 0 else ''}${global_profit:,.2f} ({global_profit_pct:.2f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-label">Capital total introdus</div>
        <div class="summary-value">${global_total_in:,.2f}</div>
        <div class="summary-label">Investit + cash neinvestit</div>
    </div>
    """, unsafe_allow_html=True)

with top3:
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-label">Cash total</div>
        <div class="summary-value">${total_cash_global:,.2f}</div>
        <div class="summary-label">Fără profit/pierdere</div>
    </div>
    """, unsafe_allow_html=True)

with top4:
    best_text = "N/A" if best_position is None else f"{best_position['ticker']} ({best_position['return_pct']:.2f}%)"
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-label">Best performer</div>
        <div class="summary-value" style="font-size:1.25rem;">{best_text}</div>
        <div class="summary-label">Cea mai bună poziție din toate PIE-urile</div>
    </div>
    """, unsafe_allow_html=True)

for result in portfolio_results:
    st.markdown(f"""
    <div class="section-box">
        <div class="section-title">{result['name']}</div>
        <div class="mini-note">
            Investit inițial: ${result['invested_total']:.2f} din {result['buy_date']:%d.%m.%Y}
            {'| Cash neinvestit: $' + format(result['cash_total'], ',.2f') if result['cash_total'] else ''}
        </div>
    """, unsafe_allow_html=True)

    target_weight = 100 / len(result["tickers"]) if result["tickers"] else 0
    cols = st.columns(4)

    for i, position in enumerate(result["positions"]):
        current_weight = (
            position["current_value"] / result["total_positions_value"] * 100
            if result["total_positions_value"] else 0
        )
        emoji = "🟢" if position["return_pct"] >= 0 else "🔴"

        with cols[i % 4]:
            st.metric(
                label=f"**{position['ticker']}**",
                value=f"${position['price']:.2f}",
                delta=f"{emoji} {position['return_pct']:.2f}%"
            )
            st.caption(f"Țintă: {target_weight:.2f}% | Acum: {current_weight:.2f}%")
            st.caption(
                f"P/L: ${position['profit_loss']:+.2f} | "
                f"${position['invested']:.2f} → ${position['current_value']:.2f}"
            )

    status_emoji = "🟢" if result["total_change_pct"] >= 0 else "🔴"
    st.markdown(
        f"""
        <div class="info-strip">
            <b>Total {result['name']}</b>: {status_emoji}
            {result['total_change_pct']:.2f}% |
            ${result['portfolio_total_in']:,.2f} → ${result['portfolio_total_now']:,.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    if result["cash_additions"]:
        st.caption(f"Alimentări cash: {format_cash_additions(result['cash_additions'])}")

    if result["failed_tickers"]:
        st.warning("Nu s-au putut încărca toate simbolurile:")
        for message in result["failed_tickers"]:
            st.write(f"- {message}")

    st.markdown("</div>", unsafe_allow_html=True)

if total_cash_global > 0:
    portfolio_totals.append({
        "Categorie": "💵 Cash",
        "Valoare": total_cash_global
    })

st.sidebar.markdown("## Distribuție totală")

if portfolio_totals:
    total_value_for_chart = sum(item["Valoare"] for item in portfolio_totals)

    colors = ["#22c55e", "#3b82f6", "#f59e0b", "#94a3b8", "#ef4444", "#06b6d4"]

    segments = []
    legend_html = ""
    current_angle = 0

    for i, item in enumerate(portfolio_totals):
        value = item["Valoare"]
        label = item["Categorie"]
        color = colors[i % len(colors)]
        pct = (value / total_value_for_chart * 100) if total_value_for_chart else 0
        angle = pct * 3.6

        segments.append(
            f"{color} {current_angle:.2f}deg {current_angle + angle:.2f}deg"
        )

        legend_html += f"""
        <div style="display:flex; align-items:center; margin-bottom:8px;">
            <div style="width:12px; height:12px; background:{color}; border-radius:3px; margin-right:8px;"></div>
            <div style="font-size:13px; color:#e5e7eb;">
                {label}<br>
                <span style="color:#94a3b8;">${value:,.2f} ({pct:.1f}%)</span>
            </div>
        </div>
        """

        current_angle += angle

    donut_style = ", ".join(segments)

    st.sidebar.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin: 12px 0 18px 0;">
            <div style="
                width:220px;
                height:220px;
                border-radius:50%;
                background: conic-gradient({donut_style});
                position:relative;
                box-shadow: 0 14px 30px rgba(0,0,0,0.22);
            ">
                <div style="
                    position:absolute;
                    top:50%;
                    left:50%;
                    transform:translate(-50%, -50%);
                    width:112px;
                    height:112px;
                    background:#0f172a;
                    border:1px solid rgba(255,255,255,0.08);
                    border-radius:50%;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    flex-direction:column;
                    color:white;
                    text-align:center;
                    font-size:12px;
                ">
                    <div style="color:#94a3b8;">Total</div>
                    <div style="font-size:16px; font-weight:800;">${total_value_for_chart:,.0f}</div>
                </div>
            </div>
        </div>
        <div class="legend-card">
            {legend_html}
        </div>
        """,
        unsafe_allow_html=True
    )

st.sidebar.markdown("---")
if best_position:
    st.sidebar.markdown(
        f"""
        <div class="legend-card">
            <div style="color:white; font-weight:700; margin-bottom:6px;">Top performer</div>
            <div style="color:#22c55e; font-size:14px; font-weight:700;">
                {best_position['ticker']} +{best_position['return_pct']:.2f}%
            </div>
            <div style="color:#94a3b8; font-size:12px;">{best_position['portfolio']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if worst_position:
    st.sidebar.markdown(
        f"""
        <div class="legend-card">
            <div style="color:white; font-weight:700; margin-bottom:6px;">Weakest performer</div>
            <div style="color:#ef4444; font-size:14px; font-weight:700;">
                {worst_position['ticker']} {worst_position['return_pct']:.2f}%
            </div>
            <div style="color:#94a3b8; font-size:12px;">{worst_position['portfolio']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '<div class="footer-note">Date de la Yahoo Finance • Cash-ul suplimentar este tratat separat, fără profit</div>',
    unsafe_allow_html=True
)
