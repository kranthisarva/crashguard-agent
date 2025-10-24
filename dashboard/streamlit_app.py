import json, pathlib, pandas as pd, streamlit as st, plotly.express as px

st.set_page_config(page_title="CrashGuard Dashboard", layout="wide")

ROOT = pathlib.Path(__file__).resolve().parent.parent
HIST_PATH = ROOT / "cri_history.json"
CFG_PATH = ROOT / "config.yaml"

st.title("📉 CrashGuard — Crash Risk Index (CRI) Dashboard")

# History & chart
if HIST_PATH.exists():
    hist = json.loads(HIST_PATH.read_text())
    df = pd.DataFrame(hist)
    df["ts"] = pd.to_datetime(df["ts"])
    df = df.sort_values("ts")

    st.subheader("CRI over time")
    fig = px.line(df.tail(180), x="ts", y="cri", markers=False, title="Crash Risk Index (last 180 entries)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    latest = df.iloc[-1]
    with col1:
        st.metric("Current CRI", f"{latest['cri']:.2f}")
    with col2:
        st.metric("State", latest["state"])
    with col3:
        st.write("Details")
        st.json(latest["details"])

    st.subheader("Latest Inputs & Scores")
    cols = st.columns(2)
    with cols[0]:
        st.write("Inputs")
        st.json(latest["inputs"])
    with cols[1]:
        st.write("Scores")
        st.json(latest["scores"])
else:
    st.info("No history yet. Run the workflow at least once to generate `cri_history.json`.")

st.divider()
st.subheader("Configuration (read-only)")
if CFG_PATH.exists():
    st.code(CFG_PATH.read_text(), language="yaml")
else:
    st.info("config.yaml not found.")
