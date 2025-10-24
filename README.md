
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

Let me know if you want me to commit this README.md into your repo for you.
