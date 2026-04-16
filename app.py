import streamlit as st
import requests
from PIL import Image
import pandas as pd

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Green-Grocer AI Dashboard",
    page_icon="🍎",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0e1117; }

    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ff88;
        text-align: center;
        padding: 1rem 0 0.2rem 0;
    }
    .dashboard-sub {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* Metric Cards */
    .metric-card {
        background: #1a1d27;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #2a2d3a;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #00ff88;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        margin-top: 0.3rem;
    }

    /* Verdict Banner */
    .verdict-pass {
        background: linear-gradient(135deg, #00ff8822, #00ff8811);
        border: 1px solid #00ff88;
        border-radius: 12px;
        padding: 1rem 2rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #00ff88;
        margin: 1rem 0;
    }
    .verdict-fail {
        background: linear-gradient(135deg, #ff444422, #ff444411);
        border: 1px solid #ff4444;
        border-radius: 12px;
        padding: 1rem 2rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: #ff4444;
        margin: 1rem 0;
    }

    /* Grade Badges */
    .badge-a {
        background: #00ff8822;
        color: #00ff88;
        border: 1px solid #00ff88;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-b {
        background: #ffaa0022;
        color: #ffaa00;
        border: 1px solid #ffaa00;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .badge-c {
        background: #ff444422;
        color: #ff4444;
        border: 1px solid #ff4444;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ccc;
        border-bottom: 1px solid #2a2d3a;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }

    .latency-bar {
        background: #1a1d27;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        color: #888;
        font-size: 0.9rem;
        border: 1px solid #2a2d3a;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="dashboard-title">🍎 Green-Grocer Quality Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-sub">AI-powered fruit inspection system — Upload an image to begin analysis</div>', unsafe_allow_html=True)

# ── Upload Section ────────────────────────────────────────────
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "webp"], label_visibility="collapsed")

if uploaded_file is not None:

    col_img, col_gap, col_info = st.columns([2, 0.2, 1.5])

    with col_img:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

    with col_info:
        st.markdown('<div class="section-header">📋 Scan Status</div>', unsafe_allow_html=True)
        st.info("🔄 Sending to AI Engine...")

    # ── API Call ──────────────────────────────────────────────
    try:
        uploaded_file.seek(0)
        files = {"file": ("image.jpg", uploaded_file.getvalue(), "image/jpeg")}
        response = requests.post("http://127.0.0.1:8000/inspect", files=files, timeout=15)

        if response.status_code == 200:
            result = response.json()
            detections = result["data"]["detections"]
            summary   = result["data"]["summary"]
            latency   = result["header"]["latency_seconds"]

            # ── Batch Verdict ─────────────────────────────────
            verdict_class = "verdict-pass" if "PASS" in summary["batch_verdict"] else "verdict-fail"
            st.markdown(f'<div class="{verdict_class}">Batch Verdict: {summary["batch_verdict"]}</div>', unsafe_allow_html=True)

            # ── Metric Cards ──────────────────────────────────
            st.markdown('<div class="section-header">📊 Batch Summary</div>', unsafe_allow_html=True)
            m1, m2, m3, m4, m5 = st.columns(5)

            with m1:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value">{summary["total_items"]}</div>
                    <div class="metric-label">Total Detected</div>
                </div>''', unsafe_allow_html=True)
            with m2:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value" style="color:#00ff88">{summary["grade_a_count"]}</div>
                    <div class="metric-label">✅ Grade A</div>
                </div>''', unsafe_allow_html=True)
            with m3:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value" style="color:#ffaa00">{summary["grade_b_count"]}</div>
                    <div class="metric-label">⚠️ Grade B</div>
                </div>''', unsafe_allow_html=True)
            with m4:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value" style="color:#ff4444">{summary["grade_c_count"]}</div>
                    <div class="metric-label">❌ Grade C</div>
                </div>''', unsafe_allow_html=True)
            with m5:
                st.markdown(f'''<div class="metric-card">
                    <div class="metric-value">{summary["pass_rate_percent"]}%</div>
                    <div class="metric-label">Pass Rate</div>
                </div>''', unsafe_allow_html=True)

            # ── Detection Table ───────────────────────────────
            st.markdown('<div class="section-header">🔍 Individual Detections</div>', unsafe_allow_html=True)

            for i, item in enumerate(detections):
                grade = item["quality"]["grade"]
                badge_class = "badge-a" if grade == "Grade A" else "badge-b" if grade == "Grade B" else "badge-c"

                with st.expander(f"{item['quality']['status']}  {item['label'].title()}  #{i+1}  —  {item['confidence_pct']} confidence"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Grade", grade)
                    c2.metric("Confidence", item["confidence_pct"])
                    c3.metric("Action", item["quality"]["action"])
                    st.caption(f"📦 Bounding Box: {item['box_coordinates']}")

            # ── Latency ───────────────────────────────────────
            st.markdown(f'<div class="latency-bar">⚡ AI Processing Time: {latency} seconds</div>', unsafe_allow_html=True)

        else:
            st.error(f"API Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot reach Docker container. Make sure it is running on port 8000.")
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The model may still be loading — wait 30 seconds and retry.")