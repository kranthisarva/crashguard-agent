
# 🚨 CrashGuard — Market Crash Detection & Alert System

CrashGuard monitors macroeconomic indicators and market signals to compute a **Crash Risk Index (CRI)**.
It emails you (or your team) **only when risk becomes meaningful** — **Yellow, Orange, or Red** — so you never miss warning signs.

---

## ✅ Features

✔ Fully automated — runs **twice daily (8 AM & 12 PM CST)** via GitHub Actions
✔ Computes a **Crash Risk Index** from 8 core economic indicators
✔ **Email alerts using Gmail (App Password supported)**
✔ Optional **stock-specific alerts** (SPY, QQQ, NVDA, AMD, etc.)
✔ Saves all runs to `cri_history.json` for trend analysis
✔ Lightweight, configurable via a single `config.yaml`
✔ No servers required — runs entirely in your GitHub repo

---

## 📁 Project Structure

```
crashguard-agent/
├── crashguard/
│   ├── fetchers/           # Fetch data from FRED, Yahoo Finance
│   │   └── fetchers.py
│   ├── scoring.py          # CRI logic, thresholds, scoring
│   ├── notify.py           # Email / Push notifications
│   └── run.py              # Main entrypoint (used by GitHub Actions)
├── config.yaml             # All weights, thresholds, stock list, rules
├── requirements.txt
├── cri_history.json        # Auto-generated log of past runs
└── .github/
    └── workflows/
        └── crashguard.yml  # Scheduled workflow & manual trigger
```

---

## ⚙️ 1. Setup — GitHub Secrets (Required)

Go to:
**GitHub → Your Repo → Settings → Secrets and Variables → Actions → New Repository Secret**

Add the following:

| Secret Name    | Description                                                                                     |
| -------------- | ----------------------------------------------------------------------------------------------- |
| `FRED_API_KEY` | From [https://fred.stlouisfed.org/](https://fred.stlouisfed.org/) (free macroeconomic data API) |
| `SMTP_HOST`    | e.g. `smtp.gmail.com`                                                                           |
| `SMTP_PORT`    | `587`                                                                                           |
| `SMTP_USER`    | Your email (e.g. `yourname@gmail.com`)                                                          |
| `SMTP_PASS`    | **Your Gmail App Password (not normal password)**                                               |
| `EMAIL_TO`     | Who should receive crash alerts?                                                                |

---

## 📧 2. How to Create a Gmail App Password (Required for Email Alerts)

Gmail blocks apps from sending emails unless an **App Password** is used.

**Follow these steps:**

1. Visit [https://myaccount.google.com/](https://myaccount.google.com/)
2. Go to **Security**
3. Enable **2-Step Verification**
4. Then, go back to **Security → App Passwords**
5. Select:

   * **App** → “Mail”
   * **Device** → “Other (CrashGuard)”
6. Click **Generate**
7. Google shows a **16-character password** (e.g. `abcd efgh ijkl mnop`)
8. Copy it → use it as the value for `SMTP_PASS` in GitHub Secrets

✅ This App Password only works for sending mail — it is **safe and revocable anytime.**

---

## ⏱️ 3. When Does It Run?

The schedule is inside `.github/workflows/crashguard.yml`:

```yaml
on:
  schedule:
    - cron: "0 14,18 * * 1-5"  # 14:00 & 18:00 UTC (Mon–Fri)
  workflow_dispatch:           # manual run option
```

| UTC Time | CST (Local) | Action            |
| -------- | ----------- | ----------------- |
| 14:00    | 8:00 AM     | Morning CRI Check |
| 18:00    | 12:00 PM    | Midday CRI Check  |

✅ The workflow will now run **automatically**, no manual work needed.

You can also run it manually:
**GitHub → Actions → CrashGuard → Run Workflow**

---

## 🚦 4. When Will You Get an Email?

| CRI Value | Risk Level | Will You Get Email? |
| --------- | ---------- | ------------------- |
| `< 55`    | 🟢 GREEN   | No (normal)         |
| `55–64`   | 🟡 YELLOW  | ✅ Yes               |
| `65–74`   | 🟠 ORANGE  | ✅ Yes               |
| `≥ 75`    | 🔴 RED     | ✅ Yes               |

### ✅ Stock-Specific Alerts (Optional)

If enabled in `config.yaml`, alerts will also be sent when any stock:

✔ Drops >5% from recent 20-day high
✔ Falls >3% below 50-day moving average
✔ Hits a bearish **20DMA < 50DMA crossover**
✔ Gaps down >3% from prior close

💡 That means **you’ll get an email even if CRI is GREEN**, if stocks are crashing.

To enable stock alerts, add this to your `config.yaml`:

```yaml
# --- Stock-specific alerts ---
stocks:
  tickers: ["SPY", "QQQ", "NVDA", "AMD"]
```

---

## 🧪 5. First-Time Run Test

1. Go to **GitHub → Actions → CrashGuard**
2. Click **Run Workflow → Run**
3. Open the logs and look for a JSON output like:

```json
{
  "ts": "2025-10-24T19:36:41Z",
  "cri": 52.0,
  "state": "GREEN",
  "inputs": { ... },
  "scores": { ... },
  "stocks": { ... }
}
```

4. ✅ If state is GREEN and no stock alerts → no email (expected)
5. ✅ If state is YELLOW/ORANGE/RED → you will receive an email

---

## 💻 6. Optional — Local Run (Instead of GitHub)

```bash
git clone https://github.com/yourname/crashguard-agent.git
cd crashguard-agent
python -m venv .venv && source .venv/bin/activate  # (or .venv/Scripts/activate on Windows)
pip install -r requirements.txt

# Create local `.env` file:
FRED_API_KEY=your_fred_key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_16_char_app_password
EMAIL_TO=your_email@gmail.com

# Run manually:
python -m crashguard.run
```

---

## 📊 7. (Optional) Visual Dashboard

You can add a Streamlit dashboard (`dashboard/streamlit_app.py`) to visualize CRI trends.
Run locally:

```bash
pip install streamlit plotly
streamlit run dashboard/streamlit_app.py
```

---

## ✅ 8. That’s It!

CrashGuard is now **automated, alert-enabled, and production-ready**.

**Next possible upgrades (just tell me if you want):**

* ✅ Deploy web dashboard (Streamlit Cloud / Vercel)
* ✅ Add Telegram / Slack / WhatsApp alerts
* ✅ Pull real Shiller P/E and Buffett Indicator instead of overrides
* ✅ Export CRI data into Google Sheets or Excel
* ✅ Add hedge suggestions (e.g., SPY puts when CRI > 70)

---



## 📐 9. How the Crash Risk Index (CRI) Is Calculated

CrashGuard uses a **weighted scoring system** that combines multiple macroeconomic stress indicators into a single number called the **Crash Risk Index (CRI)**.

### **Step 1 — Collect Economic Inputs**

The following indicators are fetched from FRED / Yahoo Finance:

| Indicator                    | Meaning                            | Input Used                |
| ---------------------------- | ---------------------------------- | ------------------------- |
| Shiller PE Ratio             | Stock market valuation vs earnings | Latest value              |
| Buffett Indicator            | Total US Market Cap / GDP          | % value                   |
| Yield Curve (10Y–2Y)         | Recession predictor                | Basis points (bps)        |
| VIX                          | Volatility / fear index            | Latest close              |
| Unemployment Rate YoY Change | Labor market weakening             | % point change            |
| CPI Inflation YoY            | Inflation pressure                 | %                         |
| Real GDP (QoQ Annualized)    | Economic growth                    | %                         |
| Margin Debt (Optional)       | Investor leverage                  | Z-score vs 5-year average |

---

### **Step 2 — Convert Each Input Into a Risk Score (0–100)**

Each variable is mapped into a **risk band** based on historical danger zones you define in `config.yaml`. Example for Shiller PE:

| Shiller PE | Score               |
| ---------- | ------------------- |
| < 25       | 10 (low risk)       |
| 25–30      | 40                  |
| 30–35      | 70                  |
| > 35       | 90 (very high risk) |

Each indicator has similar bands under `bands:` in config.yaml.

---

### **Step 3 — Apply Weighting**

Each indicator has a weight (importance) from the `weights:` section.

Example from your config:

```yaml
weights:
  shiller: 0.15
  buffett: 0.15
  unemp:   0.10
  cpi:     0.10
  gdp:     0.10
  curve:   0.15
  vix:     0.15
  margin:  0.10
```

**Weighted CRI formula:**

[
\text{CRI (base)} = \sum \big( \text{Indicator Score} \times \text{Weight} \big)
]

Example:
If Shiller = 70 → 70 × 0.15 = 10.5 points toward CRI.

---

### **Step 4 — Add “Velocity Boost” (Fast-Rising Risk)**

If CRI jumped significantly in the last 7 days, we add extra points:

From config:

```yaml
velocity_boost:
  +12: 5      # If CRI↑ by 12+ points in 7 days → add +5
  +20: 10     # If CRI↑ by 20+ points → add +10
```

This detects accelerating danger — like 2008 or 2020 crashes.

---

### **Step 5 — Add “Confluence Boost” (Multiple Red Flags at Once)**

If 3 or more of these are true at the same time:

* Yield curve inverted (< 0 bps)
* VIX > 30
* Shiller PE > 35
* Buffett Indicator > 180% of GDP

Then add:

```yaml
confluence_boost: 10
```

---

### **Step 6 — Final CRI Value and Color**

After these steps:

[
\text{CRI (final)} = \text{Weighted CRI} + \text{Velocity Boost} + \text{Confluence Boost}
]

Then we assign a color level:

```yaml
thresholds:
  yellow: 55
  orange: 65
  red: 75
```

| CRI Range | Level     | Alert Sent? |
| --------- | --------- | ----------- |
| < 55      | 🟢 GREEN  | No          |
| 55–64     | 🟡 YELLOW | ✅ Yes       |
| 65–74     | 🟠 ORANGE | ✅ Yes       |
| ≥ 75      | 🔴 RED    | ✅ Yes       |

---

### ✅ Example Output

```json
"cri": 68.4,
"state": "ORANGE",
"details": {
  "vel_boost": 0,
  "conf_boost": 10,
  "triggers": ["curve_inverted","vix_gt_30","buffett_gt_180"]
}
```

---


