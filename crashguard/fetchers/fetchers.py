import os
from fredapi import Fred
import yfinance as yf

def fred():
    return Fred(api_key=os.getenv("FRED_API_KEY"))

def fetch_yield_curve_bps():
    s = fred().get_series("T10Y2Y").dropna()
    return float(s.iloc[-1])*100.0

def fetch_unemployment_yoy_pp():
    s = fred().get_series("UNRATE").dropna()
    return float(s.iloc[-1] - s.shift(12).iloc[-1])

def fetch_cpi_yoy():
    s = fred().get_series("CPIAUCSL").dropna()
    return float((s.pct_change(12).iloc[-1])*100.0)

def fetch_gdp_qoq_annualized():
    s = fred().get_series("A191RL1Q225SBEA").dropna()
    return float(s.iloc[-1])

def fetch_vix():
    data = yf.download("^VIX", period="5d", interval="1d", progress=False, auto_adjust=True)
    return float(data["Close"].tail(1).item())

def fetch_shiller_pe():
    return float(os.getenv("SHILLER_PE_OVERRIDE","33.0"))

def fetch_buffett_indicator():
    return float(os.getenv("BUFFETT_INDICATOR_OVERRIDE","170.0"))

def fetch_margin_debt_z():
    return float(os.getenv("MARGIN_DEBT_Z_OVERRIDE","0.5"))
