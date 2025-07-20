# indicators.py

import pandas as pd
import ta

def add_indicators(df):
    """
    Adds RSI and Momentum indicators to BTC daily data.
    """
    # RSI (14-day)
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()

    # Momentum (difference over 4 days)
    df['Momentum'] = df['Close'].diff(4)

    # Drop NaN rows
    df.dropna(inplace=True)

    return df

if __name__ == "__main__":
    df = pd.read_csv("intraday.csv", parse_dates=['Datetime'])

    df = add_indicators(df)

    df.to_csv("btc_with_indicators.csv", index=False)
    print(df[['Datetime', 'Close', 'RSI', 'Momentum']].head())
