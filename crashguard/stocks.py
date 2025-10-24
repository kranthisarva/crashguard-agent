import numpy as np, yfinance as yf

def _sma(series, window):
    return series.rolling(window=window).mean()

def analyze_ticker(ticker: str, lookback_days: int = 120):
    data = yf.download(ticker, period=f"{lookback_days}d", interval="1d", progress=False, auto_adjust=True)
    if data is None or data.empty:
        return {"ticker": ticker, "error": "No data"}

    close = data["Close"]
    # yfinance sometimes returns DataFrame for single ticker; normalize to Series
    if hasattr(close, "columns"):
        close = close.iloc[:, -1]
    close = close.dropna()

    sma20 = _sma(close, 20)
    sma50 = _sma(close, 50)
    signals = []
    latest = float(close.iloc[-1])

    # 1) Drawdown vs 20d high
    recent_high = float(close.tail(20).max())
    drawdown_pct = (latest - recent_high) / recent_high * 100.0
    if drawdown_pct <= -5.0:
        signals.append({"type": "Drawdown", "level": "Alert", "detail": f"{drawdown_pct:.2f}% below 20d high"})

    # 2) Below 50DMA by >3%
    if not np.isnan(sma50.iloc[-1]):
        below50 = (latest - float(sma50.iloc[-1])) / float(sma50.iloc[-1]) * 100.0
        if below50 <= -3.0:
            signals.append({"type": "MA", "level": "Alert", "detail": f"{below50:.2f}% below 50DMA"})

    # 3) Bearish 20/50 cross (today 20<50, yesterday 20>=50)
    if len(sma20.dropna()) > 1 and len(sma50.dropna()) > 1:
        today_bear = sma20.iloc[-1] < sma50.iloc[-1]
        yest_bull = sma20.iloc[-2] >= sma50.iloc[-2]
        if today_bear and yest_bull:
            signals.append({"type": "Cross", "level": "Alert", "detail": "20DMA crossed below 50DMA"})

    # 4) Gap down >3% day-over-day
    if len(close) >= 2:
        prev = float(close.iloc[-2])
        gap = (latest - prev) / prev * 100.0
        if gap <= -3.0:
            signals.append({"type": "Gap", "level": "Alert", "detail": f"{gap:.2f}% gap down"})

    status = "OK" if len(signals) == 0 else "ALERT"
    return {"ticker": ticker, "price": latest, "signals": signals, "status": status}

def analyze_universe(tickers):
    out = []
    for t in tickers:
        try:
            out.append(analyze_ticker(t))
        except Exception as e:
            out.append({"ticker": t, "error": str(e)})
    return out
