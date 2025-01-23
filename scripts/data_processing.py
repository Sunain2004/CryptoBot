import pandas as pd
import numpy as np
import pytz

def process_crypto_data(df):
    """
    Process raw cryptocurrency data into features for ML models.
    :param df: Raw DataFrame with historical data.
    :return: Processed DataFrame.
    """

    # Calculate Price Change
    df['price_change'] = df['close'] - df['open']

    # Calculate Percent Change
    df['percent_change'] = (df['price_change'] / df['open']) * 100

    # Simple Moving Average (SMA) using cumulative data
    df['SMA_20'] = compute_sma(df['close'], window=20)
    df['SMA_50'] = compute_sma(df['close'], window=50)

    # Exponential Moving Average (EMA) using cumulative data
    df['EMA_20'] = compute_ema(df['close'], span=20)
    df['EMA_50'] = compute_ema(df['close'], span=50)

    # Volatility (Standard Deviation of Closing Prices over 14 days)
    df['volatility'] = df['close'].rolling(window=14).std()

    # Relative Strength Index (RSI)
    df['RSI'] = compute_rsi(df['close'], window=14)

    return df


def compute_sma(series, window):
    """
    Compute SMA using cumulative data from the CSV.
    :param series: The full historical data series.
    :param window: The moving average window size.
    :return: SMA values as a Series.
    """
    sma = []
    for i in range(len(series)):
        if i + 1 < window:
            # Not enough data for SMA calculation
            sma.append(np.nan)
        else:
            # Use the last `window` rows to compute SMA
            sma.append(series[i + 1 - window:i + 1].mean())
    return pd.Series(sma, index=series.index)


def compute_ema(series, span):
    """
    Compute EMA using cumulative data from the CSV.
    :param series: The full historical data series.
    :param span: The EMA span size.
    :return: EMA values as a Series.
    """
    ema = []
    alpha = 2 / (span + 1)  # Smoothing factor
    prev_ema = None

    for i, price in enumerate(series):
        if prev_ema is None:
            # First EMA is just the first price
            ema.append(price)
        else:
            # Calculate EMA based on previous EMA
            ema.append((price - prev_ema) * alpha + prev_ema)
        prev_ema = ema[-1]
    return pd.Series(ema, index=series.index)


def compute_rsi(series, window):
    """
    Calculate Relative Strength Index (RSI).
    :param series: Price series.
    :param window: Window length for RSI calculation.
    :return: RSI values as a Series.
    """
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=window).mean()
    avg_loss = pd.Series(loss).rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return pd.Series(rsi, index=series.index)
