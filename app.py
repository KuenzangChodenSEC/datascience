from pathlib import Path
from io import BytesIO
import html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

# ============================================================
# GAMING PREFERENCES & HABITS | VANILLA ANALYTICS
# ============================================================
st.set_page_config(
    page_title="Gaming Insights | Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Design system: warm vanilla / sage / charcoal ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
  --vanilla: #F7F5EF;
  --paper: #FFFEFA;
  --ink: #252B27;
  --muted: #788078;
  --sage: #718675;
  --sage-dark: #536A58;
  --sage-soft: #E8EEE7;
  --line: #E7E5DC;
  --gold: #C5A66B;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: var(--vanilla); color: var(--ink); }
[data-testid="stHeader"] { background: rgba(247,245,239,.88); }
[data-testid="stToolbar"] { right: 1rem; }
.block-container { max-width: 1480px; padding-top: 2rem; padding-bottom: 3rem; }
h1, h2, h3, h4 { color: var(--ink) !important; letter-spacing: -.035em; }
h1 { font-family: 'Playfair Display', serif !important; font-size: clamp(2rem, 3vw, 2.8rem) !important; }
h2 { font-size: 1.55rem !important; font-weight: 700 !important; }
h3 { font-size: 1.12rem !important; font-weight: 700 !important; }
p, label, .stMarkdown { color: var(--ink); }
small, .muted { color: var(--muted) !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #F0EEE6;
  border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--muted); }
.brand-mark {
  width: 42px; height: 42px; border-radius: 14px;
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--sage-dark); color: #fff; font-size: 21px;
  box-shadow: 0 6px 16px rgba(83,106,88,.18);
}
.brand-title { font-weight: 700; font-size: 1.08rem; color: var(--ink); }
.brand-sub { color: var(--muted); font-size: .72rem; letter-spacing: .12em; text-transform: uppercase; }
div[role="radiogroup"] { gap: .38rem; }
div[role="radiogroup"] label {
  background: transparent; border: 1px solid transparent;
  border-radius: 11px; padding: .62rem .75rem; transition: all .2s ease;
}
div[role="radiogroup"] label:hover { background: #E7EAE1; border-color: #DCE3D9; }
div[role="radiogroup"] label:has(input:checked) {
  background: #E2E9E0; border-color: #D2DDD0; color: var(--sage-dark);
  font-weight: 700;
}

/* Hero and cards */
.hero {
  background: linear-gradient(120deg, #FFFEFA 0%, #F0F2E9 100%);
  border: 1px solid var(--line); border-radius: 22px;
  padding: 1.55rem 1.8rem; margin-bottom: 1.35rem;
  position: relative; overflow: hidden;
  animation: riseIn .65s ease both;
}
.hero:after {
  content: ''; position: absolute; width: 220px; height: 220px;
  right: -65px; top: -105px; border-radius: 50%;
  background: radial-gradient(circle, rgba(197,166,107,.18), transparent 70%);
}
.eyebrow { color: var(--sage-dark); text-transform: uppercase; letter-spacing: .16em; font-size: .68rem; font-weight: 700; }
.hero h1 { margin: .28rem 0 .35rem 0; }
.hero p { color: var(--muted); margin: 0; max-width: 760px; }
.section-kicker { color: var(--sage-dark); text-transform: uppercase; letter-spacing: .13em; font-size: .68rem; font-weight: 700; margin-bottom: .25rem; }
.metric-card {
  background: var(--paper); border: 1px solid var(--line); border-radius: 17px;
  padding: 1rem 1.1rem; min-height: 118px; position: relative; overflow: hidden;
  box-shadow: 0 3px 14px rgba(48,55,47,.035);
  transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
  animation: riseIn .55s ease both;
}
.metric-card:hover { transform: translateY(-4px); box-shadow: 0 12px 26px rgba(48,55,47,.08); border-color: #D2DCCF; }
.metric-label { color: var(--muted); font-size: .77rem; font-weight: 600; }
.metric-value { color: var(--ink); font-size: 1.8rem; line-height: 1.35; font-weight: 700; margin-top: .28rem; letter-spacing: -.04em; }
.metric-note { color: var(--sage-dark); font-size: .72rem; margin-top: .15rem; }
.metric-symbol { float: right; width: 30px; height: 30px; border-radius: 10px; background: var(--sage-soft); color: var(--sage-dark); display:flex; align-items:center; justify-content:center; font-size: 16px; }
.panel {
  background: var(--paper); border: 1px solid var(--line); border-radius: 18px;
  padding: 1.1rem 1.25rem; box-shadow: 0 3px 14px rgba(48,55,47,.025);
}
.insight {
  background: #EEF2EA; border: 1px solid #DDE6DA; border-left: 3px solid var(--sage);
  border-radius: 12px; padding: .85rem 1rem; margin: .4rem 0;
}
.pill {
  display:inline-block; padding:.28rem .62rem; border-radius:999px;
  background:#E8EEE7; color:#536A58; font-size:.72rem; font-weight:700;
}
hr { border-color: var(--line) !important; }
div[data-testid="stVerticalBlock"] > div:has(> .element-container .hero) { animation: riseIn .55s ease both; }

/* Inputs and buttons */
.stButton > button, .stDownloadButton > button {
  border-radius: 11px; border: 1px solid #D4DED2; background: #E7EDE4;
  color: #435A48; font-weight: 700; transition: all .2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  background: #D9E4D7; border-color: #B9CBB8; color: #334B39;
  transform: translateY(-1px);
}
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
  background: #FFFEFA !important; border-color: var(--line) !important; border-radius: 10px !important;
}
[data-testid="stMetric"] { background: var(--paper); border: 1px solid var(--line); padding: 1rem; border-radius: 15px; }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 12px; overflow: hidden; }
[data-testid="stAlert"] { border-radius: 12px; }
[data-testid="stPlotlyChart"] { background: var(--paper); border: 1px solid var(--line); border-radius: 16px; padding: .35rem; }
footer { visibility: hidden; }
@keyframes riseIn { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important; transition-duration: .01ms !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------- Constants ----------
DATA_PATH = Path(__file__).parent / "data" / "cleaned_gaming_survey.xlsx"
PLOT_TEMPLATE = "plotly_white"
SAGE = "#718675"
SAGE_DARK = "#536A58"
GOLD = "#C5A66B"
PALETTE = ["#718675", "#C5A66B", "#A7B8A4", "#9A8E7B", "#B9C9C0", "#D5BFA0", "#687A85"]

# ---------- Data helpers ----------
@st.cache_data(show_spinner="Preparing the survey dataset...")
def load_default_data():
    return pd.read_excel(DATA_PATH)

@st.cache_data(show_spinner=False)
def read_uploaded_file(file_name, file_bytes):
    bio = BytesIO(file_bytes)
    if file_name.lower().endswith(".csv"):
        return pd.read_csv(bio)
    return pd.read_excel(bio)

def standardise_columns(data):
    data = data.copy()
    data.columns = [str(c).strip() for c in data.columns]
    return data

def split_multi_value(series):
    return series.dropna().astype(str).str.split(",").explode().str.strip().replace("", np.nan).dropna()

def safe_numeric(data, column):
    if column not in data.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(data[column], errors="coerce")

def category_counts(data, column):
    if column not in data.columns:
        return pd.Series(dtype=int)
    return data[column].dropna().astype(str).value_counts()

def chart_style(fig, height=360):
    fig.update_layout(
        template=PLOT_TEMPLATE, height=height,
        margin=dict(l=18, r=22, t=58, b=18),
        title=dict(font=dict(size=15, color="#303A32", family="DM Sans"), x=.02),
        font=dict(family="DM Sans", color="#59645B", size=12),
        paper_bgcolor="#FFFEFA", plot_bgcolor="#FFFEFA",
        colorway=PALETTE, hoverlabel=dict(bgcolor="#FFFEFA", bordercolor="#DDE4D9", font_color="#303A32"),
        legend=dict(orientation="h", y=-.18, title_text=""),
        transition=dict(duration=450, easing="cubic-in-out"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#E7E5DC")
    fig.update_yaxes(gridcolor="#EEECE5", zeroline=False, linecolor="#E7E5DC")
    return fig

def bar_chart(data, x, y, title, horizontal=False, color=None, height=360):
    if data.empty:
        return None
    if horizontal:
        fig = px.bar(data, x=y, y=x, orientation="h", color=color, text=y, title=title,
                     color_discrete_sequence=PALETTE)
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
    else:
        fig = px.bar(data, x=x, y=y, color=color, text=y, title=title,
                     color_discrete_sequence=PALETTE)
    fig.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0,
                      hovertemplate="%{x}: %{y}<extra></extra>" if not horizontal else "%{y}: %{x}<extra></extra>")
    return chart_style(fig, height)

def show_chart(fig, key=None):
    if fig is None:
        st.info("There is not enough data to display this chart.")
    else:
        st.plotly_chart(fig, use_container_width=True, config={
            "displaylogo": False, "scrollZoom": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"]
        }, key=key)

def metric_card(label, value, note="", symbol="◈"):
    st.markdown(f"""
    <div class="metric-card">
      <span class="metric-symbol">{symbol}</span>
      <div class="metric-label">{html.escape(str(label))}</div>
      <div class="metric-value">{html.escape(str(value))}</div>
      <div class="metric-note">{html.escape(str(note))}</div>
    </div>
    """, unsafe_allow_html=True)

def section_heading(kicker, title, description=None):
    st.markdown(f'<div class="section-kicker">{html.escape(kicker)}</div>', unsafe_allow_html=True)
    st.subheader(title)
    if description:
        st.caption(description)

def insight_card(text):
    st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)

# ---------- Load dataset ----------
st.sidebar.markdown("""
<div style="display:flex;align-items:center;gap:11px;margin:0 0 5px 2px;">
  <div class="brand-mark">◈</div>
  <div><div class="brand-title">Gaming Insights</div>
  <div class="brand-sub">Research dashboard</div></div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
upload = st.sidebar.file_uploader("Replace dataset", type=["xlsx", "xls", "csv"], help="Upload a dataset with the same project columns.")

try:
    if upload is not None:
        raw_df = read_uploaded_file(upload.name, upload.getvalue())
        data_source = upload.name
    else:
        raw_df = load_default_data()
        data_source = "Cleaned project survey"
except Exception as exc:
    st.error(f"Unable to load the dataset: {exc}")
    st.stop()

raw_df = standardise_columns(raw_df)
required = ["Age", "Gender", "Play_Frequency", "Weekly_Hours", "Devices", "Genres",
            "Favorite_Game", "Play_Mode", "Monthly_Spending", "Reasons"]
missing_required = [c for c in required if c not in raw_df.columns]
if missing_required:
    st.error("The uploaded file is missing required columns: " + ", ".join(missing_required))
    st.stop()

df = raw_df.copy()
if "Age_Group" not in df.columns:
    df["Age_Group"] = pd.cut(pd.to_numeric(df["Age"], errors="coerce"),
                             bins=[0, 19, 24, 29, 34, float("inf")],
                             labels=["15-19", "20-24", "25-29", "30-34", "35+"])
if "Weekly_Hours_Num" not in df.columns:
    hour_map = {"30 minutes": .5, "Less than 5 hours": 2.5, "5-10 hours": 7.5,
                "10-20 hours": 15, "More than 20 hours": 25, "0": 0}
    df["Weekly_Hours_Num"] = df["Weekly_Hours"].map(hour_map)
if "Monthly_Spending_Num" not in df.columns:
    spend_map = {"< ₹100": 50, "Less than ₹100": 50, "₹100–500": 300,
                 "₹100-500": 300, "₹500–1,000": 750, "₹500-1,000": 750,
                 "₹1,000+": 1250, "More than ₹1000": 1250}
    df["Monthly_Spending_Num"] = df["Monthly_Spending"].map(spend_map)
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].map(lambda v: v.strip() if isinstance(v, str) else v)

# ---------- Sidebar filters ----------
st.sidebar.markdown("---")
st.sidebar.markdown("#### Refine the sample")
filtered = df.copy()

def multi_filter(label, column):
    global filtered
    if column in df.columns:
        options = sorted(df[column].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect(label, options, default=options, key=f"filter_{column}")
        filtered = filtered[filtered[column].astype(str).isin(selected)]

multi_filter("Age group", "Age_Group")
multi_filter("Gender", "Gender")
multi_filter("Gaming frequency", "Play_Frequency")
multi_filter("Location", "Location")

st.sidebar.caption(f"Displaying {len(filtered):,} of {len(df):,} responses")
if st.sidebar.button("Reset all filters", use_container_width=True):
    for key in ["filter_Age_Group", "filter_Gender", "filter_Play_Frequency", "filter_Location"]:
        st.session_state.pop(key, None)
    st.rerun()

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "WORKSPACE",
    ["Overview", "Demographics", "Gaming behaviour", "Preferences", "Research analysis", "Data explorer"],
    label_visibility="visible",
)
st.sidebar.markdown("---")
st.sidebar.caption("GAMING PREFERENCES & HABITS")
st.sidebar.caption("Interactive survey analysis · 500-response project")

# ---------- Global hero ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">Survey analytics · Research project</div>
  <h1>Gaming preferences &amp; habits</h1>
  <p>Explore how respondents play, what they prefer, and how gaming patterns relate to age, frequency and spending.</p>
</div>
""", unsafe_allow_html=True)
st.markdown(
    f'<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:-.55rem 0 1.1rem 2px;">'
    f'<span class="muted" style="font-size:.76rem;">Source: {html.escape(data_source)}</span>'
    f'<span class="pill">{len(filtered):,} responses in current view</span></div>',
    unsafe_allow_html=True
)

if filtered.empty:
    st.warning("No responses match these filters. Adjust the filters in the sidebar.")
    st.stop()

# ---------- Overview ----------
if page == "Overview":
    section_heading("At a glance", "A snapshot of the survey", "Key indicators update automatically when you change the filters.")
    avg_age = safe_numeric(filtered, "Age").mean()
    avg_hours = safe_numeric(filtered, "Weekly_Hours_Num").mean()
    daily = int((filtered["Play_Frequency"] == "Daily").sum())
    daily_pct = daily / len(filtered) * 100 if len(filtered) else 0
    k = st.columns(4)
    with k[0]: metric_card("Respondents", f"{len(filtered):,}", "Responses in this view", "▤")
    with k[1]: metric_card("Average age", f"{avg_age:.1f}" if pd.notna(avg_age) else "—", "Years", "◷")
    with k[2]: metric_card("Daily gamers", f"{daily:,}", f"{daily_pct:.1f}% of this sample", "↗")
    with k[3]: metric_card("Estimated weekly hours", f"{avg_hours:.1f}" if pd.notna(avg_hours) else "—", "Hours · midpoint estimate", "◴")

    st.markdown("")
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        freq = category_counts(filtered, "Play_Frequency").rename_axis("Frequency").reset_index(name="Respondents")
        fig = px.pie(freq, names="Frequency", values="Respondents", hole=.64,
                     title="Gaming frequency", color_discrete_sequence=PALETTE)
        fig.update_traces(textposition="inside", textinfo="percent", marker=dict(line=dict(color="#FFFEFA", width=3)))
        show_chart(chart_style(fig, 355), "overview_frequency")
    with right:
        ages = category_counts(filtered, "Age_Group").rename_axis("Age group").reset_index(name="Respondents")
        show_chart(bar_chart(ages, "Age group", "Respondents", "Respondents by age group", height=355), "overview_age")

    section_heading("Highlights", "What stands out in this sample")
    cols = st.columns(2)
    findings = [
        ("Most common frequency", category_counts(filtered, "Play_Frequency")),
        ("Largest age group", category_counts(filtered, "Age_Group")),
        ("Most common play mode", category_counts(filtered, "Play_Mode")),
        ("Most reported favourite game", category_counts(filtered, "Favorite_Game")),
    ]
    for i, (label, series) in enumerate(findings):
        with cols[i % 2]:
            if not series.empty:
                insight_card(f"<strong>{html.escape(label)}:</strong> {html.escape(str(series.index[0]))} <span style='color:#718675'>· {int(series.iloc[0])} responses</span>")
    st.caption("Findings describe this survey sample only and should not automatically be generalised to all gamers.")

# ---------- Demographics ----------
elif page == "Demographics":
    section_heading("Respondent profile", "Demographics", "Explore the age, gender and location profile of the respondents.")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        age_values = safe_numeric(filtered, "Age").dropna()
        if not age_values.empty:
            fig = px.histogram(filtered, x="Age", nbins=15, title="Age distribution",
                               color_discrete_sequence=[SAGE], marginal="box")
            fig.update_traces(marker_line_color="#FFFEFA", marker_line_width=1)
            show_chart(chart_style(fig, 380), "demo_age")
            st.caption(f"Mean: {age_values.mean():.1f} years · Median: {age_values.median():.0f} years")
    with c2:
        gender = category_counts(filtered, "Gender").rename_axis("Gender").reset_index(name="Respondents")
        fig = px.pie(gender, names="Gender", values="Respondents", hole=.58,
                     title="Respondents by gender", color_discrete_sequence=PALETTE)
        fig.update_traces(textposition="outside", textinfo="label+percent",
                          marker=dict(line=dict(color="#FFFEFA", width=3)))
        show_chart(chart_style(fig, 380), "demo_gender")
    c3, c4 = st.columns(2, gap="large")
    with c3:
        groups = category_counts(filtered, "Age_Group").rename_axis("Age group").reset_index(name="Respondents")
        show_chart(bar_chart(groups, "Age group", "Respondents", "Age-group distribution"), "demo_groups")
    with c4:
        if "Location" in filtered.columns:
            loc = category_counts(filtered, "Location").head(12).rename_axis("Location").reset_index(name="Respondents")
            show_chart(bar_chart(loc, "Location", "Respondents", "Top 12 reported locations", True), "demo_locations")

# ---------- Behaviour ----------
elif page == "Gaming behaviour":
    section_heading("Play patterns", "Gaming behaviour", "Compare how often respondents play, how long they play and how they access games.")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        freq = category_counts(filtered, "Play_Frequency").rename_axis("Frequency").reset_index(name="Respondents")
        show_chart(bar_chart(freq, "Frequency", "Respondents", "Gaming frequency", True), "behaviour_frequency")
    with c2:
        hours = category_counts(filtered, "Weekly_Hours").rename_axis("Weekly hours").reset_index(name="Respondents")
        show_chart(bar_chart(hours, "Weekly hours", "Respondents", "Weekly gaming hours", True), "behaviour_hours")
    c3, c4 = st.columns(2, gap="large")
    with c3:
        mode = category_counts(filtered, "Play_Mode").rename_axis("Play mode").reset_index(name="Respondents")
        fig = px.pie(mode, names="Play mode", values="Respondents", hole=.58,
                     title="Preferred play mode", color_discrete_sequence=PALETTE)
        fig.update_traces(marker=dict(line=dict(color="#FFFEFA", width=3)))
        show_chart(chart_style(fig, 360), "behaviour_mode")
    with c4:
        spend = category_counts(filtered, "Monthly_Spending").rename_axis("Monthly spending").reset_index(name="Respondents")
        show_chart(bar_chart(spend, "Monthly spending", "Respondents", "Monthly gaming expenditure", True), "behaviour_spend")
    hours_avg = safe_numeric(filtered, "Weekly_Hours_Num").mean()
    st.markdown("")
    insight_card(f"<strong>Estimated average weekly gaming time:</strong> {hours_avg:.2f} hours per respondent." if pd.notna(hours_avg) else "Weekly gaming hour estimates are unavailable.")
    st.caption("Weekly hours and spending values are category-midpoint estimates, not exact amounts reported by respondents.")

# ---------- Preferences ----------
elif page == "Preferences":
    section_heading("What respondents enjoy", "Gaming preferences", "Multi-select questions count each selected option separately, so totals may exceed the number of respondents.")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        genres = split_multi_value(filtered["Genres"]).value_counts().head(12).rename_axis("Genre").reset_index(name="Selections")
        show_chart(bar_chart(genres, "Genre", "Selections", "Most selected game genres", True), "pref_genres")
    with c2:
        devices = split_multi_value(filtered["Devices"]).value_counts().head(12).rename_axis("Device").reset_index(name="Selections")
        show_chart(bar_chart(devices, "Device", "Selections", "Gaming devices used", True), "pref_devices")
    c3, c4 = st.columns(2, gap="large")
    with c3:
        games = category_counts(filtered, "Favorite_Game").head(10).rename_axis("Game").reset_index(name="Respondents")
        show_chart(bar_chart(games, "Game", "Respondents", "Most reported favourite games", True), "pref_games")
    with c4:
        reasons = split_multi_value(filtered["Reasons"]).value_counts().head(10).rename_axis("Reason").reset_index(name="Selections")
        show_chart(bar_chart(reasons, "Reason", "Selections", "Reasons for playing", True), "pref_reasons")
    if "Discovery" in filtered.columns:
        discovery = split_multi_value(filtered["Discovery"]).value_counts().head(10).rename_axis("Discovery source").reset_index(name="Selections")
        show_chart(bar_chart(discovery, "Discovery source", "Selections", "How respondents discover games", True), "pref_discovery")

# ---------- Research analysis ----------
elif page == "Research analysis":
    section_heading("Evidence and interpretation", "Research analysis", "Statistical tests are recalculated for the current filtered sample.")
    st.warning("Weekly hours and monthly spending are estimated from response-category midpoints. Interpret these tests cautiously. Association does not establish causation.")
    alpha = st.select_slider("Significance level (α)", options=[0.01, 0.05, 0.10], value=0.05)
    st.markdown("#### Hypothesis 1 · Age group and weekly gaming hours")
    st.markdown("**H₀:** Estimated weekly gaming hours do not differ across age groups.  \n**H₁:** At least one age group differs.")
    h1 = filtered[["Age_Group", "Weekly_Hours_Num"]].copy()
    h1["Weekly_Hours_Num"] = pd.to_numeric(h1["Weekly_Hours_Num"], errors="coerce")
    h1 = h1.dropna()
    groups = [g["Weekly_Hours_Num"].values for _, g in h1.groupby("Age_Group", observed=True) if len(g)]
    if len(groups) >= 2:
        stat, p = stats.kruskal(*groups)
        a, b, c = st.columns(3)
        a.metric("Kruskal–Wallis H", f"{stat:.3f}")
        b.metric("p-value", f"{p:.4f}")
        c.metric("Decision", "Reject H₀" if p < alpha else "Do not reject H₀")
        avg = h1.groupby("Age_Group", observed=True)["Weekly_Hours_Num"].mean().reset_index(name="Average hours")
        fig = px.bar(avg, x="Age_Group", y="Average hours", title="Average estimated weekly hours by age group",
                     color="Age_Group", color_discrete_sequence=PALETTE, text_auto=".1f")
        show_chart(chart_style(fig), "test_age_hours")
        st.caption("Interpretation: " + ("Evidence suggests at least one age group differs in estimated weekly gaming hours." if p < alpha else "The sample does not provide sufficient evidence of a difference across age groups."))
    else:
        st.info("At least two age groups with valid hour estimates are needed.")

    st.markdown("---")
    st.markdown("#### Hypothesis 2 · Weekly gaming hours and monthly spending")
    st.markdown("**H₀:** There is no monotonic association between estimated weekly hours and monthly spending.  \n**H₁:** A monotonic association exists.")
    h2 = filtered[["Weekly_Hours_Num", "Monthly_Spending_Num"]].apply(pd.to_numeric, errors="coerce").dropna()
    if len(h2) >= 3 and h2.nunique().min() > 1:
        rho, p2 = stats.spearmanr(h2["Weekly_Hours_Num"], h2["Monthly_Spending_Num"])
        a, b, c = st.columns(3)
        a.metric("Spearman's ρ", f"{rho:.3f}")
        b.metric("p-value", f"{p2:.4f}")
        c.metric("Decision", "Reject H₀" if p2 < alpha else "Do not reject H₀")
        fig = px.scatter(h2, x="Weekly_Hours_Num", y="Monthly_Spending_Num",
                         title="Estimated weekly hours and monthly spending",
                         labels={"Weekly_Hours_Num": "Estimated weekly hours", "Monthly_Spending_Num": "Estimated monthly spending (₹)"},
                         color_discrete_sequence=[SAGE], opacity=.65, marginal_x="histogram", marginal_y="box")
        show_chart(chart_style(fig, 410), "test_hours_spending")
        st.caption("Interpretation: " + (f"The estimates show a {'positive' if rho > 0 else 'negative'} monotonic association." if p2 < alpha else "There is insufficient evidence of a monotonic association in this sample."))
    else:
        st.info("There are not enough varied hour and spending estimates for this test.")

    st.markdown("---")
    st.markdown("#### Hypothesis 3 · Age group and gaming frequency")
    st.markdown("**H₀:** Age group and gaming frequency are independent.  \n**H₁:** Age group and gaming frequency are associated.")
    h3 = filtered[["Age_Group", "Play_Frequency"]].dropna()
    table = pd.crosstab(h3["Age_Group"], h3["Play_Frequency"])
    if table.shape[0] >= 2 and table.shape[1] >= 2:
        chi2, p3, dof, expected = stats.chi2_contingency(table)
        a, b, c = st.columns(3)
        a.metric("Chi-square", f"{chi2:.3f}")
        b.metric("p-value", f"{p3:.4f}")
        c.metric("Decision", "Reject H₀" if p3 < alpha else "Do not reject H₀")
        pct = pd.crosstab(h3["Age_Group"], h3["Play_Frequency"], normalize="index").reset_index()
        long_pct = pct.melt(id_vars="Age_Group", var_name="Frequency", value_name="Share")
        fig = px.bar(long_pct, x="Age_Group", y="Share", color="Frequency", barmode="stack",
                     title="Gaming frequency within each age group", color_discrete_sequence=PALETTE)
        fig.update_yaxes(tickformat=".0%")
        show_chart(chart_style(fig), "test_age_frequency")
        st.dataframe(table, use_container_width=True)
        if (expected < 5).any():
            st.warning("Some expected cell counts are below 5. Interpret the chi-square result cautiously.")
        st.caption("Interpretation: " + ("Evidence suggests an association between age group and gaming frequency." if p3 < alpha else "There is insufficient evidence of an association in this sample."))
    else:
        st.info("At least two age groups and two gaming-frequency categories are required.")

    st.markdown("---")
    st.markdown("#### Additional comparison · Gender and gaming frequency")
    gender_table = pd.crosstab(filtered["Gender"], filtered["Play_Frequency"])
    if gender_table.shape[0] >= 2 and gender_table.shape[1] >= 2:
        gchi, gp, gdof, gexpected = stats.chi2_contingency(gender_table)
        a, b = st.columns(2)
        a.metric("Chi-square p-value", f"{gp:.4f}")
        b.metric("Decision at selected α", "Reject H₀" if gp < alpha else "Do not reject H₀")
        if (gexpected < 5).any():
            st.warning("Some expected counts are below 5; interpret this comparison cautiously.")
        st.dataframe(gender_table, use_container_width=True)

# ---------- Data explorer ----------
elif page == "Data explorer":
    section_heading("Inspect the source", "Data explorer", "Search, filter, inspect data quality and export the selected records.")
    search_text = st.text_input("Search all visible columns", placeholder="Try a game title, location, device or gender...")
    display_df = filtered.copy()
    if search_text.strip():
        mask = display_df.astype(str).apply(lambda col: col.str.contains(search_text, case=False, na=False)).any(axis=1)
        display_df = display_df[mask]
    a, b, c = st.columns(3)
    a.metric("Matching records", f"{len(display_df):,}")
    b.metric("Missing cells", f"{int(raw_df.isna().sum().sum()):,}")
    c.metric("Duplicate rows", f"{int(raw_df.duplicated().sum()):,}")
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=430)
    csv_data = display_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Download filtered records · CSV", data=csv_data,
                       file_name="gaming_survey_filtered.csv", mime="text/csv")
    st.markdown("#### Data quality profile")
    quality = pd.DataFrame({
        "Column": raw_df.columns,
        "Data type": [str(t) for t in raw_df.dtypes],
        "Missing values": [int(raw_df[c].isna().sum()) for c in raw_df.columns],
        "Unique values": [int(raw_df[c].nunique(dropna=True)) for c in raw_df.columns],
    })
    st.dataframe(quality, use_container_width=True, hide_index=True)

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:#858B82;font-size:.72rem;">
  <span>GAMING PREFERENCES &amp; HABITS · INTERACTIVE RESEARCH DASHBOARD</span>
  <span>Prepared for academic data exploration · Vanilla / Sage design</span>
</div>
""", unsafe_allow_html=True)
