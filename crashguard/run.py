import os, json, yaml, pathlib, datetime as dt
from dotenv import load_dotenv
from crashguard.fetchers import (fetch_yield_curve_bps, fetch_unemployment_yoy_pp, fetch_cpi_yoy,
                                 fetch_gdp_qoq_annualized, fetch_vix, fetch_shiller_pe,
                                 fetch_buffett_indicator, fetch_margin_debt_z)
from crashguard.scoring import compute_scores
from crashguard.notify import notify

HERE = pathlib.Path(__file__).resolve().parent
load_dotenv()

def load_cfg():
    with open(HERE.parent / "config.yaml","r") as f: return yaml.safe_load(f)

def load_history():
    p = HERE.parent / "cri_history.json"
    if p.exists(): return json.loads(p.read_text())
    return []

def save_history(hist):
    p = HERE.parent / "cri_history.json"
    p.write_text(json.dumps(hist[-365:], indent=2))

def main():
    cfg = load_cfg(); hist = load_history()
    inputs = {
        "shiller": fetch_shiller_pe(),
        "buffett": fetch_buffett_indicator(),
        "unemp_yoy": fetch_unemployment_yoy_pp(),
        "cpi_yoy": fetch_cpi_yoy(),
        "gdp_qoq_annualized": fetch_gdp_qoq_annualized(),
        "curve_bps": fetch_yield_curve_bps(),
        "vix": fetch_vix(),
        "margin_z": fetch_margin_debt_z()
    }
    prev_cri = [h["cri"] for h in hist] if hist else None
    res = compute_scores(cfg, inputs, prev_cri)
    now = dt.datetime.utcnow().isoformat(timespec="seconds")+"Z"
    row = {"ts":now,"inputs":inputs,"scores":res.scores,"cri":res.cri,"state":res.state,"details":res.details}
    hist.append(row); save_history(hist)
    title = f"CrashGuard: {res.state} — CRI {res.cri}"
    body = json.dumps(row, indent=2)
    print(body)
    notify(title, body)

if __name__ == "__main__":
    main()
