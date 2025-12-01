# _Charts.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from utils import render_season_filter, load_and_filter_csv


# Show the global filter
season = render_season_filter()

# === TITLE ===
# st.title("Charts")

# Define theme colors for consistency
DARK_BG = "#121212"
CARD_BG = "#202124"
ROW_ALT = "#1A1A1A"
TEXT_COLOR = "#FFFFFF"
LIGHT_GREY = "#A9A9A9"
ESPN_BLUE = "#3F8EF3"
ESPN_GREEN = "#00FF66" # ESPN green for active page border

# === TEAM COLORS  ===
TEAM_COLORS = {
    "WAKA": "#3F8EF3",   # ESPN Blue
    "ED": "#00FF66",   # ESPN Green
    "WALL": "#FF4B4B",   # Bright Red
    "PUG": "#FFD700",   # Gold
    "HARN": "#9B59B6",   # Purple
    "CRAIG": "#FF8000",   # Orange
    "BIV": "#1ABC9C",   # Teal
    "HOUSE": "#E91E63",   # Pink/Magenta
    "FEDS": "#1B974F",   # Emerald Green
    "DAVE": "#34B4DB",  # Sky Blue
    "SELL": "#6E9294",  # Cool Grey
    "JAY": "#F39C12"   # Amber
}

# === PAGE CONFIG ===
st.set_page_config(page_title="Charts", layout="wide")
st.markdown(f"<style>body {{ background-color: {DARK_BG}; }}</style>", unsafe_allow_html=True)

# === BACKGROUND + HEADER STYLE + LOGO ===
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');

.stApp {{
    background-color: {DARK_BG};
    color: white;
}}  

/* Page Title with inline ESPN icon */
h1 {{
    font-family: 'Oswald', sans-serif !important;
    font-weight: 500 !important;
    font-size: 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px;
}}

/* Sidebar Styling */
.sidebar-header {{ 
    color: {TEXT_COLOR}; 
    font-size: 20px !important; 
    font-weight: 450; 
    margin-bottom: 0; 
    font-family: 'Oswald', sans-serif !important; 
}}
.sidebar-text {{ 
    color: {LIGHT_GREY}; 
    font-size: 16px; 
}}
div[data-testid="stSidebarNav"] li a[aria-current="page"] {{
    border-left: 5px solid {ESPN_GREEN};
    background-color: {ROW_ALT};
}}

/* Table Styling */
table {{
    color: {LIGHT_GREY};
}}
</style>

<h1 style="margin-bottom: 25px;">
    <img src="https://a.espncdn.com/combiner/i?img=i/fantasy/ffl.png&w=100&h=100&transparent=true"
         style="width:40px; height:40px; vertical-align:middle;"/>
    Charts
</h1>
""", unsafe_allow_html=True)

# Access the global season from session_state
season = st.session_state.get("season", 2024)

# === LOAD DATA ===
df = load_and_filter_csv("team_weekly.csv", season)

# Exclude weeks where Team Score is 0
df = df[df["Team Score"] != 0]

# --- CALCULATE MAX WEEK ---
max_week = df["Week"].max()

# --- CUMULATIVE SUMS UP TO MAX WEEK (inclusive) ---
df_cumulative = df[df["Week"] <= max_week]

cumulative_sums = df_cumulative.groupby(["Abbrev", "Owner"], as_index=False).agg(
    Team_Score_Sum=("Team Score", "sum"),
    Team_Projected_Sum=("Team Projected", "sum"),
    Points_Against_Sum=("Points Against", "sum"),
    AVG=("Team Score", "mean"),
    HIGH=("Team Score", "max"),
    MED=("Team Score", "median"),
    LOW=("Team Score", "min")
)

# --- GET TEAM INFO AND RANK AT MAX WEEK ---
df_max_week = df[df["Week"] == max_week][["Abbrev", "Owner", "Rank"]]

# --- MERGE cumulative sums WITH max week info ---
agg_df = pd.merge(df_max_week, cumulative_sums, on=["Abbrev", "Owner"])

# Calculate difference
agg_df["Difference"] = agg_df["Team_Score_Sum"] - agg_df["Team_Projected_Sum"]

# Assuming agg_df is already defined
x = agg_df['Points_Against_Sum']
y = agg_df['Team_Score_Sum']
labels = agg_df['Abbrev']

# Medians
x_med = np.median(x)
y_med = np.median(y)

fig = go.Figure()

# Map team colors

point_colors = [TEAM_COLORS[abbr] for abbr in labels]

# Scatter points with always-visible labels
fig.add_trace(go.Scatter(
    x=x, 
    y=y, 
    mode="markers+text",       # show both dots + text
    text=labels, 
    textposition="top center", # label placement
    marker=dict(
        size=16,
        color=point_colors
    ),
    textfont=dict(color="#FFFFFF", size=15)
))

# Vertical median line (Points Against)
fig.add_shape(type="line",
    x0=x_med, x1=x_med, y0=min(y), y1=max(y),
    line=dict(color="#3F8EF3", dash="dot", width=2)
)
fig.add_annotation(
    x=x_med, y=max(y),
    text=f"Median: {x_med:.1f}",
    showarrow=False,
    yshift=20,
    font=dict(color="#3F8EF3", size=12)
)

# Horizontal median line (Team Score)
fig.add_shape(type="line",
    x0=min(x), x1=max(x), y0=y_med, y1=y_med,
    line=dict(color="#3F8EF3", dash="dot", width=2)
)
fig.add_annotation(
    x=max(x), y=y_med,
    text=f"Median: {y_med:.1f}",
    showarrow=False,
    xshift=40,
    font=dict(color="#3F8EF3", size=12)
)

# Layout styling
fig.update_layout(
    height=600,
    # Background colors
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    
    # Font for axes and other text
    font=dict(color=TEXT_COLOR),
    
    # Chart title
    title=dict(
        text="POINTS FOR vs. POINTS AGAINST",
        font=dict(
            family="Oswald, sans-serif",
            size=18,
            color=TEXT_COLOR
        ),
        x=0.05,          # center horizontally
        xanchor='left',
        yanchor='top'
    ),
    
    # Margins around the chart
    margin=dict(l=60, r=60, t=80, b=60),
    
    # X-axis configuration
    xaxis=dict(
        title="Points Against",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",   # subtle gray gridlines
        zeroline=False
    ),
    
    # Y-axis configuration
    yaxis=dict(
        title="Points For",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",   # subtle gray gridlines
        zeroline=False
    )
)

# === SECOND CHART ===
x2 = agg_df['Difference']
y2 = agg_df['Team_Score_Sum']
labels2 = agg_df['Abbrev']

x2_med = np.median(x2)
y2_med = np.median(y2)

# QUADRANTS

# Define quadrant label positions
quadrant_positions = [
    ("High PF / High Diff",  (x2_med + max(x2)) / 2, (y2_med + max(y2)) / 2, "rgba(0, 200, 0, 0.12)"),  # Q1
    ("Low PF / High Diff",   (x2_med + max(x2)) / 2, (y2_med + min(y2)) / 2, "rgba(0, 120, 255, 0.12)"), # Q2
    ("Low PF / Low Diff",    (x2_med + min(x2)) / 2, (y2_med + min(y2)) / 2, "rgba(255, 0, 0, 0.12)"),   # Q3
    ("High PF / Low Diff",   (x2_med + min(x2)) / 2, (y2_med + max(y2)) / 2, "rgba(255, 165, 0, 0.12)")  # Q4
]

# Add shaded quadrant rectangles
fig2.add_shape(
    type="rect",
    x0=x2_med, y0=y2_med, x1=max(x2), y1=max(y2),
    fillcolor="rgba(0, 200, 0, 0.10)", line=dict(width=0)
)
fig2.add_shape(
    type="rect",
    x0=x2_med, y0=min(y2), x1=max(x2), y1=y2_med,
    fillcolor="rgba(0, 120, 255, 0.10)", line=dict(width=0)
)
fig2.add_shape(
    type="rect",
    x0=min(x2), y0=min(y2), x1=x2_med, y1=y2_med,
    fillcolor="rgba(255, 0, 0, 0.10)", line=dict(width=0)
)
fig2.add_shape(
    type="rect",
    x0=min(x2), y0=y2_med, x1=x2_med, y1=max(y2),
    fillcolor="rgba(255, 165, 0, 0.10)", line=dict(width=0)
)

# Add quadrant labels (centered)
for label, x_pos, y_pos, _color in quadrant_positions:
    fig2.add_annotation(
        x=x_pos,
        y=y_pos,
        text=label,
        showarrow=False,
        font=dict(size=14, color=TEXT_COLOR),
        opacity=0.8
    )

fig2 = go.Figure()
point_colors2 = [TEAM_COLORS[abbr] for abbr in labels2]

# Scatter points
fig2.add_trace(go.Scatter(
    x=x2, 
    y=y2, 
    mode="markers+text",
    text=labels2,
    textposition="top center",
    marker=dict(size=16, color=point_colors2),
    textfont=dict(color=TEXT_COLOR, size=15)
))

# Median lines
fig2.add_shape(type="line",
    x0=x2_med, x1=x2_med, y0=min(y2), y1=max(y2),
    line=dict(color=ESPN_BLUE, dash="dot", width=2)
)
fig2.add_annotation(
    x=x2_med, y=max(y2),
    text=f"Median: {x2_med:.1f}",
    showarrow=False,
    yshift=20,
    font=dict(color=ESPN_BLUE, size=12)
)
fig2.add_shape(type="line",
    x0=min(x2), x1=max(x2), y0=y2_med, y1=y2_med,
    line=dict(color=ESPN_BLUE, dash="dot", width=2)
)
fig2.add_annotation(
    x=max(x2), y=y2_med,
    text=f"Median: {y2_med:.1f}",
    showarrow=False,
    xshift=40,
    font=dict(color=ESPN_BLUE, size=12)
)

# Layout
fig2.update_layout(
    height=600,
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    font=dict(color=TEXT_COLOR),
    title=dict(
        text="POINTS FOR vs. DIFFERENCE",
        font=dict(family="Oswald, sans-serif", size=18, color=TEXT_COLOR),
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=60, r=60, t=80, b=60),
    xaxis=dict(
        title="Difference (Points For - Projected)",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",
        zeroline=False
    ),
    yaxis=dict(
        title="Points For",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",
        zeroline=False
    )
)

# === THIRD CHART (PF vs. PROJ)===
x3 = agg_df['Team_Projected_Sum']
y3 = agg_df['Team_Score_Sum']
labels2 = agg_df['Abbrev']

x3_med = np.median(x3)
y3_med = np.median(y3)

fig3 = go.Figure()
point_colors2 = [TEAM_COLORS[abbr] for abbr in labels2]

# Scatter points
fig3.add_trace(go.Scatter(
    x=x3, 
    y=y3, 
    mode="markers+text",
    text=labels2,
    textposition="top center",
    marker=dict(size=16, color=point_colors2),
    textfont=dict(color=TEXT_COLOR, size=15)
))

# Median lines
fig3.add_shape(type="line",
    x0=x3_med, x1=x3_med, y0=min(y3), y1=max(y3),
    line=dict(color=ESPN_BLUE, dash="dot", width=2)
)
fig3.add_annotation(
    x=x3_med, y=max(y3),
    text=f"Median: {x3_med:.1f}",
    showarrow=False,
    yshift=20,
    font=dict(color=ESPN_BLUE, size=12)
)
fig3.add_shape(type="line",
    x0=min(x3), x1=max(x3), y0=y3_med, y1=y3_med,
    line=dict(color=ESPN_BLUE, dash="dot", width=2)
)
fig3.add_annotation(
    x=max(x3), y=y3_med,
    text=f"Median: {y3_med:.1f}",
    showarrow=False,
    xshift=40,
    font=dict(color=ESPN_BLUE, size=12)
)

# Layout
fig3.update_layout(
    height=600,
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    font=dict(color=TEXT_COLOR),
    title=dict(
        text="POINTS FOR vs. PROJECTED",
        font=dict(family="Oswald, sans-serif", size=18, color=TEXT_COLOR),
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=60, r=60, t=80, b=60),
    xaxis=dict(
        title="Points Projected",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",
        zeroline=False
    ),
    yaxis=dict(
        title="Points For",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",
        zeroline=False
    )
)

# === FOURTH CHART (Points Heatmap)===

# Sort teams by total Team Score (descending)
team_totals = df.groupby("Abbrev")["Team Score"].sum().sort_values(ascending=False)
sorted_abbrevs = team_totals.index.tolist()

# Build pivot table and reindex
heatmap_df = df.pivot_table(
    index="Abbrev", 
    columns="Week", 
    values="Team Score", 
    aggfunc="sum"
).fillna(0)

heatmap_df = heatmap_df.reindex(sorted_abbrevs)  # ✅ sorted order

colorscale = [
    [0.0, "#D64545"],  # lowest = red
    [0.5, "#1A1A1A"],  # middle = dark neutral
    [1.0, "#21C55D"],  # highest = ESPN blue
]

# Create heatmap
fig5 = go.Figure(
    data=go.Heatmap(
        z=heatmap_df.values,
        x=heatmap_df.columns,
        y=heatmap_df.index,
        colorscale=colorscale,
        colorbar=dict(
            title=dict(
                text="Team Score",
                font=dict(color=TEXT_COLOR)
            ),
            tickfont=dict(color=LIGHT_GREY)
        ),
        showscale=False,
        text=heatmap_df.values,                # values to display
        texttemplate="%{text}",                # show raw numbers
        textfont=dict(color=TEXT_COLOR, size=14)  # label styling
    )
)

fig5.update_layout(
    title=dict(
        text="TEAM SCORES BY WEEK",
        font=dict(family="Oswald, sans-serif", size=18, color=TEXT_COLOR),
        x=0.05,
        xanchor="left"
    ),
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    margin=dict(l=80, r=60, t=80, b=60),
    xaxis=dict(
        title=dict(
            text="Week",
            font=dict(color=TEXT_COLOR)
        ),
        tickmode="linear",
        dtick=1,
        tickfont=dict(color=LIGHT_GREY)
    ),
    yaxis=dict(
        title=dict(
            text="Team",
            font=dict(color=TEXT_COLOR)
        ),
        autorange="reversed",
        tickfont=dict(color=ESPN_BLUE, size=14)
    ),
    height=600
)

# === 6TH CHART (Weekly Score Rank Heatmap)===

# --- Compute weekly ranks (1 = best, 12 = worst) ---
rank_df = df.pivot_table(
    index="Abbrev",
    columns="Week",
    values="Team Score",
    aggfunc="first"  # keep the actual weekly score
)

# Rank per week (descending: highest score = rank 1)
rank_df = rank_df.rank(ascending=False, method='min', axis=0)

# Sort teams by average weekly rank (or choose another sorting method)
sorted_abbrevs = rank_df.mean(axis=1).sort_values().index.tolist()
rank_df = rank_df.reindex(sorted_abbrevs)

# Define your existing colorscale
colorscale = [
    [0.0, "#21C55D"],  # best (rank 1) = green
    [0.5, "#1A1A1A"],  # middle = dark neutral
    [1.0, "#D64545"],  # worst (rank 12) = red
]

# Create heatmap
fig6 = go.Figure(
    data=go.Heatmap(
        z=rank_df.values,
        x=rank_df.columns,
        y=rank_df.index,
        colorscale=colorscale,
        zmin=1,
        zmax=12,
        showscale=False,
        colorbar=dict(
            title=dict(
                text="Weekly Score Rank",
                font=dict(color=TEXT_COLOR)
            ),
            tickfont=dict(color=LIGHT_GREY)
        ),
        text=rank_df.values,
        texttemplate="%{text}",
        textfont=dict(color=TEXT_COLOR, size=14)
    )
)

fig6.update_layout(
    title=dict(
        text="TEAM WEEKLY SCORE RANKS",
        font=dict(family="Oswald, sans-serif", size=18, color=TEXT_COLOR),
        x=0.05,
        xanchor="left"
    ),
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    margin=dict(l=80, r=60, t=80, b=60),
    xaxis=dict(
        title=dict(text="Week", font=dict(color=TEXT_COLOR)),
        tickmode="linear",
        dtick=1,
        tickfont=dict(color=LIGHT_GREY)
    ),
    yaxis=dict(
        title=dict(text="Team", font=dict(color=TEXT_COLOR)),
        autorange="reversed",
        tickfont=dict(color=ESPN_BLUE, size=14)
    ),
    height=600
)


# === FIFTH CHART (Points vs. Drafted)===

# Load the roster data
roster_df = load_and_filter_csv("roster.csv", season)

# Calculate players drafted
draft_counts = (
    roster_df[roster_df["Acquisition Type"] == "DRAFT"]
    .groupby("Abbrev")
    .size()
    .reset_index(name="Drafted_Player_Count")
)

# Merge with agg_df
agg_with_draft = pd.merge(
    agg_df,
    draft_counts,
    on="Abbrev",
    how="left"   # in case a team has no drafted players (shouldn’t happen, but safe)
)

# Create scatter plot
x4 = agg_with_draft["Drafted_Player_Count"]
y4 = agg_with_draft["Team_Score_Sum"]
labels4 = agg_with_draft["Abbrev"]

x4_med = np.median(x4)
y4_med = np.median(y4)

fig4 = go.Figure()
point_colors2 = [TEAM_COLORS[abbr] for abbr in labels4]

# Scatter points
fig4.add_trace(go.Scatter(
    x=x4, 
    y=y4, 
    mode="markers+text",
    text=labels2,
    textposition="top center",
    marker=dict(size=16, color=point_colors2),
    textfont=dict(color=TEXT_COLOR, size=15)
))

# Median lines
fig4.add_shape(type="line",
    x0=x4_med, x1=x4_med, y0=min(y4), y1=max(y4),
    line=dict(color=ESPN_BLUE, dash="dot", width=2)
)
fig4.add_annotation(
    x=x4_med, y=max(y4),
    text=f"Median: {x4_med:.1f}",
    showarrow=False,
    yshift=20,
    font=dict(color=ESPN_BLUE, size=12)
)
fig4.add_shape(type="line",
    x0=min(x4), x1=max(x4), y0=y4_med, y1=y4_med,
    line=dict(color=ESPN_BLUE, dash="dot", width=2)
)
fig4.add_annotation(
    x=max(x4), y=y4_med,
    text=f"Median: {y4_med:.1f}",
    showarrow=False,
    xshift=40,
    font=dict(color=ESPN_BLUE, size=12)
)

# Layout
fig4.update_layout(
    height=600,
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    font=dict(color=TEXT_COLOR),
    title=dict(
        text="POINTS FOR vs. DRAFTED",
        font=dict(family="Oswald, sans-serif", size=18, color=TEXT_COLOR),
        x=0.05,
        xanchor='left',
        yanchor='top'
    ),
    margin=dict(l=60, r=60, t=80, b=60),
    xaxis=dict(
        title="Drafted Players on Current Roster",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",
        zeroline=False
    ),
    yaxis=dict(
        title="Points For",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",
        zeroline=False
    )
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Points For vs. Against", "Points For vs. Projected", "Points For vs. Difference", "Points For vs. Drafted", "Weekly Points", "Weekly Score Rank"])

with tab1:
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.plotly_chart(fig4, use_container_width=True)

with tab5:
    st.plotly_chart(fig5, use_container_width=True)

with tab6:
    st.plotly_chart(fig6, use_container_width=True)

st.markdown(f"""
<style>
/* Default tab label text */
.stTabs [role="tab"] p {{
    color: {LIGHT_GREY};
}}

/* Active tab label text */
.stTabs [role="tab"][aria-selected="true"] p {{
    color: {TEXT_COLOR} !important;  /* your highlight color */
    font-weight: 600 !important;
}}
</style>
""", unsafe_allow_html=True)
