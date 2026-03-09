import math
from datetime import datetime

import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Simple Stock Helper", page_icon="📈", layout="centered")

st.title("📈 Simple Stock Helper")
st.caption("Educational use only — not financial advice.")

st.markdown(
    "This app helps you check a stock price, see how many shares you can afford, "
    "and set a stop loss and target."
)

cash = st.number_input("How much money do you have?", min_value=1.0, value=250.0, step=25.0)
ticker = st.text_input("Stock ticker", value="AAPL").upper().strip()
stop_loss_pct = st.slider("Stop loss %", min_value=1, max_value=20, value=5) / 100
take_profit_pct = st.slider("Take profit %", min_value=1, max_value=50, value=10) / 100
allow_fractional = st.toggle("Allow fractional shares", value=False)

def get_price(symbol: str):
    try:
        data = yf.Ticker(symbol).history(period="1d", interval="1m")
        if data.empty:
            return None
        return float(data["Close"].iloc[-1])
    except Exception:
        return None

if st.button("Check stock"):
    price = get_price(ticker)

    if price is None:
        st.error("Could not load that ticker right now. Try another one.")
    else:
        if allow_fractional:
            shares = round(cash / price, 4)
        else:
            shares = math.floor(cash / price)

        cost = round(shares * price, 2)
        stop_price = round(price * (1 - stop_loss_pct), 2)
        target_price = round(price * (1 + take_profit_pct), 2)
        leftover_cash = round(cash - cost, 2)

        st.subheader(f"{ticker} results")
        st.metric("Current price", f"${price:.2f}")
        st.metric("Shares you can buy", f"{shares}")
        st.metric("Estimated cost", f"${cost:.2f}")
        st.metric("Cash left over", f"${leftover_cash:.2f}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Stop loss price", f"${stop_price:.2f}")
        with col2:
            st.metric("Take profit price", f"${target_price:.2f}")

        st.info(
            f"If you buy {shares} shares of {ticker} at about ${price:.2f}, "
            f"you could consider selling if it falls to ${stop_price:.2f} "
            f"or taking profit near ${target_price:.2f}."
        )

st.divider()
st.subheader("How to run this on the web")
st.markdown(
    '''
**Easiest option: Streamlit Cloud**

1. Make a free GitHub account  
2. Create a new file named `app.py` and paste this code into it  
3. Create a second file named `requirements.txt` with:

```text
streamlit
yfinance
```

4. Put both files in a GitHub repo  
5. Go to Streamlit Community Cloud and deploy the repo  
6. Your app opens in a browser link
'''
)

st.caption(f"Last opened: {datetime.now().strftime('%b %d, %Y %I:%M %p')}")
