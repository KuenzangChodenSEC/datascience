from pathlib import Path
from io import BytesIO
import base64
import html
import textwrap

import numpy as np
import pandas as pd
import plotly.express as px
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

ASSET_DIR = Path(__file__).parent / "assets"
ARTWORKS = {
    "dashboard_feature": ASSET_DIR / "24c43180662d27aa5b62106b596fa4f7.webp",
    "dashboard_mid": ASSET_DIR / "9ea138369ca4a37b4806ac64998df054.webp",
    "dashboard_lower": ASSET_DIR / "3a7693b9a565b4e1d67d57ae73eb5297.webp",
    "sidebar": ASSET_DIR / "Alucard-min-1024x576.png",
    "research_feature": ASSET_DIR / "julian_mobile_legends_png_transparan_by_dechunf_df6wpq8-fullview.png",
    "research_mid": ASSET_DIR / "Alucard-min-1024x576.png",
}

# ---------- Safe HTML renderer ----------
# textwrap.dedent is important: indented HTML inside st.markdown()
# can otherwise be interpreted as a Markdown code block.
def render_html(markup: str):
    st.markdown(textwrap.dedent(markup).strip(), unsafe_allow_html=True)


def render_static_table(data: pd.DataFrame):
    table_html = data.to_html(classes="static-table", border=0, escape=True)
    render_html(f'<div class="static-table-wrap">{table_html}</div>')


def background_art_style():
    layers = [
        ("sidebar", "3% 82%", "min(17vw, 28vh) auto"),
        ("dashboard_feature", "31% 8%", "min(28vw, 38vh) auto"),
        ("dashboard_mid", "96% 32%", "min(27vw, 38vh) auto"),
        ("dashboard_lower", "82% 94%", "min(25vw, 36vh) auto"),
        ("research_feature", "22% 68%", "min(25vw, 36vh) auto"),
        ("research_mid", "62% 92%", "min(22vw, 34vh) auto"),
    ]
    image_types = {
        ".webp": "image/webp",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }
    image_urls = []
    positions = []
    sizes = []
    for name, position, size in layers:
        image_path = ARTWORKS[name]
        image_type = image_types[image_path.suffix.lower()]
        image_data = base64.b64encode(image_path.read_bytes()).decode("ascii")
        image_urls.append(f'url("data:{image_type};base64,{image_data}")')
        positions.append(position)
        sizes.append(size)
    return f"""
<style>
.stApp {{ isolation:isolate; }}
.stApp::before {{
  content:"";
  position:fixed;
  inset:0;
  z-index:0;
  pointer-events:none;
  opacity:.25;
  mix-blend-mode:screen;
  background-image:{", ".join(image_urls)};
  background-size:{", ".join(sizes)};
  background-position:{", ".join(positions)};
  background-repeat:no-repeat;
}}
[data-testid="stAppViewContainer"] {{ position:relative; z-index:1; }}
</style>
"""


# ---------- Design system: warm vanilla / sage / charcoal ----------
render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700&family=Rajdhani:wght@400;500;600;700&display=swap');
:root { --bg:#090611; --panel:#171027; --panel2:#211538; --text:#F8F3FF; --muted:#B9A8D0; --cyan:#B026FF; --purple:#7B2CFF; --pink:#FF3CAC; --line:rgba(125,146,205,.18); }
html, body, [class*="css"] { font-family:'Rajdhani',sans-serif; }
.stApp { background:radial-gradient(circle at 82% 8%,rgba(176,38,255,.24),transparent 28%),radial-gradient(circle at 20% 0%,rgba(255,60,172,.12),transparent 24%),var(--bg); color:var(--text); }
[data-testid="stHeader"] { background:rgba(8,11,22,.82); }
.block-container { max-width:1500px; padding-top:1.5rem; padding-bottom:3rem; }
h1,h2,h3 { color:var(--text)!important; font-family:'Orbitron',sans-serif!important; letter-spacing:.02em; }
p,label,.stMarkdown { color:var(--text); }
section[data-testid="stSidebar"] { background:linear-gradient(180deg,rgba(18,10,34,.82),rgba(9,6,17,.84)); border-right:1px solid var(--line); }
.brand-mark { width:44px;height:44px;border-radius:12px;display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--purple),var(--purple));color:#07101A;font-size:20px;box-shadow:0 0 25px rgba(176,38,255,.35); }
.brand-title { font-family:'Orbitron',sans-serif;font-weight:700;color:#fff; } .brand-sub,.muted { color:var(--muted)!important; }
div[role="radiogroup"] label { border-radius:10px;padding:.62rem .75rem; } div[role="radiogroup"] label:has(input:checked){background:linear-gradient(90deg,rgba(176,38,255,.20),rgba(255,60,172,.16));border:1px solid rgba(176,38,255,.48);color:#fff; }
.hero { background:linear-gradient(110deg,rgba(17,22,42,.96),rgba(23,29,53,.82));border:1px solid var(--line);border-radius:22px;padding:1.5rem 1.8rem;margin-bottom:1.1rem;position:relative;overflow:hidden;box-shadow:0 18px 55px rgba(0,0,0,.22); }
.eyebrow,.section-kicker { color:var(--purple);text-transform:uppercase;letter-spacing:.16em;font-size:.72rem;font-weight:700; }
.metric-card,[data-testid="stMetric"] { background:rgba(17,22,42,.92)!important;border:1px solid var(--line)!important;border-radius:16px!important;box-shadow:0 10px 30px rgba(0,0,0,.16); }
[data-testid="stPlotlyChart"] { background:transparent!important;border:1px solid var(--line)!important;border-radius:16px!important;box-shadow:0 10px 30px rgba(0,0,0,.16); }
.metric-card { padding:1rem 1.1rem;min-height:108px; } .metric-label,.metric-note { color:var(--muted); } .metric-value { color:#fff;font-size:1.8rem;font-weight:700; } .metric-symbol{float:right;color:var(--purple);}
.pill { display:inline-block;padding:.3rem .7rem;border-radius:999px;background:rgba(0,229,255,.10);border:1px solid rgba(0,229,255,.2);color:var(--purple);font-weight:700; }
.stButton>button,.stDownloadButton>button { background:linear-gradient(90deg,var(--purple),#4D7CFE);color:#07101A;border:0;border-radius:10px;font-weight:700; }
.stTextInput input,.stSelectbox div[data-baseweb="select"]>div,.stMultiSelect div[data-baseweb="select"]>div { background:#10162A!important;color:#fff!important;border-color:var(--line)!important; }
.static-table-wrap { width:100%; overflow-x:auto; border:1px solid var(--line); border-radius:12px; }
.static-table { width:100%; border-collapse:collapse; background:rgba(17,22,42,.92); color:var(--text); }
.static-table th,.static-table td { padding:.55rem .75rem; border-bottom:1px solid var(--line); text-align:left; white-space:nowrap; }
.static-table th { background:var(--panel2); color:#fff; }
.static-table tbody tr:nth-child(even) { background:rgba(255,255,255,.025); }
footer { visibility:hidden; }
</style>
""" + background_art_style())

# ---------- Constants ----------
DATA_PATH = Path(__file__).parent / "data" / "cleaned_gaming_survey.xlsx"
PLOT_TEMPLATE = "plotly_dark"
SAGE = "#B026FF"
SAGE_DARK = "#7B2CFF"
GOLD = "#FFD166"
PALETTE = ["#B026FF", "#7B2CFF", "#FF3CAC", "#9D4EDD", "#C77DFF", "#F72585", "#7209B7"]


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
    return (
        series.dropna().astype(str).str.split(",").explode()
        .str.strip().replace("", np.nan).dropna()
    )


def safe_numeric(data, column):
    if column not in data.columns:
        return pd.Series(dtype=float)
    return pd.to_numeric(data[column], errors="coerce")


def category_counts(data, column):
    if column not in data.columns:
        return pd.Series(dtype=int)
    return data[column].dropna().astype(str).value_counts()


def chart_style(fig, height=360):
    has_legend = fig.layout.showlegend is True or any(
        getattr(trace, "showlegend", False) for trace in fig.data
    )
    fig.update_layout(
        template=PLOT_TEMPLATE,
        height=height,
        margin=dict(l=18, r=22, t=58, b=100 if has_legend else 18),
        title=dict(font=dict(size=15, color="#F4F7FF", family="Orbitron"), x=.02),
        font=dict(family="Rajdhani", color="#C8D2EB", size=13),
        paper_bgcolor="rgba(17,22,42,.90)",
        plot_bgcolor="rgba(17,22,42,.90)",
        colorway=PALETTE,
        hoverlabel=dict(bgcolor="#171D35", bordercolor="#B026FF", font_color="#F4F7FF"),
        legend=dict(orientation="h", y=-.12, yanchor="top", x=.01, xanchor="left", title_text="Legend", bgcolor="rgba(23,16,39,.75)", bordercolor="#7B2CFF", borderwidth=1),
        # Disable Plotly's animated transitions.
        transition=dict(duration=0),
        uirevision="gaming-insights-stable",
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="#34405F")
    fig.update_yaxes(gridcolor="#26314D", zeroline=False, linecolor="#34405F")
    return fig


def bar_chart(data, x, y, title, horizontal=False, color=None, height=360):
    if data.empty:
        return None
    if horizontal:
        fig = px.bar(
            data, x=y, y=x, orientation="h", color=color, text=y,
            title=title, color_discrete_sequence=PALETTE
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
    else:
        fig = px.bar(
            data, x=x, y=y, color=color, text=y,
            title=title, color_discrete_sequence=PALETTE
        )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        hovertemplate="%{x}: %{y}<extra></extra>" if not horizontal else "%{y}: %{x}<extra></extra>",
    )
    return chart_style(fig, height)


def show_chart(fig, key=None):
    if fig is None:
        st.info("There is not enough data to display this chart.")
    else:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "scrollZoom": False,
                "staticPlot": False,
                "modeBarButtonsToRemove": ["lasso2d", "select2d"],
            },
            key=key,
        )


def metric_card(label, value, note="", symbol="◈"):
    render_html(f"""
    <div class="metric-card">
      <span class="metric-symbol">{html.escape(str(symbol))}</span>
      <div class="metric-label">{html.escape(str(label))}</div>
      <div class="metric-value">{html.escape(str(value))}</div>
      <div class="metric-note">{html.escape(str(note))}</div>
    </div>
    """)


def section_heading(kicker, title, description=None):
    render_html(f'<div class="section-kicker">{html.escape(kicker)}</div>')
    st.subheader(title)
    if description:
        st.caption(description)


def insight_card(content):
    render_html(f'<div class="insight">{content}</div>')


# ---------- Sidebar: workspace first ----------
render_html("""
<div style="display:flex;align-items:center;gap:11px;margin:0 0 5px 2px;">
  <div class="brand-mark">◈</div><div><div class="brand-title">Gaming Insights</div><div class="brand-sub">Research dashboard</div></div>
</div>""")
st.sidebar.markdown("---")
page = st.sidebar.radio("WORKSPACE", ["Dashboard", "Research analysis"], label_visibility="visible")
st.sidebar.markdown("---")

upload = st.sidebar.file_uploader("Replace dataset", type=["xlsx", "xls", "csv"], help="Upload a dataset with the same project columns.")
try:
    if upload is not None:
        raw_df = read_uploaded_file(upload.name, upload.getvalue()); data_source = upload.name
    else:
        raw_df = load_default_data(); data_source = "Cleaned project survey"
except Exception as exc:
    st.error(f"Unable to load the dataset: {exc}"); st.stop()
raw_df = standardise_columns(raw_df)
required = ["Age", "Gender", "Play_Frequency", "Weekly_Hours", "Devices", "Genres", "Favorite_Game", "Play_Mode", "Monthly_Spending", "Reasons"]
missing_required = [column for column in required if column not in raw_df.columns]
if missing_required:
    st.error("The uploaded file is missing required columns: " + ", ".join(missing_required)); st.stop()
df = raw_df.copy()
if "Age_Group" not in df.columns:
    df["Age_Group"] = pd.cut(pd.to_numeric(df["Age"], errors="coerce"), bins=[0,19,24,29,34,float("inf")], labels=["15-19","20-24","25-29","30-34","35+"])
if "Weekly_Hours_Num" not in df.columns:
    df["Weekly_Hours_Num"] = df["Weekly_Hours"].map({"30 minutes":.5,"Less than 5 hours":2.5,"5-10 hours":7.5,"10-20 hours":15,"More than 20 hours":25,"0":0})
if "Monthly_Spending_Num" not in df.columns:
    df["Monthly_Spending_Num"] = df["Monthly_Spending"].map({"< ₹100":50,"Less than ₹100":50,"₹100–500":300,"₹100-500":300,"₹500–1,000":750,"₹500-1,000":750,"₹1,000+":1250,"More than ₹1000":1250})
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].map(lambda value: value.strip() if isinstance(value,str) else value)

st.sidebar.markdown("#### Refine the sample")
filtered = df.copy()
def multi_filter(label,column):
    global filtered
    if column in df.columns:
        options=sorted(df[column].dropna().astype(str).unique().tolist())
        selected=st.sidebar.multiselect(label,options,default=options,key=f"filter_{column}")
        filtered=filtered[filtered[column].astype(str).isin(selected)]
multi_filter("Age group","Age_Group"); multi_filter("Gender","Gender"); multi_filter("Gaming frequency","Play_Frequency"); multi_filter("Location","Location")
st.sidebar.caption(f"Displaying {len(filtered):,} of {len(df):,} responses")
if st.sidebar.button("Reset all filters", use_container_width=True):
    for key in ["filter_Age_Group", "filter_Gender", "filter_Play_Frequency", "filter_Location"]:
        st.session_state.pop(key, None)
    st.rerun()
# ---------- Global hero ----------
render_html("""
<div class="hero">
  <div class="eyebrow">Survey analytics · Research project</div>
  <h1>Gaming preferences &amp; habits</h1>

</div>
""")

render_html(f"""
<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:-.55rem 0 1.1rem 2px;">
  <span class="muted" style="font-size:.76rem;">Source: {html.escape(str(data_source))}</span>
  <span class="pill">{len(filtered):,} responses in current view</span>
</div>
""")

if filtered.empty:
    st.warning("No responses match these filters. Adjust the filters in the sidebar.")
    st.stop()


# ---------- Dashboard ----------
if page == "Dashboard":
    # Decorative transparent artwork: all supplied images are blended into the dashboard.
    section_heading("LIVE GAMING ANALYTICS", "Dashboard")
    avg_age=safe_numeric(filtered,"Age").mean(); avg_hours=safe_numeric(filtered,"Weekly_Hours_Num").mean()
    daily=int((filtered["Play_Frequency"]=="Daily").sum()); daily_pct=daily/len(filtered)*100 if len(filtered) else 0
    k=st.columns(4)
    with k[0]: metric_card("Respondents",f"{len(filtered):,}",symbol="▤")
    with k[1]: metric_card("Average age",f"{avg_age:.1f}" if pd.notna(avg_age) else "—",symbol="◷")
    with k[2]: metric_card("Daily gamers",f"{daily_pct:.1f}%",symbol="↗")
    with k[3]: metric_card("Weekly hours",f"{avg_hours:.1f}" if pd.notna(avg_hours) else "—",symbol="◴")

    charts=[]
    age_values=safe_numeric(filtered,"Age").dropna()
    if not age_values.empty:
        fig=px.histogram(filtered,x="Age",nbins=15,title="Age Distribution",color_discrete_sequence=["#B026FF"])
        fig.update_traces(name="Respondents", marker_line_color="#211538",marker_line_width=1); charts.append((fig,"dash_age"))
    gender=category_counts(filtered,"Gender").rename_axis("Gender").reset_index(name="Respondents")
    if not gender.empty:
        fig=px.pie(gender,names="Gender",values="Respondents",hole=.55,title="Respondents by Gender",color="Gender",color_discrete_sequence=PALETTE); charts.append((fig,"dash_gender"))
    groups=category_counts(filtered,"Age_Group").rename_axis("Age group").reset_index(name="Respondents")
    if not groups.empty:
        fig=px.area(groups,x="Age group",y="Respondents",title="Age-group Distribution",markers=True,color_discrete_sequence=["#7B2CFF"]); fig.update_traces(name="Age groups"); charts.append((fig,"dash_groups"))
    if "Location" in filtered.columns:
        loc=category_counts(filtered,"Location").head(12).rename_axis("Location").reset_index(name="Respondents")
        fig=px.treemap(loc,path=["Location"],values="Respondents",color="Respondents",title="Top Reported Locations",color_continuous_scale="Purples"); charts.append((fig,"dash_locations"))
    freq=category_counts(filtered,"Play_Frequency").rename_axis("Frequency").reset_index(name="Respondents")
    if not freq.empty:
        fig=px.line_polar(freq,r="Respondents",theta="Frequency",line_close=True,title="Gaming Frequency",color_discrete_sequence=["#FF3CAC"]); fig.update_traces(fill="toself",name="Gaming frequency"); charts.append((fig,"dash_frequency"))
    hours=category_counts(filtered,"Weekly_Hours").rename_axis("Weekly hours").reset_index(name="Respondents")
    if not hours.empty:
        fig=px.funnel(hours,x="Respondents",y="Weekly hours",title="Weekly Gaming Hours",color="Weekly hours",color_discrete_sequence=PALETTE); charts.append((fig,"dash_hours"))
    mode=category_counts(filtered,"Play_Mode").rename_axis("Play mode").reset_index(name="Respondents")
    if not mode.empty:
        fig=px.sunburst(mode,path=["Play mode"],values="Respondents",color="Respondents",title="Preferred Play Mode",color_continuous_scale="Purples"); charts.append((fig,"dash_mode"))
    spend=category_counts(filtered,"Monthly_Spending").rename_axis("Monthly spending").reset_index(name="Respondents")
    if not spend.empty:
        fig=px.bar(spend,x="Monthly spending",y="Respondents",color="Monthly spending",title="Monthly Gaming Expenditure",color_discrete_sequence=PALETTE); charts.append((fig,"dash_spend"))
    genres=split_multi_value(filtered["Genres"]).value_counts().head(12).rename_axis("Genre").reset_index(name="Selections")
    if not genres.empty:
        fig=px.treemap(genres,path=["Genre"],values="Selections",color="Selections",title="Most Selected Game Genres",color_continuous_scale="Purples"); charts.append((fig,"dash_genres"))
    devices=split_multi_value(filtered["Devices"]).value_counts().head(12).rename_axis("Device").reset_index(name="Selections")
    if not devices.empty:
        fig=px.pie(devices,names="Device",values="Selections",title="Gaming Devices Used",color="Device",color_discrete_sequence=PALETTE); charts.append((fig,"dash_devices"))
    games=category_counts(filtered,"Favorite_Game").head(10).rename_axis("Game").reset_index(name="Respondents")
    if not games.empty:
        fig=px.bar(games,x="Respondents",y="Game",orientation="h",color="Game",title="Most Reported Favourite Games",color_discrete_sequence=PALETTE); charts.append((fig,"dash_games"))
    reasons=split_multi_value(filtered["Reasons"]).value_counts().head(10).rename_axis("Reason").reset_index(name="Selections")
    if not reasons.empty:
        fig=px.bar(reasons,x="Reason",y="Selections",color="Reason",title="Reasons for Playing",color_discrete_sequence=PALETTE); charts.append((fig,"dash_reasons"))
    if "Discovery" in filtered.columns:
        discovery=split_multi_value(filtered["Discovery"]).value_counts().head(10).rename_axis("Discovery source").reset_index(name="Selections")
        if not discovery.empty:
            fig=px.scatter(discovery,x="Discovery source",y="Selections",size="Selections",color="Discovery source",title="How Respondents Discover Games",color_discrete_sequence=PALETTE); charts.append((fig,"dash_discovery"))

    # 3D visualization: suitable for the two numerical gaming measures.
    h3d=filtered[["Age","Weekly_Hours_Num","Monthly_Spending_Num"]].copy()
    h3d=h3d.apply(pd.to_numeric,errors="coerce").dropna()
    if len(h3d) >= 3:
        fig=px.scatter_3d(h3d,x="Age",y="Weekly_Hours_Num",z="Monthly_Spending_Num",color="Age",title="3D Gaming Profile",color_continuous_scale="Plasma")
        fig.update_traces(marker=dict(size=5)); charts.append((fig,"dash_3d"))
    for i in range(0,len(charts),2):
        cols=st.columns(2,gap="large")
        for j,(fig,key) in enumerate(charts[i:i+2]):
            with cols[j]: show_chart(chart_style(fig,400) if fig is not None else None,key)
# ---------- Research analysis ----------
elif page == "Research analysis":
    section_heading(
        "Evidence and interpretation",
        "Research analysis",
        "Statistical tests are recalculated for the current filtered sample.",
    )
    st.warning(
        "Weekly hours and monthly spending are estimated from response-category midpoints. "
        
    )
    alpha = st.select_slider("Significance level (α)", options=[0.01, 0.05, 0.10], value=0.05)

    st.markdown("#### Hypothesis 1 · Age group and weekly gaming hours")
    st.markdown(
        "**H₀:** Estimated weekly gaming hours do not differ across age groups.  \n"
        "**H₁:** At least one age group differs."
    )
    h1 = filtered[["Age_Group", "Weekly_Hours_Num"]].copy()
    h1["Weekly_Hours_Num"] = pd.to_numeric(h1["Weekly_Hours_Num"], errors="coerce")
    h1 = h1.dropna()
    groups = [group["Weekly_Hours_Num"].values for _, group in h1.groupby("Age_Group", observed=True) if len(group)]
    if len(groups) >= 2:
        stat, p = stats.kruskal(*groups)
        a, b, c = st.columns(3)
        a.metric("Kruskal–Wallis H", f"{stat:.3f}")
        b.metric("p-value", f"{p:.4f}")
        c.metric("Decision", "Reject H₀" if p < alpha else "Do not reject H₀")
        avg = h1.groupby("Age_Group", observed=True)["Weekly_Hours_Num"].mean().reset_index(name="Average hours")
        fig = px.bar(
            avg, x="Age_Group", y="Average hours",
            title="Average estimated weekly hours by age group",
            color="Age_Group", color_discrete_sequence=PALETTE, text_auto=".1f",
        )
        show_chart(chart_style(fig), "test_age_hours")
        st.caption(
            "Interpretation: " + (
                "Evidence suggests at least one age group differs in estimated weekly gaming hours."
                if p < alpha
                else "The sample does not provide sufficient evidence of a difference across age groups."
            )
        )
    else:
        st.info("At least two age groups with valid hour estimates are needed.")

    st.markdown("---")
    st.markdown("#### Hypothesis 2 · Weekly gaming hours and monthly spending")
    st.markdown(
        "**H₀:** There is no monotonic association between estimated weekly hours and monthly spending.  \n"
        "**H₁:** A monotonic association exists."
    )
    h2 = filtered[["Weekly_Hours_Num", "Monthly_Spending_Num"]].apply(pd.to_numeric, errors="coerce").dropna()
    if len(h2) >= 3 and h2.nunique().min() > 1:
        rho, p2 = stats.spearmanr(h2["Weekly_Hours_Num"], h2["Monthly_Spending_Num"])
        a, b, c = st.columns(3)
        a.metric("Spearman's ρ", f"{rho:.3f}")
        b.metric("p-value", f"{p2:.4f}")
        c.metric("Decision", "Reject H₀" if p2 < alpha else "Do not reject H₀")
        fig = px.scatter(
            h2, x="Weekly_Hours_Num", y="Monthly_Spending_Num",
            title="Estimated weekly hours and monthly spending",
            labels={
                "Weekly_Hours_Num": "Estimated weekly hours",
                "Monthly_Spending_Num": "Estimated monthly spending (₹)",
            },
            color_discrete_sequence=[SAGE],
            opacity=.65,
            marginal_x="histogram",
            marginal_y="box",
        )
        show_chart(chart_style(fig, 410), "test_hours_spending")
        st.caption(
            "Interpretation: " + (
                f"The estimates show a {'positive' if rho > 0 else 'negative'} monotonic association."
                if p2 < alpha
                else "There is insufficient evidence of a monotonic association in this sample."
            )
        )
    else:
        st.info("There are not enough varied hour and spending estimates for this test.")

    st.markdown("---")
    st.markdown("#### Hypothesis 3 · Age group and gaming frequency")
    st.markdown(
        "**H₀:** Age group and gaming frequency are independent.  \n"
        "**H₁:** Age group and gaming frequency are associated."
    )
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
        fig = px.bar(
            long_pct, x="Age_Group", y="Share", color="Frequency", barmode="stack",
            title="Gaming frequency within each age group",
            color_discrete_sequence=PALETTE,
        )
        fig.update_yaxes(tickformat=".0%")
        show_chart(chart_style(fig), "test_age_frequency")
        render_static_table(table)
        if (expected < 5).any():
            st.warning("Some expected cell counts are below 5.")
        st.caption(
            "Interpretation: " + (
                "Evidence suggests an association between age group and gaming frequency."
                if p3 < alpha
                else "There is insufficient evidence of an association in this sample."
            )
        )
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
        render_static_table(gender_table)


# ---------- Footer ----------
st.markdown("---")
render_html("""
<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:#858B82;font-size:.72rem;">
  <span>GAMING PREFERENCES &amp; HABITS · INTERACTIVE RESEARCH DASHBOARD</span>
  <span>Prepared for academic data exploration · Purple Neon gaming design</span>
</div>
""")
