
import streamlit as st
import numpy as np
import pandas as pd
import requests
import scipy.stats as stats
import matplotlib.pyplot as plt

# Fetch real-time FX data from ExchangeRate-API
def get_fx_rate(pair="EUR/USD"):
    """Fetch FX rate using ExchangeRate-API and print debug info."""
    base_currency, quote_currency = pair.split("/")
    url = f"https://v6.exchangerate-api.com/v6/89241354e5ba7ba43db18baf/latest/{base_currency}"
    
    try:
        response = requests.get(url).json()
        
        # Debugging: Print full API response in Streamlit
        st.write("🔍 Debug: API Response", response)

        if "conversion_rates" in response and quote_currency in response["conversion_rates"]:
            return response["conversion_rates"][quote_currency]
        else:
            st.error(f"⚠️ Error: No FX data found for {pair}. Check API key and supported currencies.")
            return None
    
    except Exception as e:
        st.error(f"⚠️ Error fetching FX rate: {str(e)}")
        return None

# Black-Scholes Model for FX Options
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)

# Monte Carlo Simulation for Stress Testing
def monte_carlo_fx(S, r, sigma, T, simulations=100000):
    dt = T / 252  # Assume 252 trading days per year
    paths = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * np.random.randn(simulations))
    return paths

# Streamlit UI
def main():
    st.title("Currency Run Prediction App")
    st.sidebar.header("Settings")
    
    # Select currency pair
    currency_pair = st.sidebar.selectbox("Select Currency Pair", ["EUR/USD", "GBP/JPY", "USD/JPY"])
    
    # Set FX option parameters
    S = get_fx_rate(currency_pair)
    if S is None:
        return
    
    K = st.sidebar.slider("Strike Price", min_value=0.8 * S, max_value=1.2 * S, value=S * 0.95)
    T = st.sidebar.slider("Time to Expiration (years)", 0.1, 2.0, 0.5)
    r = 0.02  # Fixed risk-free rate
    sigma = st.sidebar.slider("Implied Volatility (%)", 5.0, 50.0, 15.0) / 100
    
    # Compute option price
    call_price = black_scholes_call(S, K, T, r, sigma)
    st.write(f"**Current FX Rate:** {S:.4f}")
    st.write(f"**Black-Scholes Call Price:** {call_price:.4f}")
    
    # Monte Carlo Simulation
    simulated_fx = monte_carlo_fx(S, r, sigma, T)
    crash_prob = np.mean(simulated_fx < K)
    
    # Display results
    st.write(f"⚠️ **Probability of a Currency Run:** {crash_prob:.2%}")
    
    # Histogram of simulated FX movements
    fig, ax = plt.subplots()
    ax.hist(simulated_fx, bins=100, color='blue', alpha=0.6)
    ax.axvline(x=K, color='red', linestyle='--', label="Strike Price")
    ax.set_title("Monte Carlo Simulated FX Rates")
    ax.set_xlabel("Simulated Exchange Rate")
    ax.set_ylabel("Frequency")
    ax.legend()
    st.pyplot(fig)

if __name__ == "__main__":
    main()

