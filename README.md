# 💰 Currency Hedge Fund Risk Analysis App

### **📌 Overview**
This app models **currency risk for hedge funds** using advanced **quantitative finance techniques**.  
It calculates **option prices, probability of currency crashes, and Monte Carlo simulations** to assess risk exposure.

---

## **📈 Theory Behind the Model**
### **1️⃣ Black-Scholes Model (FX Options Pricing)**
Used to price **currency options**, helping hedge funds estimate the **fair value of an option contract**.
- **Call Option Formula**:
  \[
  C = S \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)
  \]
  where:
  - \( S \) = Current FX rate
  - \( K \) = Strike price
  - \( T \) = Time to expiration
  - \( r \) = Risk-free interest rate
  - \( \sigma \) = Implied volatility
  - \( N(d) \) = Cumulative normal distribution

### **2️⃣ Monte Carlo Simulation (Stress Testing)**
Used to simulate **thousands of potential future FX rates** to assess **currency crash probabilities**.
- Simulates FX rates using a **stochastic process**:
  \[
  S_T = S_0 \cdot e^{(r - 0.5 \sigma^2)T + \sigma \sqrt{T} Z}
  \]
  where \( Z \) is a random variable from a normal distribution.

---

## **⚙️ Parameters Used**
| **Parameter** | **Definition** | **User Adjustable?** |
|--------------|--------------|------------------|
| `S` | Current exchange rate | ✅ (Fetched live) |
| `K` | Strike price (option contract) | ✅ (User selects) |
| `T` | Time to expiration (years) | ✅ |
| `r` | Risk-free rate | ❌ (Fixed at 2%) |
| `σ` | Implied volatility | ✅ (User selects) |
| `Simulations` | Number of Monte Carlo runs | ❌ (Fixed at 100,000) |

---

## **📊 What the App Calculates**
✅ **FX Option Price** (Black-Scholes formula).  
✅ **Monte Carlo Stress Test** (Future FX rate simulations).  
✅ **Crash Probability** (% chance that FX rate drops below `K`).  
✅ **Interactive Visualization** (FX rate histogram).  

---

## **🚀 How to Run**
streamlit run currency_run_app.py
