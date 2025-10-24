import yaml
from dataclasses import dataclass

@dataclass
class ScoreResult:
    scores: dict
    cri: float
    state: str
    details: dict

def _band_score(bands, value):
    v = float(value)
    for lo, hi, score in bands:
        lo = float(lo); hi = float(hi)
        if lo <= v < hi:
            return score
    return bands[-1][2]


def _classify(cri, th):
    if cri >= th["red"]: return "RED"
    if cri >= th["orange"]: return "ORANGE"
    if cri >= th["yellow"]: return "YELLOW"
    return "GREEN"

def compute_scores(cfg, inputs, history_cri=None):
    b = cfg["bands"]; w = cfg["weights"]
    scores = {
        "shiller": _band_score(b["shiller"], inputs["shiller"]),
        "buffett": _band_score(b["buffett"], inputs["buffett"]),
        "unemp": _band_score(b["unemp_yoy"], inputs["unemp_yoy"]),
        "cpi": _band_score(b["cpi_yoy"], inputs["cpi_yoy"]),
        "gdp": _band_score(b["gdp_qoq_annualized"], inputs["gdp_qoq_annualized"]),
        "curve": _band_score(b["curve_bps"], inputs["curve_bps"]),
        "vix": _band_score(b["vix"], inputs["vix"]),
        "margin": _band_score(b["margin_z"], inputs["margin_z"]),
    }
    cri = sum(scores[k]*w[k] for k in scores)
    vel_boost = 0
    if history_cri and len(history_cri) >= 7:
        delta7 = cri - history_cri[-7]
        for k,v in cfg["velocity_boost"].items():
            if delta7 >= float(k): vel_boost = max(vel_boost, v)
    cri += vel_boost
    conf = 0; triggers = []
    if inputs["curve_bps"] < 0: triggers.append("curve_inverted")
    if inputs["vix"] > 30: triggers.append("vix_gt_30")
    if inputs["shiller"] > 35: triggers.append("shiller_gt_35")
    if inputs["buffett"] > 180: triggers.append("buffett_gt_180")
    if sum(t in triggers for t in cfg["confluence_hard_triggers"]) >= 3: conf = cfg["confluence_boost"]
    cri += conf
    state = _classify(cri, cfg["thresholds"])
    return ScoreResult(scores=scores, cri=round(cri,2), state=state, details={"vel_boost":vel_boost,"conf_boost":conf,"triggers":triggers})
