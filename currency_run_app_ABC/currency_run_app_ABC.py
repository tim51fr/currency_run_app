import streamlit as st
import numpy as np
import pandas as pd
import requests
import scipy.stats as stats
import matplotlib.pyplot as plt

# API Key for ExchangeRate-API (Replace with a real key if needed)
API_KEY = "89241354e5ba7ba43db18baf"
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

st.title("💰 Currency Hedge Fund Risk Analysis App")
st.write("Analyze FX risk with Black-Scholes & Monte Carlo simulations.")

# -------------------------------------------
# 🔹 Fetch Available Currencies from API
# -------------------------------------------
@st.cache_data
def get_available_currencies():
    """Fetch available currencies from ExchangeRate-API"""
    url = API_URL + "USD"  # Use USD as the base currency for listing all rates
    response = requests.get(url).json()
    
    if "conversion_rates" in response:
        return list(response["conversion_rates"].keys())  # Get currency list
    else:
        st.error("⚠️ Error: Could not fetch currency list.")
        return []

currencies = get_available_currencies()

# -------------------------------------------
# 🔹 User Inputs: Select Currency Pair
# -------------------------------------------
col1, col2 = st.columns(2)
with col1:
    base_currency = st.selectbox("Select Base Currency", currencies, index=currencies.index("USD"))
with col2:
    quote_currency = st.selectbox("Select Quote Currency", currencies, index=currencies.index("EUR"))

currency_pair = f"{base_currency}/{quote_currency}"

# -------------------------------------------
# 🔹 Fetch Real-Time FX Rate
# -------------------------------------------
def get_fx_rate(base_currency, quote_currency):
    """Fetch FX rate for any currency pair"""
    url = API_URL + base_currency
    response = requests.get(url).json()

    if "conversion_rates" in response and quote_currency in response["conversion_rates"]:
        return response["conversion_rates"][quote_currency]
    else:
        st.error(f"⚠️ Error: No FX data found for {base_currency}/{quote_currency}.")
        return None

S = get_fx_rate(base_currency, quote_currency)
if S is None:
    st.stop()  # Stop execution if no FX rate is found

st.markdown(f"### 💵 **Current FX Rate:** {S:.4f} {base_currency} = 1 {quote_currency}")

# -------------------------------------------
# 🔹 Black-Scholes Model for FX Options
# -------------------------------------------
def black_scholes_call(S, K, T, r, sigma):
    """Black-Scholes pricing for call options"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)

# -------------------------------------------
# 🔹 Monte Carlo Simulation for FX Stress Testing
# -------------------------------------------
def monte_carlo_fx(S, r, sigma, T, simulations=100000):
    """Monte Carlo simulation for FX rates"""
    dt = T / 252  # Assume 252 trading days per year
    paths = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * np.random.randn(simulations))
    return paths

# -------------------------------------------
# 🔹 FX Option Pricing Parameters
# -------------------------------------------
st.sidebar.header("FX Option Pricing Parameters")
K = st.sidebar.slider("Strike Price", min_value=0.8 * S, max_value=1.2 * S, value=S * 0.95)
T = st.sidebar.slider("Time to Expiration (years)", 0.1, 2.0, 0.5)
r = 0.02  # Fixed risk-free rate
sigma = st.sidebar.slider("Implied Volatility (%)", 5.0, 50.0, 15.0) / 100

# Compute Black-Scholes Call Price
call_price = black_scholes_call(S, K, T, r, sigma)
st.markdown(f"### 📊 **Black-Scholes Call Price:** {call_price:.4f}")

# -------------------------------------------
# 🔹 Monte Carlo Stress Test & Crash Probability
# -------------------------------------------
simulated_fx = monte_carlo_fx(S, r, sigma, T)
crash_prob = np.mean(simulated_fx < K)

st.markdown(f"### ⚠️ **Probability of a Currency Run:** {crash_prob:.2%}")

# Plot Histogram of Simulated FX Rates
fig, ax = plt.subplots()
ax.hist(simulated_fx, bins=100, color='blue', alpha=0.6)
ax.axvline(x=K, color='red', linestyle='--', label="Strike Price")
ax.set_title(f"Monte Carlo Simulated FX Rates for {currency_pair}")
ax.set_xlabel("Simulated Exchange Rate")
ax.set_ylabel("Frequency")
ax.legend()
st.pyplot(fig)

# -------------------------------------------
# 🔹 Final Notes for Hedge Fund Users
# -------------------------------------------
st.markdown("""
### 📈 Professional Use Case:
- **Live FX risk modeling** with option pricing & Monte Carlo.
- **Supports any currency pair** with real-time API data.
- **Use cases:** Hedge funds, FX traders, risk analysts.
""")


