import pandas as pd

def backtest_strategy(df):
    # Strategy Parameters
    capital = 100000  # ₹1 lakh total capital
    leverage = 100
    position_pct = 0.25  # 25% of total capital per trade
    capital_per_trade = capital * position_pct
    exposure = capital_per_trade * leverage
    liquidation_loss = capital_per_trade * 0.75  # Liquidation wipes out 75% of margin
    liquidation_threshold_pct = liquidation_loss / exposure  # % move against trade to liquidate

    # Indicator filter
    df['SMA50'] = df['Close'].rolling(window=50).mean()

    # Trading variables
    in_position = False
    entry_price = 0
    trades = []

    for i in range(50, len(df)):
        row = df.iloc[i]

        if pd.isna(row['SMA50']):
            continue

        # 📈 Long Entry Condition
        if not in_position and row['RSI'] < 45 and row['Close'] > row['SMA50']:
            in_position = True
            entry_price = row['Close']
            entry_time = row['Datetime']
            trades.append({
                'Action': 'Buy',
                'Type': 'Long',
                'Time': entry_time,
                'Price': entry_price
            })

        elif in_position:
            drawdown_pct = (entry_price - row['Close']) / entry_price

            # ⚠️ Liquidation Condition
            if drawdown_pct >= liquidation_threshold_pct:
                exit_price = row['Close']
                exit_time = row['Datetime']
                trades.append({
                    'Action': 'Sell',
                    'Type': 'Liquidated',
                    'Time': exit_time,
                    'Price': exit_price,
                    'Profit': -round(liquidation_loss, 2)
                })
                in_position = False
                continue

            # ✅ Long Exit Condition
            if row['RSI'] > 55:
                exit_price = row['Close']
                exit_time = row['Datetime']
                profit = (exit_price - entry_price) * leverage * (capital_per_trade / entry_price)
                trades.append({
                    'Action': 'Sell',
                    'Type': 'Long Exit',
                    'Time': exit_time,
                    'Price': exit_price,
                    'Profit': round(profit, 2)
                })
                in_position = False

    return pd.DataFrame(trades)

# Execution
if __name__ == "__main__":
    df = pd.read_csv("btc_with_indicators.csv")  # Make sure 'Datetime', 'Close', 'RSI' are present

    trades = backtest_strategy(df)
    trades.to_csv("btc_backtest_with_100x.csv", index=False)

    if not trades.empty:
        print(trades)
        print(f"\n💰 Total Profit: {round(trades['Profit'].sum(), 2)}")
        print(trades['Type'].value_counts())
    else:
        print("⚠️ No trades triggered — check RSI/SMA logic or soften conditions.")
