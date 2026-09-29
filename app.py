
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Toronto Ferry Operations Analytics",
    page_icon="⛴️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PATHS
# ============================================================

DATA_DIR = Path("/content/data")
DATA_FILE = DATA_DIR / "hourly_dashboard.csv"

# ============================================================
# DESIGN SYSTEM
# ============================================================

NAVY = "#1E293B"
DARK = "#0F172A"
BLUE = "#2563EB"
EMERALD = "#10B981"
SLATE = "#64748B"
LIGHT = "#F8FAFC"
BORDER = "#E2E8F0"
WHITE = "#FFFFFF"
RED = "#EF4444"
AMBER = "#F59E0B"

# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       REMOVE STREAMLIT DEFAULT CHROME
       ====================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0px !important;
    }

    [data-testid="stDecoration"] {
        display: none;
    }

    /* ======================================================
       PAGE
       ====================================================== */

    .stApp {
        background: #F8FAFC;
        color: #0F172A;
    }

    .main .block-container {
        max-width: 1600px;
        padding: 1.5rem 2.25rem 3rem 2.25rem;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background: #1E293B;
        border-right: 1px solid #334155;
    }

    section[data-testid="stSidebar"] > div {
        background: #1E293B;
    }

    section[data-testid="stSidebar"] * {
        color: #F8FAFC;
    }

    section[data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }

    .brand {
        padding: 8px 4px 24px 4px;
    }

    .brand-main {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.4px;
    }

    .brand-sub {
        color: #94A3B8;
        font-size: 11px;
        margin-top: 4px;
    }

    .sidebar-label {
        color: #94A3B8;
        text-transform: uppercase;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.2px;
        margin: 22px 0 8px 0;
    }

    .sidebar-info {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 9px;
        padding: 11px;
        margin-top: 16px;
        color: #CBD5E1;
        font-size: 11px;
        line-height: 1.6;
    }

    /* ======================================================
       TOP APP HEADER
       ====================================================== */

    .app-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 14px;
        box-shadow: 0 3px 12px rgba(15,23,42,0.04);
    }

    .app-title {
        color: #0F172A;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .app-subtitle {
        color: #64748B;
        font-size: 12px;
        margin-top: 4px;
    }

    .online-badge {
        display: inline-block;
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #047857;
        padding: 7px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
    }

    .role-badge {
        display: inline-block;
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #1D4ED8;
        padding: 7px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 5px;
    }

    /* ======================================================
       BREADCRUMB
       ====================================================== */

    .breadcrumb {
        color: #64748B;
        font-size: 11px;
        margin: 7px 0 18px 2px;
    }

    .breadcrumb b {
        color: #334155;
    }

    /* ======================================================
       KPI CARDS
       ====================================================== */

    .kpi {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 17px 18px;
        min-height: 122px;
        box-shadow: 0 3px 10px rgba(15,23,42,0.035);
    }

    .kpi-label {
        color: #64748B;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .7px;
        text-transform: uppercase;
    }

    .kpi-value {
        color: #0F172A;
        font-size: 25px;
        font-weight: 800;
        margin-top: 9px;
        line-height: 1.1;
    }

    .kpi-description {
        color: #94A3B8;
        font-size: 11px;
        margin-top: 8px;
    }

    .kpi-accent-blue {
        border-top: 3px solid #2563EB;
    }

    .kpi-accent-green {
        border-top: 3px solid #10B981;
    }

    .kpi-accent-slate {
        border-top: 3px solid #64748B;
    }

    .kpi-accent-amber {
        border-top: 3px solid #F59E0B;
    }

    /* ======================================================
       SECTION HEADINGS
       ====================================================== */

    .section-title {
        color: #0F172A;
        font-size: 15px;
        font-weight: 800;
        margin: 25px 0 3px 1px;
    }

    .section-subtitle {
        color: #64748B;
        font-size: 11px;
        margin: 0 0 10px 1px;
    }

    /* ======================================================
       INSIGHT CARDS
       ====================================================== */

    .insight {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #10B981;
        border-radius: 9px;
        padding: 13px 15px;
        margin-bottom: 8px;
        color: #334155;
        font-size: 12px;
        line-height: 1.55;
    }

    .insight-title {
        color: #0F172A;
        font-weight: 800;
        font-size: 11px;
        margin-bottom: 3px;
    }

    /* ======================================================
       INFO CARD
       ====================================================== */

    .info-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        color: #475569;
        font-size: 12px;
        line-height: 1.7;
    }

    /* ======================================================
       STREAMLIT INPUTS
       ====================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 7px !important;
        border-color: #CBD5E1 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 900px) {
        .main .block-container {
            padding: 1rem;
        }

        .app-title {
            font-size: 18px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    if not DATA_FILE.exists():
        st.error(
            f"Dataset not found: {DATA_FILE}"
        )
        st.stop()

    data = pd.read_csv(DATA_FILE)

    data["Timestamp"] = pd.to_datetime(
        data["Timestamp"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Timestamp"]
    ).copy()

    data["Year"] = data["Timestamp"].dt.year
    data["Month"] = data["Timestamp"].dt.month
    data["Hour"] = data["Timestamp"].dt.hour
    data["Date"] = data["Timestamp"].dt.date

    if "Day_Type" not in data.columns:
        data["Day_Type"] = np.where(
            data["Timestamp"].dt.dayofweek >= 5,
            "Weekend",
            "Weekday"
        )

    if "Season" not in data.columns:

        month = data["Timestamp"].dt.month

        data["Season"] = np.select(
            [
                month.isin([12, 1, 2]),
                month.isin([3, 4, 5]),
                month.isin([6, 7, 8]),
                month.isin([9, 10, 11])
            ],
            [
                "Winter",
                "Spring",
                "Summer",
                "Autumn"
            ],
            default="Unknown"
        )

    data["Total Activity"] = (
        data["Sales Count"] +
        data["Redemption Count"]
    )

    return data.sort_values(
        "Timestamp"
    ).reset_index(drop=True)


df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-main">⛴ Toronto Ferry</div>
            <div class="brand-sub">
                Operations Intelligence Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">Workspace</div>',
        unsafe_allow_html=True
    )

    role = st.selectbox(
        "Dashboard View",
        [
            "Executive View",
            "Operations View",
            "Policy Planners"
        ],
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="sidebar-label">Filters</div>',
        unsafe_allow_html=True
    )

    available_years = sorted(
        df["Year"].unique()
    )

    selected_years = st.multiselect(
        "Year",
        available_years,
        default=available_years
    )

    selected_seasons = st.multiselect(
        "Season",
        ["Winter", "Spring", "Summer", "Autumn"],
        default=["Winter", "Spring", "Summer", "Autumn"]
    )

    selected_day = st.selectbox(
        "Day Type",
        ["All", "Weekday", "Weekend"]
    )

    st.markdown(
        '<div class="sidebar-label">Data Replay</div>',
        unsafe_allow_html=True
    )

    replay = st.toggle(
        "Historical Replay",
        value=False
    )

    replay_speed = st.slider(
        "Replay speed",
        1,
        5,
        3
    )

    st.markdown(
        f"""
        <div class="sidebar-info">
            <b>Data coverage</b><br>
            {df["Timestamp"].min():%d %b %Y}
            → {df["Timestamp"].max():%d %b %Y}<br><br>
            <b>Source records</b><br>
            {len(df):,} hourly records
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FILTERING
# ============================================================

filtered = df.copy()

if selected_years:
    filtered = filtered[
        filtered["Year"].isin(selected_years)
    ]

if selected_seasons:
    filtered = filtered[
        filtered["Season"].isin(selected_seasons)
    ]

if selected_day != "All":
    filtered = filtered[
        filtered["Day_Type"] == selected_day
    ]

if filtered.empty:

    st.warning(
        "No data matches the selected filters."
    )

    st.stop()

# ============================================================
# HEADER
# ============================================================

role_short = {
    "Executive View": "Executive Overview",
    "Operations View": "Operations Control",
    "Policy Planners": "Policy Planning"
}[role]

header_left, header_right = st.columns(
    [5, 2]
)

with header_left:

    st.markdown(
        """
        <div class="app-header">
            <div class="app-title">
                ⛴ Toronto Ferry Operations Analytics
            </div>
            <div class="app-subtitle">
                Toronto Island Park · Passenger Demand &
                Operations Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        """
        <div class="app-header" style="text-align:right;">
            <span class="online-badge">
                ● System Online
            </span>
            <span class="role-badge">
                Current View
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    f"""
    <div class="breadcrumb">
        Operations Intelligence &nbsp;/&nbsp;
        <b>{role_short}</b>
        &nbsp;/&nbsp;
        Historical Analytics
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered["Sales Count"].sum()

total_redemptions = filtered[
    "Redemption Count"
].sum()

difference = total_sales - total_redemptions

hourly_avg = (
    filtered.groupby("Hour")["Total Activity"]
    .mean()
)

peak_hour = int(hourly_avg.idxmax())
peak_hour_value = hourly_avg.max()

season_avg = (
    filtered.groupby("Season")["Total Activity"]
    .mean()
)

peak_season = season_avg.idxmax()
peak_season_value = season_avg.max()

winter_avg = season_avg.get(
    "Winter",
    np.nan
)

if pd.notna(winter_avg) and winter_avg > 0:
    off_season_index = (
        filtered["Total Activity"].mean()
        / winter_avg
    )
else:
    off_season_index = np.nan

coverage = (
    filtered["Coverage_Pct"].mean()
    if "Coverage_Pct" in filtered.columns
    else np.nan
)

# ============================================================
# EXECUTIVE VIEW
# ============================================================

if role == "Executive View":

    st.markdown(
        '<div class="section-title">Executive Snapshot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'High-level view of historical ferry demand and activity.'
        '</div>',
        unsafe_allow_html=True
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    cards = [
        (
            k1,
            "TOTAL TICKET SALES",
            f"{total_sales:,.0f}",
            "Recorded sales",
            "kpi-accent-blue"
        ),
        (
            k2,
            "GATE REDEMPTIONS",
            f"{total_redemptions:,.0f}",
            "Recorded scans",
            "kpi-accent-green"
        ),
        (
            k3,
            "SALES–REDEMPTION DIFFERENCE",
            f"{difference:,.0f}",
            "Sales minus scans",
            "kpi-accent-slate"
        ),
        (
            k4,
            "PEAK DEMAND HOUR",
            f"{peak_hour:02d}:00",
            f"{peak_hour_value:,.1f} avg activity",
            "kpi-accent-amber"
        ),
        (
            k5,
            "PEAK SEASON",
            peak_season.upper(),
            f"{peak_season_value:,.1f} avg activity",
            "kpi-accent-green"
        )
    ]

    for col, label, value, desc, accent in cards:

        with col:

            st.markdown(
                f"""
                <div class="kpi {accent}">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-description">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # MONTHLY TREND
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Demand Trend</div>',
        unsafe_allow_html=True
    )

    monthly = (
        filtered
        .set_index("Timestamp")
        .resample("MS")
        .agg({
            "Sales Count": "sum",
            "Redemption Count": "sum"
        })
        .reset_index()
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["Timestamp"],
            y=monthly["Sales Count"],
            name="Ticket Sales",
            mode="lines",
            line=dict(
                color=BLUE,
                width=2.5
            ),
            fill="tozeroy",
            fillcolor="rgba(37,99,235,0.10)"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=monthly["Timestamp"],
            y=monthly["Redemption Count"],
            name="Redemptions",
            mode="lines",
            line=dict(
                color=EMERALD,
                width=2.5
            ),
            fill="tozeroy",
            fillcolor="rgba(16,185,129,0.07)"
        )
    )

    fig.update_layout(
        template="plotly_white",
        title="Monthly Ticket Activity",
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=45, b=10),
        legend=dict(
            orientation="h",
            y=1.02,
            x=0
        )
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        gridcolor="#E2E8F0"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    # --------------------------------------------------------
    # SEASON + HOUR
    # --------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        seasonal = (
            filtered.groupby("Season")
            ["Total Activity"]
            .sum()
            .reindex(
                ["Winter", "Spring", "Summer", "Autumn"]
            )
            .fillna(0)
            .reset_index()
        )

        fig = px.pie(
            seasonal,
            names="Season",
            values="Total Activity",
            hole=0.62
        )

        fig.update_layout(
            title="Seasonal Volume Share",
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=45, b=10),
            showlegend=True
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    with c2:

        hourly = (
            filtered.groupby("Hour")
            ["Total Activity"]
            .mean()
            .reset_index()
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hourly["Hour"],
                y=hourly["Total Activity"],
                mode="lines+markers",
                name="Average Activity",
                line=dict(
                    color=BLUE,
                    width=3
                )
            )
        )

        fig.add_vrect(
            x0=10,
            x1=15,
            fillcolor=EMERALD,
            opacity=0.08,
            line_width=0
        )

        fig.update_layout(
            title="24-Hour Demand Profile",
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=45, b=10),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )


# ============================================================
# OPERATIONS VIEW
# ============================================================

elif role == "Operations View":

    st.markdown(
        '<div class="section-title">Operations Control Centre</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Detailed demand timing and operational activity patterns.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # OPERATIONS KPIs
    # --------------------------------------------------------

    k1, k2, k3, k4, k5 = st.columns(5)

    weekend_avg = filtered.loc[
        filtered["Day_Type"] == "Weekend",
        "Total Activity"
    ].mean()

    weekday_avg = filtered.loc[
        filtered["Day_Type"] == "Weekday",
        "Total Activity"
    ].mean()

    ratio = (
        weekend_avg / weekday_avg
        if pd.notna(weekday_avg) and weekday_avg > 0
        else np.nan
    )

    cards = [
        (
            k1,
            "PEAK HOUR",
            f"{peak_hour:02d}:00",
            f"{peak_hour_value:,.1f} avg activity",
            "kpi-accent-blue"
        ),
        (
            k2,
            "PEAK SEASON",
            peak_season.upper(),
            f"{peak_season_value:,.1f} avg activity",
            "kpi-accent-green"
        ),
        (
            k3,
            "WEEKEND / WEEKDAY",
            f"{ratio:.2f}×" if pd.notna(ratio) else "N/A",
            "Average activity ratio",
            "kpi-accent-amber"
        ),
        (
            k4,
            "HOURLY RECORDS",
            f"{len(filtered):,}",
            "Filtered observations",
            "kpi-accent-slate"
        ),
        (
            k5,
            "COVERAGE",
            f"{coverage:.1f}%" if pd.notna(coverage) else "N/A",
            "Average hourly coverage",
            "kpi-accent-green"
        )
    ]

    for col, label, value, desc, accent in cards:

        with col:

            st.markdown(
                f"""
                <div class="kpi {accent}">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-description">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # HOURLY SALES VS REDEMPTIONS
    # --------------------------------------------------------

    c1, c2 = st.columns([1.6, 1])

    with c1:

        hourly = (
            filtered.groupby("Hour")
            .agg(
                Sales=("Sales Count", "mean"),
                Redemptions=("Redemption Count", "mean")
            )
            .reset_index()
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=hourly["Hour"],
                y=hourly["Sales"],
                name="Sales",
                mode="lines+markers",
                line=dict(
                    color=BLUE,
                    width=2.5
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=hourly["Hour"],
                y=hourly["Redemptions"],
                name="Redemptions",
                mode="lines+markers",
                line=dict(
                    color=EMERALD,
                    width=2.5
                )
            )
        )

        fig.add_vrect(
            x0=10,
            x1=15,
            fillcolor=EMERALD,
            opacity=0.07,
            line_width=0
        )

        fig.update_layout(
            title="Hourly Sales vs Redemptions",
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified",
            margin=dict(l=10, r=10, t=45, b=10)
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    with c2:

        period = filtered.copy()

        period["Demand Period"] = np.where(
            period["Hour"].between(10, 15),
            "Peak",
            "Off-Peak"
        )

        comparison = (
            period.groupby("Demand Period")
            ["Total Activity"]
            .mean()
            .reindex(["Peak", "Off-Peak"])
            .reset_index()
        )

        fig = px.bar(
            comparison,
            x="Demand Period",
            y="Total Activity",
            title="Peak vs Off-Peak Activity"
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=45, b=10),
            showlegend=False
        )

        fig.update_traces(
            marker_color=BLUE
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    # --------------------------------------------------------
    # WEEKDAY PATTERN
    # --------------------------------------------------------

    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    temp = filtered.copy()

    temp["Day_Name"] = (
        temp["Timestamp"]
        .dt.day_name()
    )

    weekday = (
        temp.groupby("Day_Name")
        ["Total Activity"]
        .mean()
        .reindex(weekday_order)
        .reset_index()
    )

    fig = px.bar(
        weekday,
        x="Day_Name",
        y="Total Activity",
        title="Average Activity by Day of Week"
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=45, b=10)
    )

    fig.update_traces(
        marker_color=EMERALD
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )


# ============================================================
# POLICY PLANNERS VIEW
# ============================================================

else:

    st.markdown(
        '<div class="section-title">Policy Planning & Historical Trends</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Long-term demand patterns to support operational planning.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # POLICY KPIs
    # --------------------------------------------------------

    annual = (
        filtered.groupby("Year")
        ["Total Activity"]
        .sum()
        .reset_index()
    )

    if len(annual) >= 2:

        first_value = annual.iloc[0]["Total Activity"]
        last_value = annual.iloc[-1]["Total Activity"]

        if first_value != 0:
            change_pct = (
                (last_value - first_value)
                / abs(first_value)
            ) * 100
        else:
            change_pct = np.nan

    else:
        change_pct = np.nan

    k1, k2, k3, k4, k5 = st.columns(5)

    cards = [
        (
            k1,
            "YEARS ANALYSED",
            f"{filtered['Year'].nunique()}",
            "Historical years",
            "kpi-accent-blue"
        ),
        (
            k2,
            "PEAK SEASON",
            peak_season.upper(),
            f"{peak_season_value:,.1f} avg activity",
            "kpi-accent-green"
        ),
        (
            k3,
            "WINTER INDEX",
            f"{off_season_index:.2f}×"
            if pd.notna(off_season_index)
            else "N/A",
            "Overall vs winter",
            "kpi-accent-slate"
        ),
        (
            k4,
            "HISTORICAL CHANGE",
            f"{change_pct:+.1f}%"
            if pd.notna(change_pct)
            else "N/A",
            "First vs latest selected year",
            "kpi-accent-amber"
        ),
        (
            k5,
            "TOTAL ACTIVITY",
            f"{filtered['Total Activity'].sum():,.0f}",
            "Recorded activity",
            "kpi-accent-green"
        )
    ]

    for col, label, value, desc, accent in cards:

        with col:

            st.markdown(
                f"""
                <div class="kpi {accent}">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-description">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # YEARLY TREND
    # --------------------------------------------------------

    c1, c2 = st.columns([1.5, 1])

    with c1:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=annual["Year"],
                y=annual["Total Activity"],
                mode="lines+markers",
                name="Total Activity",
                line=dict(
                    color=BLUE,
                    width=3
                ),
                marker=dict(
                    size=8
                )
            )
        )

        fig.update_layout(
            title="Annual Recorded Activity",
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=45, b=10)
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    with c2:

        season_year = (
            filtered.groupby(
                ["Year", "Season"]
            )["Total Activity"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            season_year,
            x="Year",
            y="Total Activity",
            color="Season",
            title="Seasonal Activity by Year",
            barmode="stack",
            color_discrete_map={
                "Winter": "#94A3B8",
                "Spring": "#60A5FA",
                "Summer": "#10B981",
                "Autumn": "#64748B"
            }
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=45, b=10)
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )

    # --------------------------------------------------------
    # POLICY PATTERN
    # --------------------------------------------------------

    monthly_policy = (
        filtered.groupby("Month")
        ["Total Activity"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        monthly_policy,
        x="Month",
        y="Total Activity",
        title="Average Activity by Calendar Month"
    )

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=45, b=10)
    )

    fig.update_traces(
        marker_color=EMERALD
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

# ============================================================
# INSIGHTS — COMMON TO ALL VIEWS
# ============================================================

st.markdown(
    '<div class="section-title">Intelligence Summary</div>',
    unsafe_allow_html=True
)

insight1, insight2 = st.columns(2)

with insight1:

    weekend = filtered.loc[
        filtered["Day_Type"] == "Weekend",
        "Total Activity"
    ].mean()

    weekday = filtered.loc[
        filtered["Day_Type"] == "Weekday",
        "Total Activity"
    ].mean()

    if (
        pd.notna(weekend)
        and pd.notna(weekday)
        and weekday > 0
    ):

        weekend_ratio = weekend / weekday

        text1 = (
            f"Weekend activity averages "
            f"<b>{weekend_ratio:.2f}×</b> weekday activity "
            f"under the selected filters."
        )

    else:

        text1 = (
            "Weekend and weekday activity could not "
            "be compared under the selected filters."
        )

    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">
                WEEKEND DEMAND
            </div>
            {text1}
        </div>
        """,
        unsafe_allow_html=True
    )

with insight2:

    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">
                PEAK WINDOW
            </div>
            Historical average activity is highest around
            <b>{peak_hour:02d}:00</b>, with approximately
            <b>{peak_hour_value:,.0f}</b> recorded activities
            in the hourly dataset.
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# RECENT RECORDS
# ============================================================

st.markdown(
    '<div class="section-title">Recent Operations Records</div>',
    unsafe_allow_html=True
)

search = st.text_input(
    "Search records",
    placeholder="Search by date, season, day type..."
)

recent = filtered.sort_values(
    "Timestamp",
    ascending=False
).copy()

if search:

    search_lower = search.lower()

    mask = (
        recent.astype(str)
        .apply(
            lambda row:
            row.str.lower()
            .str.contains(
                search_lower,
                regex=False
            ).any(),
            axis=1
        )
    )

    recent = recent[mask]

table_columns = [
    "Timestamp",
    "Sales Count",
    "Redemption Count",
    "Total Activity",
    "Hour",
    "Day_Type",
    "Season"
]

recent_table = recent[
    table_columns
].head(100).copy()

recent_table["Timestamp"] = (
    recent_table["Timestamp"]
    .dt.strftime("%Y-%m-%d %H:%M")
)

recent_table.columns = [
    "Timestamp",
    "Sales",
    "Redemptions",
    "Total Activity",
    "Hour",
    "Day Type",
    "Season"
]

st.dataframe(
    recent_table,
    width="stretch",
    hide_index=True
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Toronto Ferry Operations Analytics · "
    "Historical dataset analysis · "
    f"Latest available record: "
    f"{df['Timestamp'].max():%d %b %Y %H:%M}"
)

# ============================================================
# HISTORICAL REPLAY
# ============================================================

if replay:

    st.info(
        f"Historical replay enabled at speed {replay_speed}/5. "
        "This is a visual replay of historical records, "
        "not a live Toronto ferry data feed."
    )
