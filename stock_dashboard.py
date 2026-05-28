import streamlit as st
import yfinance as yf
from datetime import date

st.set_page_config(page_title="Portfolio Tracker", layout="wide", page_icon="📈")

theme_mode = st.sidebar.selectbox("Temă", ["Light", "Dark"], index=0)

if theme_mode == "Dark":
    bg_main = "#071226"
    bg_panel = "#121c34"
    bg_card = "#1a233b"
    bg_subtle = "#101a30"
    border = "rgba(255,255,255,0.08)"
    text_main = "#f8fafc"
    text_soft = "#94a3b8"
    green = "#4ade80"
    green_bg = "rgba(74,222,128,0.16)"
    blue = "#38bdf8"
    orange = "#f59e0b"
    red = "#f87171"
    donut_center = "#0d172d"
    shadow = "0 18px 40px rgba(0,0,0,0.18)"
else:
    bg_main = "#f4f7fb"
    bg_panel = "#ffffff"
    bg_card = "#ffffff"
    bg_subtle = "#eef3f9"
    border = "rgba(15,23,42,0.08)"
    text_main = "#0f172a"
    text_soft = "#64748b"
    green = "#16a34a"
    green_bg = "rgba(22,163,74,0.10)"
    blue = "#2563eb"
    orange = "#d97706"
    red = "#dc2626"
    donut_center = "#ffffff"
    shadow = "0 16px 34px rgba(15,23,42,0.08)"

st.markdown(
    f"""
    <style>
        .stApp {{
            background: {bg_main};
        }}

        .block-container {{
            max-width: 1450px;
            padding-top: 1rem;
            padding-bottom: 2rem;
        }}

        .hero {{
            background: linear-gradient(135deg, {bg_panel} 0%, {bg_subtle} 100%);
            border: 1px solid {border};
            border-radius: 26px;
            padding: 28px;
            margin-bottom: 18px;
            box-shadow: {shadow};
        }}

        .hero-kicker {{
            color: {blue};
            font-size: 0.82rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
            font-weight: 700;
        }}

        .hero-title {{
            color: {text_main};
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1.05;
            margin-bottom: 8px;
        }}

        .hero-subtitle {{
            color: {text_soft};
            font-size: 0.98rem;
            max-width: 780px;
        }}

        .summary-card {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 22px;
            padding: 18px;
            min-height: 118px;
            box-shadow: {shadow};
        }}

        .summary-label {{
            color: {text_soft};
            font-size: 0.84rem;
            margin-bottom: 10px;
        }}

        .summary-value {{
            color: {text_main};
            font-size: 1.75rem;
            font-weight: 800;
            line-height: 1.05;
        }}

        .summary-positive {{
            color: {green};
            margin-top: 8px;
            font-size: 0.92rem;
            font-weight: 700;
        }}

        .summary-negative {{
            color: {red};
            margin-top: 8px;
            font-size: 0.92rem;
            font-weight: 700;
        }}

        .glass-card {{
            background: {bg_panel};
            border: 1px solid {border};
            border-radius: 22px;
            padding: 18px;
            box-shadow: {shadow};
        }}

        .section-title {{
            color: {text_main};
            font-size: 1.15rem;
            font-weight: 780;
            margin-bottom: 6px;
        }}

        .section-subtitle {{
            color: {text_soft};
            font-size: 0.9rem;
            margin-bottom: 14px;
        }}

        .asset-row {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }}

        .asset-name {{
            color: {text_main};
            font-size: 1rem;
            font-weight: 700;
        }}

        .asset-sub {{
            color: {text_soft};
            font-size: 0.82rem;
            margin-top: 2px;
        }}

        .pill-pos {{
            display: inline-block;
            background: {green_bg};
            color: {green};
            border: 1px solid rgba(34,197,94,0.22);
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        .pill-neg {{
            display: inline-block;
            background: rgba(239,68,68,0.10);
            color: {red};
            border: 1px solid rgba(239,68,68,0.20);
            border-radius: 999px;
            padding: 4px 10px;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        .sidebar-card {{
            background: {bg_panel};
            border: 1px solid {border};
            border-radius: 22px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: {shadow};
        }}

        .sidebar-title {{
            color: {text_main};
            font-size: 1rem;
            font-weight: 760;
            margin-bottom: 10px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}

        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 4px;
            margin-right: 8px;
            flex-shrink: 0;
        }}

        .legend-text {{
            color: {text_main};
            font-size: 13px;
            line-height: 1.3;
        }}

        .legend-sub {{
            color: {text_soft};
            font-size: 12px;
        }}

        .notice-box {{
            background: {bg_subtle};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 16px;
            color: {text_main};
            font-size: 0.94rem;
            line-height: 1.7;
        }}

        .ticker-chip {{
            background: {bg_subtle};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 8px 10px;
            text-align: center;
            font-weight: 700;
            color: {text_main};
            margin-bottom: 8px;
        }}

        div[data-testid="stMetric"] {{
            background: {bg_card};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 14px;
            box-shadow: none;
        }}

        div[data-testid="stMetricLabel"] {{
            color: {text_soft};
        }}

        div[data-testid="stMetricValue"] {{
            color: {text_main};
            font-weight: 800;
        }}

        div[data-testid="stMetricDelta"] {{
            font-weight: 700;
        }}

        details {{
            background: {bg_panel};
            border: 1px solid {border};
            border-radius: 16px;
            margin-bottom: 12px;
            box-shadow: {shadow};
        }}

        details summary {{
            color: {text_main};
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

PORTFOLIOS = [
    {
        "name": "🤖 AI TECH",
        "mode": "calculated",
        "tickers": ["AMAT", "MU", "MSTR", "AMD", "MRVL", "ASML", "TSM", "SNPS", "SNDK", "NTNX", "INTC", "AVGO", "CDNS", "ON"],
        "buy_date": date(2026, 5, 27),
        "amount_per_stock": 78.44,
        "cash_additions": [],
    },
    {
        "name": "💰 PIE OT Investimental",
        "mode": "manual_total",
        "tickers": ["LIN", "XOM", "PLD", "NEE", "MSFT", "AMZN", "WMT", "META", "JPM", "LLY"],
        "invested_now": 480.84,
        "cash_now": 141.98,
        "total_now": 622.82,
        "note": "PIE OT folosește valorile reale din aplicație. Când cash-ul va fi investit, actualizezi manual aceste valori.",
    },
    {
        "name": "📈 Alex PIE 20",
        "mode": "calculated",
        "tickers": ["COST", "V", "ORCL", "JNJ", "HD", "XOM", "CAT", "MSFT", "WMT", "MA", "AMZN", "GOOG", "BRK-B", "NVDA", "TSLA", "JPM", "LLY", "META", "AVGO", "AAPL"],
        "buy_date": date(2026, 5, 19),
        "amount_per_stock": 54.91,
        "cash_additions": [],
    },
]

st.sidebar.markdown('<div class="sidebar-title">Control Panel</div>', unsafe_allow_html=True)
if st.sidebar.button("Refresh Manual", use_container_width=True):
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
            return None, "Fără istoric"
        current_price = float(history["Close"].iloc[-1])
        buy_price = get_price_on_or_before(history, buy_date)
        if buy_price is None:
            return None, "Fără preț la data cumpărării"
        return {"price": current_price, "buy_price": buy_price}, None
    except Exception as e:
        return None, str(e)


portfolio_totals = []
portfolio_results = []
global_total_now = 0.0
global_total_in = 0.0
total_cash_global = 0.0
best_position = None
worst_position = None

for portfolio in PORTFOLIOS:
    if portfolio["mode"] == "manual_total":
        invested_total = portfolio["invested_now"]
        cash_total = portfolio["cash_now"]
        portfolio_total_now = portfolio["total_now"]
        portfolio_total_in = invested_total + cash_total
        change_pct = ((portfolio_total_now - portfolio_total_in) / portfolio_total_in * 100) if portfolio_total_in else 0

        portfolio_results.append({
            "name": portfolio["name"],
            "mode": "manual_total",
            "tickers": portfolio["tickers"],
            "invested_total": invested_total,
            "cash_total": cash_total,
            "portfolio_total_now": portfolio_total_now,
            "portfolio_total_in": portfolio_total_in,
            "change_pct": change_pct,
            "note": portfolio["note"],
            "positions": [],
            "failed": [],
        })

        portfolio_totals.append({"Categorie": portfolio["name"], "Valoare": portfolio_total_now})
        global_total_now += portfolio_total_now
        global_total_in += portfolio_total_in
        total_cash_global += cash_total
        continue

    positions = []
    failed = []
    total_positions_value = 0.0
    invested_total = portfolio["amount_per_stock"] * len(portfolio["tickers"])
    cash_total = sum(x["amount"] for x in portfolio["cash_additions"])

    for ticker in portfolio["tickers"]:
        data, error = get_ticker_data(ticker, portfolio["buy_date"])
        if error:
            failed.append(f"{ticker}: {error}")
            continue

        current_value = portfolio["amount_per_stock"] * (data["price"] / data["buy_price"])
        profit_loss = current_value - portfolio["amount_per_stock"]
        return_pct = (profit_loss / portfolio["amount_per_stock"]) * 100 if portfolio["amount_per_stock"] else 0

        position = {
            "ticker": ticker,
            "price": data["price"],
            "invested": portfolio["amount_per_stock"],
            "current_value": current_value,
            "profit_loss": profit_loss,
            "return_pct": return_pct,
            "portfolio": portfolio["name"],
        }
        positions.append(position)
        total_positions_value += current_value

        if best_position is None or return_pct > best_position["return_pct"]:
            best_position = position
        if worst_position is None or return_pct < worst_position["return_pct"]:
            worst_position = position

    portfolio_total_now = total_positions_value + cash_total
    portfolio_total_in = invested_total + cash_total
    change_pct = ((portfolio_total_now - portfolio_total_in) / portfolio_total_in * 100) if portfolio_total_in else 0

    portfolio_results.append({
        "name": portfolio["name"],
        "mode": "calculated",
        "tickers": portfolio["tickers"],
        "buy_date": portfolio["buy_date"],
        "positions": positions,
        "failed": failed,
        "cash_total": cash_total,
        "invested_total": invested_total,
        "total_positions_value": total_positions_value,
        "portfolio_total_now": portfolio_total_now,
        "portfolio_total_in": portfolio_total_in,
        "change_pct": change_pct,
        "ticker_count": len(portfolio["tickers"]),
    })

    portfolio_totals.append({"Categorie": portfolio["name"], "Valoare": portfolio_total_now})
    global_total_now += portfolio_total_now
    global_total_in += portfolio_total_in
    total_cash_global += cash_total

global_profit = global_total_now - global_total_in
global_profit_pct = (global_profit / global_total_in * 100) if global_total_in else 0

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Dashboard</div>
        <div class="hero-title">My Assets</div>
        <div class="hero-subtitle">
            O vedere mai curată asupra portofoliului tău: valoare totală, cash, alocare pe PIE-uri și performanță pe fiecare poziție.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([3.4, 1.3])

with left:
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Total Assets</div>
                <div class="summary-value">${global_total_now:,.2f}</div>
                <div class="{'summary-positive' if global_profit >= 0 else 'summary-negative'}">
                    {'+' if global_profit >= 0 else ''}${global_profit:,.2f} ({global_profit_pct:.2f}%)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s2:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Capital introdus</div>
                <div class="summary-value">${global_total_in:,.2f}</div>
                <div class="summary-label">Investit + cash</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s3:
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Cash</div>
                <div class="summary-value">${total_cash_global:,.2f}</div>
                <div class="summary-label">Neinvestit</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with s4:
        best_text = "N/A" if best_position is None else f"{best_position['ticker']} {best_position['return_pct']:.2f}%"
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-label">Best Performer</div>
                <div class="summary-value" style="font-size:1.16rem;">{best_text}</div>
                <div class="summary-label">Cea mai bună poziție calculată</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Portfolio Buckets</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">PIE-urile tale tratate ca asset groups</div>', unsafe_allow_html=True)

    for result in portfolio_results:
        pill_class = "pill-pos" if result["change_pct"] >= 0 else "pill-neg"
        sign = "+" if result["change_pct"] >= 0 else ""
        cash_line = f" | Cash: ${result['cash_total']:,.2f}" if result["cash_total"] else ""

        st.markdown(
            f"""
            <div class="asset-row">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div class="asset-name">{result['name']}</div>
                        <div class="asset-sub">Investit: ${result['invested_total']:,.2f}{cash_line}</div>
                    </div>
                    <div style="text-align:right;">
                        <div class="asset-name">${result['portfolio_total_now']:,.2f}</div>
                        <div class="{pill_class}">{sign}{result['change_pct']:.2f}%</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    for result in portfolio_results:
        expander_suffix = "Manual" if result["mode"] == "manual_total" else f"{result['change_pct']:+.2f}%"
        with st.expander(
            f"{result['name']} • ${result['portfolio_total_now']:,.2f} • {expander_suffix}",
            expanded=False
        ):
            if result["mode"] == "manual_total":
                st.markdown(
                    f"""
                    <div class="notice-box">
                        <b>Valoare investită:</b> ${result['invested_total']:.2f}<br>
                        <b>Cash:</b> ${result['cash_total']:.2f}<br>
                        <b>Valoare totală:</b> ${result['portfolio_total_now']:.2f}<br><br>
                        {result['note']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("**Stockurile din PIE OT:**")
                chip_cols = st.columns(5)
                for i, ticker in enumerate(result["tickers"]):
                    with chip_cols[i % 5]:
                        st.markdown(
                            f'<div class="ticker-chip">{ticker}</div>',
                            unsafe_allow_html=True,
                        )
                continue

            st.caption(f"Data intrării: {result['buy_date']:%d.%m.%Y}")

            cols = st.columns(4)
            target_weight = 100 / result["ticker_count"] if result["ticker_count"] else 0

            for i, pos in enumerate(result["positions"]):
                current_weight = (
                    pos["current_value"] / result["total_positions_value"] * 100
                    if result["total_positions_value"] else 0
                )
                with cols[i % 4]:
                    st.metric(
                        label=pos["ticker"],
                        value=f"${pos['price']:.2f}",
                        delta=f"{pos['return_pct']:.2f}%"
                    )
                    st.caption(f"Țintă: {target_weight:.2f}% | Acum: {current_weight:.2f}%")
                    st.caption(f"Valoare poziție: ${pos['current_value']:.2f}")
                    st.caption(f"P/L: ${pos['profit_loss']:+.2f}")

            if result["failed"]:
                st.warning("Simboluri neîncărcate:")
                for item in result["failed"]:
                    st.write(f"- {item}")

with right:
    st.markdown('<div class="sidebar-card"><div class="sidebar-title">Allocation</div>', unsafe_allow_html=True)

    total_value = sum(x["Valoare"] for x in portfolio_totals)
    colors = [green, blue, orange, "#94a3b8", red, "#8b5cf6"]

    current_angle = 0
    segments = []
    legend_html = ""

    for i, item in enumerate(portfolio_totals):
        color = colors[i % len(colors)]
        pct = (item["Valoare"] / total_value * 100) if total_value else 0
        angle = pct * 3.6
        segments.append(f"{color} {current_angle:.2f}deg {current_angle + angle:.2f}deg")
        legend_html += f"""
        <div class="legend-item">
            <div class="legend-color" style="background:{color};"></div>
            <div class="legend-text">
                {item['Categorie']}<br>
                <span class="legend-sub">${item['Valoare']:,.2f} ({pct:.1f}%)</span>
            </div>
        </div>
        """
        current_angle += angle

    donut_style = ", ".join(segments)

    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin:8px 0 16px 0;">
            <div style="
                width:220px;
                height:220px;
                border-radius:50%;
                background: conic-gradient({donut_style});
                position:relative;
                box-shadow:{shadow};
            ">
                <div style="
                    position:absolute;
                    top:50%;
                    left:50%;
                    transform:translate(-50%, -50%);
                    width:112px;
                    height:112px;
                    border-radius:50%;
                    background:{donut_center};
                    border:1px solid {border};
                    display:flex;
                    flex-direction:column;
                    align-items:center;
                    justify-content:center;
                    color:{text_main};
                    text-align:center;
                ">
                    <div style="color:{text_soft}; font-size:12px;">Total</div>
                    <div style="font-size:17px; font-weight:800;">${total_value:,.0f}</div>
                </div>
            </div>
        </div>
        {legend_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if best_position:
        st.markdown(
            f"""
            <div class="sidebar-card">
                <div class="sidebar-title">Top Performer</div>
                <div style="color:{text_main}; font-size:1.1rem; font-weight:800;">{best_position['ticker']}</div>
                <div style="color:{green}; font-weight:700; margin-top:4px;">{best_position['return_pct']:+.2f}%</div>
                <div style="color:{text_soft}; font-size:0.84rem; margin-top:4px;">{best_position['portfolio']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if worst_position:
        st.markdown(
            f"""
            <div class="sidebar-card">
                <div class="sidebar-title">Weakest Performer</div>
                <div style="color:{text_main}; font-size:1.1rem; font-weight:800;">{worst_position['ticker']}</div>
                <div style="color:{red}; font-weight:700; margin-top:4px;">{worst_position['return_pct']:.2f}%</div>
                <div style="color:{text_soft}; font-size:0.84rem; margin-top:4px;">{worst_position['portfolio']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.caption("Date de la Yahoo Finance • Tema implicită este Light • PIE OT folosește momentan valorile reale manuale")
