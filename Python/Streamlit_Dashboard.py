"""
Egypt Tourism Analytics Dashboard
==================================
An interactive Streamlit dashboard built on top of the original tourism
analysis notebook. The dataset is Egypt's inbound tourism fact table
(2005-2024), joined with its country/destination/date dimension tables
from a star-schema Excel workbook.

Run with:
    streamlit run app.py
"""

import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# --------------------------------------------------------------------------
# 1. Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Egypt Tourism Dashboard",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, r"C:\Users\ELTANANY 01062856027\Desktop\dashoardpy\Tourism_Data.xlsx")

# --------------------------------------------------------------------------
# 1b. Ancient-Egyptian theme -- colors, fonts & chart template
# --------------------------------------------------------------------------
GOLD = "#C9A227"
GOLD_LIGHT = "#E7C878"
CREAM = "#FBF2E1"
CREAM_DARK = "#F0E1C4"
CARD_WHITE = "#FFFDF8"
NAVY = "#1B2A6B"
NAVY_DARK = "#0B1230"
NAVY_DARKER = "#04060F"
TERRACOTTA = "#B85C34"
TAN = "#E9C7A4"
SKYBLUE = "#4FA8DE"
MAROON = "#4A1942"
ROSE = "#D98CA0"
PURPLE = "#5B2C6F"
BROWN = "#8B4A2B"
INK = "#2A2118"

LAPIS = NAVY
LAPIS_DARK = NAVY_DARK
HIEROGLYPH_INK = INK
PAPYRUS = CREAM
PAPYRUS_DARK = CREAM_DARK

PALETTE = {
    "blue": SKYBLUE,
    "green": NAVY,
    "amber": TERRACOTTA,
    "purple": PURPLE,
    "red": MAROON,
}

pio.templates["egyptian"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="#FFFDF8",
        plot_bgcolor="#F8F4EC",
        font=dict(family="Poppins, Segoe UI, sans-serif", color=INK, size=15),
        title=dict(font=dict(family="Poppins, Segoe UI, sans-serif", size=18, color=TERRACOTTA)),
        colorway=[NAVY, TERRACOTTA, TAN, SKYBLUE, MAROON, ROSE, PURPLE, BROWN],
        xaxis=dict(gridcolor="#EEE2CB", linecolor="#D9C7A8", zerolinecolor="#D9C7A8"),
        yaxis=dict(gridcolor="#EEE2CB", linecolor="#D9C7A8", zerolinecolor="#D9C7A8"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        coloraxis=dict(colorbar=dict(outlinecolor="#D9C7A8")),
    )
)
px.defaults.template = "egyptian"

# --------------------------------------------------------------------------
# 1c. Inject CSS
# --------------------------------------------------------------------------
EGYPT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', 'Segoe UI', sans-serif; }
.stApp { background: __CREAM__; }
.main .block-container { padding-top: 1.2rem; max-width: 1300px; }

section[data-testid="stSidebar"] {
    background: linear-gradient(190deg, __NAVY_DARK__ 0%, __NAVY_DARKER__ 100%);
    border-right: 1px solid rgba(201,162,39,0.35);
}
section[data-testid="stSidebar"] * { color: #E9E3D6 !important; font-family: 'Poppins', 'Segoe UI', sans-serif; }
section[data-testid="stSidebar"] h1 { display: none; }
section[data-testid="stSidebar"] label p { color: __GOLD_LIGHT__ !important; font-weight: 600; font-size: 13px; letter-spacing: 0.4px; text-transform: uppercase; }
section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
section[data-testid="stSidebar"] div[data-testid="stMultiSelect"] > div > div { background-color: rgba(255,255,255,0.06) !important; border: 1px solid rgba(201,162,39,0.55) !important; border-radius: 8px !important; }
section[data-testid="stSidebar"] span[data-baseweb="tag"] { background-color: __GOLD__ !important; color: __NAVY_DARKER__ !important; font-weight: 600; }
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] { background-color: __GOLD__ !important; border-color: __GOLD__ !important; }
section[data-testid="stSidebar"] .stCheckbox label p { text-transform: none; font-weight: 400; }
section[data-testid="stSidebar"] hr { border-color: rgba(201,162,39,0.4) !important; opacity: 0.7; }

.sidebar-logo { text-align: center; padding: 6px 0 22px 0; margin-bottom: 6px; border-bottom: 1px solid rgba(201,162,39,0.35); }
.sidebar-logo .brand-line1 { color: #E9E3D6; font-size: 12px; letter-spacing: 5px; font-weight: 500; margin-top: 10px; }
.sidebar-logo .brand-line2 { color: __GOLD__; font-size: 22px; letter-spacing: 4px; font-weight: 700; }
.sidebar-footer-art { text-align: center; margin-top: 28px; opacity: 0.9; }

h1, h2, h3 { color: __NAVY__ !important; }

.egypt-header { background: linear-gradient(135deg, #FDF6E8 0%, __CREAM_DARK__ 100%); border-radius: 18px; padding: 22px 28px 0 28px; margin-bottom: 22px; box-shadow: 0 3px 10px rgba(42,33,24,0.08); overflow: hidden; }
.egypt-header h1 { font-family: 'Poppins', sans-serif !important; font-weight: 800 !important; font-size: 30px !important; color: __NAVY__ !important; letter-spacing: 0.5px; text-align: left; margin: 0; padding: 0; }
.egypt-header .subtitle { color: __TERRACOTTA__; font-weight: 600; font-size: 14px; margin-top: 2px; }
h1::after { content: none !important; }

div[data-testid="stMetric"] { background: __CARD_WHITE__; border: 1px solid rgba(184,92,52,0.18); border-radius: 16px; padding: 16px 14px 12px 14px; box-shadow: 0 2px 8px rgba(42,33,24,0.08); }
div[data-testid="stMetric"] label { color: __TERRACOTTA__ !important; font-family: 'Poppins', sans-serif !important; font-weight: 600 !important; font-size: 14px !important; letter-spacing: 0.3px; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: __NAVY__ !important; font-family: 'Poppins', sans-serif !important; font-weight: 700 !important; }

div[data-testid="stVerticalBlockBorderWrapper"] { background: __CARD_WHITE__; border-radius: 16px !important; box-shadow: 0 2px 10px rgba(42,33,24,0.08); padding: 6px 6px 2px 6px; }
div[data-testid="stVerticalBlockBorderWrapper"] h3 { color: __TERRACOTTA__ !important; font-weight: 700 !important; font-size: 18px !important; }

.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: none; margin-bottom: 10px; }
.stTabs [data-baseweb="tab"] { background-color: __NAVY__; border: none; border-radius: 999px; color: #FFFFFF !important; font-family: 'Poppins', sans-serif; font-weight: 600; padding: 8px 20px; }
.stTabs [data-baseweb="tab"] p { color: #FFFFFF !important; }
.stTabs [aria-selected="true"] { background-color: __TERRACOTTA__ !important; }
.stTabs [aria-selected="true"] p { color: #FFFFFF !important; }

details[data-testid="stExpander"] { background: __CARD_WHITE__; border: 1px solid rgba(184,92,52,0.18); border-radius: 12px; }
summary { font-family: 'Poppins', sans-serif !important; color: __NAVY__ !important; font-weight: 600 !important; }
.main .stSlider [data-baseweb="slider"] div[role="slider"] { background-color: __TERRACOTTA__ !important; border-color: __TERRACOTTA__ !important; }
hr { border-top: 1px solid rgba(184,92,52,0.25) !important; }
.stCaption, [data-testid="stCaptionContainer"] { color: __INK__ !important; font-family: 'Poppins', sans-serif !important; }
</style>
"""

EGYPT_CSS = (
    EGYPT_CSS
    .replace("__CREAM_DARK__", CREAM_DARK)
    .replace("__CREAM__", CREAM)
    .replace("__CARD_WHITE__", CARD_WHITE)
    .replace("__NAVY_DARKER__", NAVY_DARKER)
    .replace("__NAVY_DARK__", NAVY_DARK)
    .replace("__NAVY__", NAVY)
    .replace("__GOLD_LIGHT__", GOLD_LIGHT)
    .replace("__GOLD__", GOLD)
    .replace("__TERRACOTTA__", TERRACOTTA)
    .replace("__INK__", INK)
)
st.markdown(EGYPT_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 1d. Sidebar logo
# --------------------------------------------------------------------------
SIDEBAR_LOGO_SVG = f"""
<div class="sidebar-logo">
  <svg width="72" height="46" viewBox="0 0 120 76" xmlns="http://www.w3.org/2000/svg">
    <path d="M6 40 C 28 12, 92 12, 114 40 C 92 54, 28 54, 6 40 Z" fill="none" stroke="{GOLD}" stroke-width="3.5" stroke-linejoin="round"/>
    <circle cx="60" cy="40" r="13" fill="none" stroke="{GOLD}" stroke-width="3.5"/>
    <circle cx="60" cy="40" r="5" fill="{GOLD}"/>
    <path d="M60 53 C 57 63, 50 66, 44 62 C 50 65, 55 61, 56 53 Z" fill="{GOLD}"/>
    <path d="M20 40 C 12 44, 8 52, 4 50" fill="none" stroke="{GOLD}" stroke-width="3.5" stroke-linecap="round"/>
  </svg>
  <div class="brand-line1">E&nbsp;X&nbsp;P&nbsp;L&nbsp;O&nbsp;R&nbsp;E</div>
  <div class="brand-line2">EGYPT</div>
</div>
"""
st.sidebar.markdown(SIDEBAR_LOGO_SVG, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 2. Load & prepare data
# --------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading and preparing tourism data...")
def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        st.error(f"Data file not found: `{os.path.basename(path)}`.")
        st.stop()
    try:
        sheets = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    except ImportError:
        st.error("Missing dependency `openpyxl`.")
        st.stop()

    main = sheets["Main_Data"].copy()
    dim_country = sheets["Dim_Country"].copy()
    dim_dest = sheets["Dim_Destination"].copy()
    dim_date = sheets["Dim_Date"].copy()

    df = main.merge(
        dim_country[["Country_Key", "Country_Name", "Region"]].rename(columns={"Region": "Source_Region"}),
        on="Country_Key", how="left"
    )
    df = df.merge(
        dim_dest[["Dest_Key", "Destination_Name", "Region", "Tourism_Type"]].rename(columns={"Region": "Dest_Region"}),
        on="Dest_Key", how="left"
    )
    df = df.merge(dim_date[["Date_Key", "Quarter", "Month_Name"]], on="Date_Key", how="left")

    df["Date"] = pd.to_datetime(df["Year"].astype(str) + df["Month"].astype(str).str.zfill(2), format="%Y%m")
    df["Year"] = pd.to_datetime(df["Year"].astype(str), format="%Y")

    cat_cols = [
        "Dest_Key", "Country_Key", "Transport_Mode", "Purpose_of_Visit",
        "Egypt_Tourism_Season", "Entry_Point", "Country_Name", "Destination_Name", 
        "Source_Region", "Dest_Region", "Tourism_Type", "Quarter", "Month_Name",
    ]
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype("category")

    int_cols = ["Tourist_Arrivals", "Tourism_Revenue_USD", "ADR_EGP", "Avg_Flight_Cost_USD", "Package_Tour_Share_pct"]
    float_cols = ["Avg_Spend_Per_Tourist_USD", "Avg_Stay_Days", "Avg_Temp_C", "ADR_USD", "RevPAR_USD", "USD_EGP_Rate"]
    for c in int_cols:
        df[c] = df[c].astype(np.int64)
    for c in float_cols:
        df[c] = df[c].astype(np.float64)

    df["Month"] = df["Month"].astype(np.int8)
    
    df["Revenue_Per_Arrival_USD"] = np.divide(
        df["Tourism_Revenue_USD"], df["Tourist_Arrivals"],
        out=np.zeros(len(df)), where=df["Tourist_Arrivals"].to_numpy() != 0,
    )
    df["Log_Revenue"] = np.log1p(df["Tourism_Revenue_USD"].to_numpy())

    arr = df["Tourist_Arrivals"].to_numpy(dtype=float)
    z = (arr - np.mean(arr)) / np.std(arr)
    df["Arrivals_Zscore"] = np.round(z, 2)
    df["Is_Outlier_Month"] = np.abs(z) > 2.5

    return df

df = load_data(DATA_PATH)

# --------------------------------------------------------------------------
# 3. Sidebar — interactive filters
# --------------------------------------------------------------------------
year_min, year_max = int(df["Year"].dt.year.min()), int(df["Year"].dt.year.max())
year_range = st.sidebar.slider("Year range", min_value=year_min, max_value=year_max, value=(year_min, year_max), step=1)

dest_options = sorted(df["Destination_Name"].cat.categories.tolist())
selected_dests = st.sidebar.multiselect("Destination", dest_options, default=dest_options)

country_options = sorted(df["Country_Name"].cat.categories.tolist())
selected_countries = st.sidebar.multiselect("Source country", country_options, default=country_options)

purpose_options = sorted(df["Purpose_of_Visit"].cat.categories.tolist())
selected_purpose = st.sidebar.multiselect("Purpose of visit", purpose_options, default=purpose_options)

transport_options = sorted(df["Transport_Mode"].cat.categories.tolist())
selected_transport = st.sidebar.multiselect("Transport mode", transport_options, default=transport_options)

season_options = sorted(df["Egypt_Tourism_Season"].cat.categories.tolist())
selected_season = st.sidebar.multiselect("Season", season_options, default=season_options)

st.sidebar.markdown("---")
show_outliers_only = st.sidebar.checkbox("Show only anomaly months (|z| > 2.5)", value=False)

SIDEBAR_FOOTER_SVG = f"""
<div class="sidebar-footer-art">
  <svg width="150" height="90" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 100 Q 100 108 180 100" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.7"/>
    <path d="M55 100 C 55 70, 60 55, 66 40 C 70 55, 72 70, 68 100 Z" fill="{GOLD}" opacity="0.85"/>
    <path d="M90 100 C 90 65, 96 48, 103 32 C 108 48, 110 65, 104 100 Z" fill="{GOLD}" opacity="0.85"/>
    <path d="M40 98 C 60 90, 140 90, 160 98 C 140 104, 60 104, 40 98 Z" fill="{GOLD}"/>
    <path d="M100 98 L 100 55 L 132 80 Z" fill="{GOLD}" opacity="0.9"/>
    <circle cx="72" cy="86" r="6" fill="{GOLD}"/>
    <path d="M72 92 L 72 98 M 66 92 L 62 98 M 78 92 L 82 98" stroke="{GOLD}" stroke-width="2.5" stroke-linecap="round"/>
  </svg>
</div>
"""
st.sidebar.markdown(SIDEBAR_FOOTER_SVG, unsafe_allow_html=True)

mask = (
    df["Year"].dt.year.between(year_range[0], year_range[1])
    & df["Destination_Name"].isin(selected_dests)
    & df["Country_Name"].isin(selected_countries)
    & df["Purpose_of_Visit"].isin(selected_purpose)
    & df["Transport_Mode"].isin(selected_transport)
    & df["Egypt_Tourism_Season"].isin(selected_season)
)
if show_outliers_only: mask &= df["Is_Outlier_Month"]

fdf = df.loc[mask].copy()

if fdf.empty:
    st.warning("No data matches the current filters. Adjust the sidebar selections.")
    st.stop()

# --------------------------------------------------------------------------
# 4. Header & KPI row
# --------------------------------------------------------------------------
HEADER_SKYLINE_SVG = f"""
<svg width="100%" height="46" viewBox="0 0 1000 60" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" style="display:block;">
  <g fill="{TAN}" opacity="0.55">
    <rect x="0" y="30" width="18" height="26"/><rect x="22" y="18" width="18" height="38"/>
    <rect x="46" y="30" width="18" height="26"/><rect x="70" y="18" width="18" height="38"/>
    <rect x="94" y="30" width="18" height="26"/>
    <circle cx="150" cy="18" r="14"/><rect x="146" y="18" width="8" height="38"/>
    <polygon points="230,56 270,10 310,56"/>
    <polygon points="330,56 390,-2 450,56"/>
    <polygon points="470,56 505,20 540,56"/>
    <rect x="620" y="20" width="10" height="36"/><rect x="645" y="20" width="10" height="36"/>
    <rect x="670" y="20" width="10" height="36"/><rect x="695" y="20" width="10" height="36"/>
    <rect x="610" y="14" width="105" height="8"/>
    <circle cx="880" cy="16" r="13"/><rect x="876" y="16" width="8" height="40"/>
    <rect x="930" y="30" width="16" height="26"/><rect x="952" y="18" width="16" height="38"/>
    <rect x="974" y="30" width="16" height="26"/>
  </g>
</svg>
"""

st.markdown(
    f"""<div class="egypt-header">
  <h1>EGYPT TOURISM DASHBOARD · {fdf['Year'].dt.year.min()} – {fdf['Year'].dt.year.max()}</h1>
  <div class="subtitle">
    Showing {len(fdf):,} records · {fdf['Destination_Name'].nunique()} destinations ·
    {fdf['Country_Name'].nunique()} source countries
  </div>
  {HEADER_SKYLINE_SVG}
</div>""",
    unsafe_allow_html=True,
)

total_arrivals = np.sum(fdf["Tourist_Arrivals"].to_numpy())
total_revenue = np.sum(fdf["Tourism_Revenue_USD"].to_numpy())
avg_spend = np.mean(fdf["Avg_Spend_Per_Tourist_USD"].to_numpy())
avg_adr = np.mean(fdf["ADR_USD"].to_numpy())
avg_stay = np.mean(fdf["Avg_Stay_Days"].to_numpy())

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Arrivals", f"{total_arrivals / 1e6:.1f} M")
k2.metric("Total Revenue", f"${total_revenue / 1e9:.1f} B")
k3.metric("Avg Spend / Tourist", f"${avg_spend:,.0f}")
k4.metric("Avg Daily Rate (ADR)", f"${avg_adr:,.0f}")
k5.metric("Avg Stay Length", f"{avg_stay:.1f} days")

with st.expander("𓋹 Scroll of Records (structure & data types)"):
    info_df = pd.DataFrame({
        "Column": fdf.columns,
        "Dtype": [str(t) for t in fdf.dtypes],
        "Non-Null Count": [fdf[c].notna().sum() for c in fdf.columns],
        "Unique Values": [fdf[c].nunique() for c in fdf.columns],
    })
    st.write(f"**{fdf.shape[0]:,} rows × {fdf.shape[1]} columns** (memory usage: {fdf.memory_usage(deep=True).sum() / 1e6:.1f} MB)")
    st.dataframe(info_df, use_container_width=True, height=350)

st.markdown("---")

# --------------------------------------------------------------------------
# 5. Tabs — one per analysis section
# --------------------------------------------------------------------------
tab_trend, tab_countries, tab_dest, tab_season, tab_transport = st.tabs(
    ["Yearly Trend", "Source Countries", "Destination Performance", "Seasonality", "Transport & Purpose"]
)

# ===========================================================================
# 5.1 YEARLY TREND
# ===========================================================================
with tab_trend:
    yearly = (
        fdf.groupby("Year", observed=True)
        .agg(Arrivals=("Tourist_Arrivals", "sum"), Revenue=("Tourism_Revenue_USD", "sum"))
        .reset_index()
    )
    yearly["Arrivals_M"] = yearly["Arrivals"] / 1e6
    yearly["Revenue_B"] = yearly["Revenue"] / 1e9
    yearly["Year_Int"] = yearly["Year"].dt.year 

    if len(yearly) > 1:
        coeffs = np.polyfit(yearly["Year_Int"], yearly["Arrivals_M"], 1)
        yearly["Trend_M"] = np.polyval(coeffs, yearly["Year_Int"])
    else:
        yearly["Trend_M"] = yearly["Arrivals_M"]

    x_min = yearly["Year_Int"].min()
    x_max = yearly["Year_Int"].max()

    with st.container(border=True):
        fig = px.line(
            yearly, x="Year_Int", y=["Arrivals_M", "Trend_M"],
            markers=True, template="egyptian", title="Tourist Arrivals (Actual vs Trend)",
            labels={"Year_Int": "Year", "value": "Arrivals (Millions)", "variable": "Series"},
            color_discrete_sequence=[PALETTE["blue"], "#9CA3AF"]
        )
        
        fig.update_traces(
            mode="lines+markers+text", line=dict(width=4), marker=dict(size=8), 
            texttemplate="<b>%{y:.1f}</b>", textposition="top center", 
            textfont=dict(size=15), selector=dict(name="Arrivals_M")
        )
        fig.update_traces(line=dict(width=3, dash="dash"), selector=dict(name="Trend_M"))
        
        fig.update_yaxes(visible=False)
        fig.update_xaxes(dtick=1, showgrid=False, title="", tickfont=dict(weight="bold", size=15), range=[x_min - 0.5, x_max + 0.5])
        fig.update_layout(hovermode="x unified", legend_title_text="", margin=dict(l=10, r=10, t=60, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        fig2 = px.line(
            yearly, x="Year_Int", y="Revenue_B", markers=True, template="egyptian",
            title="Tourism Revenue", labels={"Year_Int": "Year", "Revenue_B": "Revenue (Billion USD)"},
            color_discrete_sequence=[PALETTE["green"]]
        )
        
        fig2.update_traces(
            mode="lines+markers+text", line=dict(width=4), marker=dict(size=8),
            texttemplate="<b>%{y:.1f}</b>", textposition="top center", textfont=dict(size=15)
        )
        
        fig2.update_yaxes(visible=False)
        fig2.update_xaxes(dtick=1, showgrid=False, title="", tickfont=dict(weight="bold", size=15), range=[x_min - 0.5, x_max + 0.5])
        fig2.update_layout(hovermode="x unified", margin=dict(l=10, r=10, t=60, b=10))
        st.plotly_chart(fig2, use_container_width=True)

# ===========================================================================
# 5.2 SOURCE COUNTRIES
# ===========================================================================
with tab_countries:
    n_top = st.slider("How many top countries to show", 5, 20, 10)
    with st.container(border=True):
        st.subheader("Top Source Countries by Revenue")
        top_countries = (
            fdf.groupby("Country_Name", observed=True)["Tourism_Revenue_USD"]
            .sum().sort_values(ascending=False).head(n_top).div(1e9).reset_index()
            .rename(columns={"Tourism_Revenue_USD": "Revenue_B"})
        )
        fig = px.bar(
            top_countries.sort_values("Revenue_B"), x="Revenue_B", y="Country_Name",
            orientation="h", title=f"Top {n_top} Source Countries by Revenue",
            labels={"Revenue_B": "Revenue (Billion USD)", "Country_Name": ""},
            color_discrete_sequence=[PALETTE["green"]]
        )
        
        fig.update_xaxes(visible=False)
        fig.update_yaxes(tickfont=dict(weight="bold", size=15), showgrid=False)
        fig.update_traces(texttemplate="<b>%{x:.1f}</b>", textposition="outside", textfont=dict(size=15))
        st.plotly_chart(fig, use_container_width=True)

# ===========================================================================
# 5.3 DESTINATION PERFORMANCE 
# ===========================================================================
with tab_dest:
    dest_summary = (
        fdf.groupby("Destination_Name", observed=True)
        .agg(Arrivals=("Tourist_Arrivals", "sum"), Revenue=("Tourism_Revenue_USD", "sum"), Avg_ADR=("ADR_USD", "mean"))
        .reset_index().sort_values("Revenue", ascending=False)
    )
    dest_summary["Revenue_B"] = dest_summary["Revenue"] / 1e9

    with st.container(border=True):
        st.subheader("Revenue & Occupancy by Destination")
        fig = px.bar(
            dest_summary, x="Destination_Name", y="Revenue_B",
            title="Revenue by Destination (colored by avg. daily rate)",
            color="Avg_ADR", color_continuous_scale=[[0, TAN], [1, NAVY]],
            labels={"Revenue_B": "Revenue (Billion USD)", "Destination_Name": "", "Avg_ADR": "Avg ADR (USD)"}
        )
        
        fig.update_yaxes(visible=False)
        fig.update_xaxes(tickfont=dict(weight="bold", size=15), showgrid=False, title="")
        fig.update_traces(texttemplate="<b>%{y:.1f}</b>", textposition="outside", textfont=dict(size=15))
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Destination Summary Table")
        current_year = fdf['Year'].dt.year.max()
        prev_year = current_year - 1
        rev_curr = fdf[fdf['Year'].dt.year == current_year].groupby("Destination_Name", observed=True)["Tourism_Revenue_USD"].sum()
        rev_prev = fdf[fdf['Year'].dt.year == prev_year].groupby("Destination_Name", observed=True)["Tourism_Revenue_USD"].sum()
        
        yoy_growth = ((rev_curr - rev_prev) / rev_prev.replace(0, np.nan)) * 100
        dest_summary["YoY_Growth"] = dest_summary["Destination_Name"].map(yoy_growth).astype(float).fillna(0)

        def format_mb(val, is_currency=False):
            prefix = "$" if is_currency else ""
            if pd.isna(val): return "0"
            elif val >= 1e9: return f"{prefix}{val/1e9:.2f} B"
            elif val >= 1e6: return f"{prefix}{val/1e6:.2f} M"
            elif val >= 1e3: return f"{prefix}{val/1e3:.1f} K"
            return f"{prefix}{val:,.0f}"

        dest_summary["Arrivals_Fmt"] = dest_summary["Arrivals"].apply(lambda x: format_mb(x, False))
        dest_summary["Revenue_Fmt"] = dest_summary["Revenue"].apply(lambda x: format_mb(x, True))

        def get_trend_label(val):
            if pd.isna(val) or val == 0: return "➖ 0.0%"
            elif val > 0: return f"🔼 +{val:.1f}%"
            else: return f"🔽 {val:.1f}%"

        dest_summary["Trend (YoY)"] = dest_summary["YoY_Growth"].apply(get_trend_label)

        def style_trend(val):
            if isinstance(val, str):
                if "🔼" in val: return 'color: #16A34A; font-weight: bold;'
                elif "🔽" in val: return 'color: #DC2626; font-weight: bold;'
            return ''

        display_df = dest_summary[["Destination_Name", "Arrivals_Fmt", "Revenue_Fmt", "Avg_ADR", "Trend (YoY)"]].rename(columns={
            "Destination_Name": "Destination", "Arrivals_Fmt": "Total Arrivals", "Revenue_Fmt": "Total Revenue", "Avg_ADR": "Avg ADR"
        })

        styled_df = display_df.style.map(style_trend, subset=["Trend (YoY)"]).format({"Avg ADR": "${:.0f}"})
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

# ===========================================================================
# 5.4 SEASONALITY (Modified Colors: Navy / Beige)
# ===========================================================================
with tab_season:
    with st.container(border=True):
        st.subheader("Effect of Season on Arrivals")

        quarter_summary = (
            fdf.groupby("Quarter", observed=True)["Tourist_Arrivals"]
            .sum().reindex([1, 2, 3, 4]).reset_index()
        )
        quarter_summary["Quarter"] = "Q" + quarter_summary["Quarter"].astype(str)
        quarter_summary["Arrivals_M"] = quarter_summary["Tourist_Arrivals"] / 1e6

        fig = px.bar(
            quarter_summary, x="Quarter", y="Arrivals_M",
            title="Arrivals by Quarter", 
            color_discrete_sequence=[NAVY], # تغيير اللون إلى الكحلي
            labels={"Arrivals_M": "Arrivals (Millions)"}
        )
        
        fig.update_yaxes(visible=False)
        fig.update_xaxes(tickfont=dict(weight="bold", size=15), showgrid=False, title="")
        fig.update_traces(texttemplate="<b>%{y:.1f}M</b>", textposition="outside", textfont=dict(size=15))
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Monthly Seasonality of Arrivals")
        
        month_summary = (
            fdf.groupby(["Month", "Month_Name"], observed=True)["Tourist_Arrivals"]
            .sum().reset_index()
            .sort_values("Month")
        )
        month_summary["Arrivals_M"] = month_summary["Tourist_Arrivals"] / 1e6

        fig2 = px.bar(
            month_summary, x="Month_Name", y="Arrivals_M",
            title="", 
            color="Arrivals_M", 
            color_continuous_scale=[[0, TAN], [1, NAVY]], # تغيير التدرج من البيج إلى الكحلي
            labels={"Arrivals_M": "Arrivals (Millions)", "Month_Name": ""}
        )
        
        fig2.update_yaxes(visible=False)
        fig2.update_xaxes(tickfont=dict(weight="bold", size=15), showgrid=False, title="")
        fig2.update_traces(texttemplate="<b>%{y:.0f}M</b>", textposition="outside", textfont=dict(size=15))
        
        fig2.update_layout(coloraxis_showscale=False, margin=dict(t=20))
        st.plotly_chart(fig2, use_container_width=True)

# ===========================================================================
# 5.5 TRANSPORT & PURPOSE OF VISIT
# ===========================================================================
with tab_transport:
    with st.container(border=True):
        st.subheader("Arrivals Share by Transport Mode")

        trans_share = fdf.groupby("Transport_Mode", observed=True)["Tourist_Arrivals"].sum().reset_index()
        fig = px.pie(
            trans_share, names="Transport_Mode", values="Tourist_Arrivals",
            title="Arrivals Share by Transport Mode",
            color_discrete_sequence=[PALETTE["blue"], PALETTE["green"], PALETTE["amber"]]
        )
        
        fig.update_traces(textinfo="label+percent", textfont=dict(weight="bold", size=15))
        st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True):
        st.subheader("Arrivals by Purpose of Visit")
        purpose_summary = fdf.groupby("Purpose_of_Visit", observed=True)["Tourist_Arrivals"].sum().reset_index()
        purpose_summary["Arrivals_M"] = purpose_summary["Tourist_Arrivals"] / 1e6
        
        fig2 = px.bar(
            purpose_summary.sort_values("Arrivals_M"), x="Arrivals_M", y="Purpose_of_Visit",
            orientation="h", title="Arrivals by Purpose of Visit",
            labels={"Arrivals_M": "Arrivals (Millions)", "Purpose_of_Visit": ""},
            color_discrete_sequence=[PALETTE["amber"]] 
        )
        
        fig2.update_xaxes(visible=False)
        fig2.update_yaxes(tickfont=dict(weight="bold", size=15), showgrid=False)
        fig2.update_traces(texttemplate="<b>%{x:.1f}M</b>", textposition="outside", textfont=dict(size=15))
        st.plotly_chart(fig2, use_container_width=True)

# ===========================================================================
# 5.6 FOOTER
# ===========================================================================

st.markdown("---")
st.caption("𓇳 Built with Streamlit, pandas & numpy · Data: Egypt Tourism star-schema dataset (2005–2024) 𓇳")