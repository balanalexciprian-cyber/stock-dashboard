def get_data(tick, group_name):
    try:
        stock = yf.Ticker(tick)
        hist = stock.history(period="3y")

        if hist.empty:
            return None

        current_price = hist['Close'].iloc[-1]

        if group_name == "🤖 AI TECH":
            ref_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        else:
            target_date = pie_ot_date if group_name == "💰 PIE OT Investimental" else alex_pie_date
            past_data = hist[hist.index.date <= target_date]
            ref_price = past_data['Close'].iloc[-1] if not past_data.empty else hist['Close'].iloc[0]

        change_pct = (current_price - ref_price) / ref_price * 100 if ref_price else 0

        return {
            'price': current_price,
            'change_pct': change_pct,
            'ref_price': ref_price
        }

    except Exception as e:
        st.error(f"Eroare la {tick}: {e}")
        return None
