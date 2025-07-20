# 📈 Bitcoin Intraday Strategy with RSI, SMA & Leverage 💰

This project simulates a crypto trading strategy using technical indicators and high leverage, designed for intraday swing trades in Bitcoin. It's a resume-ready, backtesting-focused implementation that mirrors real-world liquidation logic used in crypto exchanges.

---

## ✅ Strategy Highlights

- **Long Entry**: When `RSI < 45` and price is above `SMA50`
- **Long Exit**: When `RSI > 55`
- **Leverage**: 100x with 25% capital usage per trade
- **Liquidation Logic**: If price drops by 0.75% (75% of margin), position is liquidated

---

## 💼 Backtest Assumptions

| Parameter        | Value             |
|------------------|------------------|
| Capital          | ₹1,00,000         |
| Capital per Trade| ₹25,000 (25%)     |
| Leverage         | 100x              |
| Exposure per Trade| ₹25,00,000       |
| Liquidation Threshold | 0.75% adverse movement |

---

## 📁 Files Included

| File               | Description                              |
|--------------------|------------------------------------------|
| `backtestingt.py`  | Fetches Bitcoin OHLCV data using Alpha Vantage API |
| `indicators.py`    | Adds indicators calculating RSI and returns a cleaned file |
| `btc_with_indicators.csv` | The cleaned data file with `Datetime`, `Close`, and `RSI` |
| `backtest.py`      | Applies SMA-RSI based backtesting strategy with leverage and liquidation |
| `btc_backtest_with_100x.csv` | Backtest output showing each trade, type, time, price, and profit |
| `README.md`        | This documentation file |

---

## 📊 Sample Trade Output

  Action        Type        Time      Price    Profit
0    Buy        Long  2024-12-22   95087.75       NaN
1   Sell  Liquidated  2024-12-27   94171.89  -18750.0
2    Buy        Long  2025-06-05  101570.20       NaN
3   Sell   Long Exit  2025-06-09  110301.15  214899.4

💰 Total Profit: 196149.4

## 🛠 How to Run

```bash
# Step 1: Fetch and preprocess BTC data
python backtestingt.py

# Step 2: Adds the indicators 
python indicators.py

# Step 3: Run the strategy
python backtest.py