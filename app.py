from dotenv import load_dotenv
load_dotenv()
import streamlit as st

st.set_page_config(
    page_title="Review Analysis System",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ─── Root Variables ─────────────────────────────── */
:root {
    --purple-900: #1a0533;
    --purple-800: #2d0a52;
    --purple-700: #3d1270;
    --purple-600: #5b21b6;
    --purple-500: #7c3aed;
    --purple-400: #a855f7;
    --purple-300: #c084fc;
    --purple-200: #e9d5ff;
    --purple-100: #f5f3ff;
    --accent:     #f0abfc;
    --gold:       #fbbf24;
    --surface:    #ffffff;
    --text-primary: #1e1b4b;
    --text-secondary: #6b7280;
    --border: #ede9fe;
    --shadow: 0 4px 24px rgba(124, 58, 237, 0.12);
    --shadow-lg: 0 8px 48px rgba(124, 58, 237, 0.18);
}

/* ─── Global Reset ───────────────────────────────── */
* { font-family: 'DM Sans', sans-serif; }

html, body, [class*="css"] {
    background-color: #f8f5ff !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 2rem 2.5rem 4rem;
    max-width: 1200px;
}

/* ─── Sidebar ────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--purple-900) 0%, var(--purple-800) 60%, var(--purple-700) 100%) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #e9d5ff !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    display: block !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(168, 85, 247, 0.25) !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stRadio [data-checked="true"] label,
[data-testid="stSidebar"] .stRadio input:checked + div {
    background: rgba(168, 85, 247, 0.3) !important;
    color: #ffffff !important;
}

[data-testid="stSidebarNav"] { display: none; }

/* Sidebar title */
[data-testid="stSidebar"] h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.4rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: -0.5px !important;
    padding: 0.5rem 0 !important;
}

[data-testid="stSidebar"] .stMarkdown p {
    font-size: 0.8rem !important;
    color: #c084fc !important;
    line-height: 1.5 !important;
    padding: 0.5rem 0 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(168, 85, 247, 0.3) !important;
    margin: 1rem 0 !important;
}

/* ─── Page Headers ───────────────────────────────── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text-primary) !important;
}

.main-banner {
    background: linear-gradient(135deg, var(--purple-800) 0%, var(--purple-600) 50%, var(--purple-500) 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.main-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(240,171,252,0.2) 0%, transparent 70%);
    border-radius: 50%;
}

.main-banner::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 20%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(167,139,250,0.15) 0%, transparent 70%);
    border-radius: 50%;
}

.main-banner h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    margin: 0 0 0.5rem 0 !important;
    letter-spacing: -1px;
    position: relative; z-index: 1;
}

.main-banner p {
    color: #e9d5ff !important;
    font-size: 1rem !important;
    margin: 0 !important;
    font-weight: 300 !important;
    position: relative; z-index: 1;
}

/* ─── Section Headers ────────────────────────────── */
.page-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.75rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--border);
}

.page-header h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--purple-700) !important;
    margin: 0 !important;
}

/* ─── Metric Cards ───────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: var(--shadow) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-lg) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: var(--purple-600) !important;
}

/* ─── Buttons ────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--purple-600), var(--purple-500)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--purple-500), var(--purple-400)) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.45) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── Alerts / Status Messages ───────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-size: 0.9rem !important;
}

.stSuccess {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
    border-left: 4px solid #22c55e !important;
}

.stWarning {
    background: linear-gradient(135deg, #fffbeb, #fef3c7) !important;
    border-left: 4px solid #f59e0b !important;
}

.stError {
    background: linear-gradient(135deg, #fef2f2, #fee2e2) !important;
    border-left: 4px solid #ef4444 !important;
}

.stInfo {
    background: linear-gradient(135deg, var(--purple-100), #ede9fe) !important;
    border-left: 4px solid var(--purple-400) !important;
}

/* ─── Inputs ─────────────────────────────────────── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within {
    border-color: var(--purple-400) !important;
    box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.12) !important;
}

/* ─── File Uploader ──────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--purple-300) !important;
    border-radius: 16px !important;
    background: var(--purple-100) !important;
    padding: 1rem !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--purple-500) !important;
    background: #ede9fe !important;
}

/* ─── Dataframe ──────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: var(--shadow) !important;
}

/* ─── Divider ────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1.5px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ─── Spinner ────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--purple-500) !important;
}

/* ─── Download Button ────────────────────────────── */
.stDownloadButton > button {
    background: var(--surface) !important;
    color: var(--purple-600) !important;
    border: 1.5px solid var(--purple-300) !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.stDownloadButton > button:hover {
    background: var(--purple-100) !important;
    border-color: var(--purple-500) !important;
    color: var(--purple-700) !important;
}

/* ─── Plotly Charts ──────────────────────────────── */
.js-plotly-plot .plotly .main-svg {
    border-radius: 12px !important;
}

/* ─── Scrollbar ──────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--purple-100); border-radius: 10px; }
::-webkit-scrollbar-thumb { background: var(--purple-300); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--purple-400); }

</style>
""", unsafe_allow_html=True)


# ─── Main Banner ──────────────────────────────────────────────
st.markdown("""
<div class="main-banner">
    <h1> Review Analysis System</h1>
    <p>Advanced rule-based sentiment scoring engine for bulk review processing</p>
</div>
""", unsafe_allow_html=True)


# ─── Navigation ───────────────────────────────────────────────
section_descriptions = {
    " Overview":       "View system statistics and overall performance summary.",
    " Upload Files":   "Upload CSV, TXT, XLSX, or DOCX files to begin processing.",
    " Run Analysis":   "Analyze reviews using the regex keyword sentiment engine.",
    " View Records":   "Browse, search, filter and download all processed reviews.",
    " Analytics":      "Visualize sentiment distribution and trend charts.",
    " Email Report":   "Generate a PDF report and send results via email.",
    " Clear Data":     "Permanently delete all stored reviews and analysis results.",
}

st.sidebar.title(" Review Analysis")
st.sidebar.markdown("---")

section = st.sidebar.radio(
    "Navigate",
    list(section_descriptions.keys())
)

st.sidebar.markdown("---")
st.sidebar.markdown(section_descriptions[section])


# ─── Page Router ──────────────────────────────────────────────
key = section.split(" ", 1)[1]   # strip emoji prefix

if key == "Overview":
    from pages.overview import show; show()
elif key == "Upload Files":
    from pages.upload import show; show()
elif key == "Run Analysis":
    from pages.analysis import show; show()
elif key == "View Records":
    from pages.records import show; show()
elif key == "Analytics":
    from pages.analytics import show; show()
elif key == "Email Report":
    from pages.email_report import show; show()
elif key == "Clear Data":
    from pages.clear_data import show; show()
