# 1_Total_Matchups.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# === THEME COLORS ===
DARK_BG = "#121212"
CARD_BG = "#202124"
ROW_ALT = "#1A1A1A"
TEXT_COLOR = "#FFFFFF"
LIGHT_GREY = "#A9A9A9"
GREY = "#4C4C4C"
RED = "#FF0000"
ESPN_BLUE = "#3F8EF3"
ESPN_GREEN = "#00FF66"
GREEN_DARK = "#228B22"
RED_DARK = "#B22222"

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
st.set_page_config(page_title="Total Matchups", layout="wide")
st.markdown(f"<style>body {{ background-color: {DARK_BG}; }}</style>", unsafe_allow_html=True)

# === HEADER ===
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');

.stApp {{
    background-color: {DARK_BG};
    color: white;
}}  

h1 {{
    font-family: 'Oswald', sans-serif !important;
    font-weight: 500 !important;
    font-size: 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px;
}}

div[data-testid="stSidebarNav"] li a[aria-current="page"] {{
    border-left: 5px solid {ESPN_GREEN};
    background-color: {ROW_ALT};
}}

table {{
    color: {LIGHT_GREY};
}}
</style>

<h1 style="margin-bottom: 25px;">
    <img src="https://a.espncdn.com/combiner/i?img=i/fantasy/ffl.png&w=100&h=100&transparent=true"
         style="width:40px; height:40px; vertical-align:middle;"/>
    Total Matchups
</h1>
""", unsafe_allow_html=True)

# === LOAD DATA ===
df = pd.read_csv("total_matchups.csv")

# Temporary Exclusion
#df = df[~((df["Season"] == 2025) & (df["Week"] > 11))]

# Filter out invalid rows
df = df[df["Team Score"] != 0]

# === SIDEBAR FILTERS ===
st.sidebar.markdown("### Season")
all_seasons = sorted(df["Season"].unique())

selected_seasons = st.sidebar.multiselect(
    "",
    options=all_seasons,
    default=all_seasons  # default: show all
)

# Apply filter
df = df[df["Season"].isin(selected_seasons)]

# Add cumulative Wins and Losses across all seasons (no reset per season)
df = df.sort_values(["Abbrev", "Season", "Week"]).copy()

df["Wins"] = df.groupby("Abbrev")["Win"].cumsum()
df["Losses"] = df.groupby("Abbrev")["Loss"].cumsum()

# --- Convert Actual Result to numeric wins/losses ---
df["Actual Win"] = (df["Actual Result"] == "Win").astype(int)
df["Actual Loss"] = (df["Actual Result"] == "Loss").astype(int)

# --- Aggregate to unique Season–Week–Abbrev combinations ---
weekly_actual = (
    df.groupby(["Abbrev", "Season", "Week"])
    .agg(
        WinsThisWeek=("Actual Win", "sum"),
        LossesThisWeek=("Actual Loss", "sum")
    )
    .reset_index()
)

# --- Compute cumulative totals (not resetting per season) ---
weekly_actual["WinsToDate"] = weekly_actual.groupby("Abbrev")["WinsThisWeek"].cumsum()
weekly_actual["LossesToDate"] = weekly_actual.groupby("Abbrev")["LossesThisWeek"].cumsum()

# --- Compute Actual Win % ---
weekly_actual["Actual Win %"] = (
    weekly_actual["WinsToDate"] /
    (weekly_actual["WinsToDate"] + weekly_actual["LossesToDate"])
).round(3)

# --- Merge back so all rows for that (Season, Week, Abbrev) share the same Actual Win % ---
df = df.merge(
    weekly_actual[["Season", "Week", "Abbrev", "Actual Win %"]],
    on=["Season", "Week", "Abbrev"],
    how="left"
)

# --- Add True Win % column (cumulative across all seasons) ---
df["True Win %"] = (
    df["Wins"] / (df["Wins"] + df["Losses"])
).round(3)

# === CALCULATE TEAM-LEVEL STATS ===
score_stats = (
    df.groupby("Abbrev")["Team Score"]
    .agg(
        AVG="mean",
        MED="median",
        HIGH="max",
        LOW="min"
    )
    .reset_index()
)

# === PREPARE STANDINGS ===
latest_df = df.sort_values(["Abbrev", "Season", "Week"]).groupby("Abbrev").tail(1)

# Combine stats
latest_df = latest_df.merge(score_stats, on="Abbrev", how="left")

# Combine team abbrev + owner
latest_df["Abbrev_Owner"] = latest_df.apply(
    lambda x: f"<span style='color:{ESPN_BLUE}; font-weight:600;'>{x['Abbrev']}</span><br>"
              f"<span style='color:{LIGHT_GREY}; font-size:0.9em;'>{x['Owner']}</span>",
    axis=1
)

# --- CALCULATE DIFF ---
latest_df["Diff"] = (latest_df["True Win %"] - latest_df["Actual Win %"]) * 100

# --- FORMAT DISPLAY ---
latest_df["True Win % Display"] = (latest_df["True Win %"] * 100).round(1).astype(str) + "%"
latest_df["Actual Win % Display"] = (latest_df["Actual Win %"] * 100).round(1).astype(str) + "%"
latest_df["AVG"] = latest_df["AVG"].round(1)
latest_df["MED"] = latest_df["MED"].round(1)
latest_df["HIGH"] = latest_df["HIGH"].round(1)
latest_df["LOW"] = latest_df["LOW"].round(1)

# --- Stat Max and Mins ---
stat_cols = ["AVG", "MED", "HIGH", "LOW"]

max_vals = {col: latest_df[col].max() for col in stat_cols}
min_vals = {col: latest_df[col].min() for col in stat_cols}

# --- SORT + RANK ---
latest_df = latest_df.sort_values("True Win %", ascending=False).reset_index(drop=True)
latest_df["Rank"] = latest_df.index + 1

# === COLUMNS TO DISPLAY ===
display_columns = [
    "Rank", "Abbrev_Owner", "Wins", "Losses",
    "True Win % Display", "Actual Win % Display", "Diff",
    "AVG", "MED", "HIGH", "LOW"
]

header_map = {
    "Rank": "",
    "Abbrev_Owner": "Team",
    "Wins": "W",
    "Losses": "L",
    "True Win % Display": "True Win %",
    "Actual Win % Display": "Actual Win %",
    "Diff": "Diff (True - Actual)",
    "AVG": "AVG",
    "MED": "MED",
    "HIGH": "HIGH",
    "LOW": "LOW",
}

# === BUILD HTML TABLE ===
table_html = f"""
<table style='background-color:{CARD_BG}; border-collapse:collapse; width:100%; text-align:center; border:none;'>
    <thead>
        <tr style='color:white; text-transform:uppercase;'>
"""

# Header row
for col in display_columns:
    header_label = header_map[col]
    th_style = (
        f"padding:3px; border-bottom:1px solid #444; border-left:none; border-right:none; "
        f"font-family: Oswald, sans-serif; font-weight:175; background-color:{ROW_ALT};"
    )
    if col == "Abbrev_Owner":
        th_style += " text-align:left;"
    table_html += f"<th style='{th_style}'>{header_label}</th>"

table_html += "</tr></thead><tbody>"

# Body rows
for i, (_, row) in enumerate(latest_df.iterrows()):
    bg_color = CARD_BG if i % 2 == 0 else ROW_ALT
    table_html += f"<tr style='background-color:{bg_color}; border:none;'>"

    for col in display_columns:
        style = "border:none;"
        cell_html = ""

        if col == "Abbrev_Owner":
            style += " text-align:left;"
            cell_html = row[col]

        elif col == "Rank":
            style += f" color:{LIGHT_GREY};"
            cell_html = row[col]

        elif col in ["Wins", "Losses"]:
            style += f" color:{LIGHT_GREY};"
            cell_html = int(row[col])

        elif col == "True Win % Display":
            style += f" color:{ESPN_GREEN}; font-weight:600;"
            cell_html = row[col]

        elif col == "Actual Win % Display":
            style += f" color:{ESPN_BLUE}; font-weight:600;"
            cell_html = row[col]

        elif col == "Diff":
            diff_val = round(row["Diff"], 1)
            color = GREEN_DARK if diff_val > 0 else RED_DARK if diff_val < 0 else LIGHT_GREY
            sign = "+" if diff_val > 0 else ""
            cell_html = f"<span style='color:{color}; font-weight:600;'>{sign}{diff_val}%</span>"

        elif col in ["AVG", "MED", "HIGH", "LOW"]:
            val = row[col]
        
            if val == max_vals[col]:
                style += f" color:{GREEN_DARK}; font-weight:600;"
            elif val == min_vals[col]:
                style += f" color:{RED_DARK}; font-weight:600;"
            else:
                style += f" color:{LIGHT_GREY};"
        
            cell_html = f"{val:.1f}"

        table_html += f"<td style='padding:4px; {style}'>{cell_html}</td>"

    table_html += "</tr>"

table_html += "</tbody></table>"

# === True Win % vs. Actual Win % ===

# Assuming latest_df is already defined
x = latest_df['Actual Win %']
y = latest_df['True Win %']
labels = latest_df['Abbrev']

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

# Vertical median line (True Win %)
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

# Horizontal median line (Actual Win %)
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
        text="TRUE WIN % vs. ACTUAL WIN %",
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
        title="Actual Win %",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",   # subtle gray gridlines
        zeroline=False
    ),
    
    # Y-axis configuration
    yaxis=dict(
        title="True Win %",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",   # subtle gray gridlines
        zeroline=False
    )
)

# === True Win % vs. Difference ===

# Assuming latest_df is already defined
x2 = latest_df['Diff']
y2 = latest_df['True Win %']
labels = latest_df['Abbrev']

# Medians
x_med2 = np.median(x2)
y_med2 = np.median(y2)

fig2 = go.Figure()

# Map team colors

point_colors = [TEAM_COLORS[abbr] for abbr in labels]

# Scatter points with always-visible labels
fig2.add_trace(go.Scatter(
    x=x2, 
    y=y2, 
    mode="markers+text",       # show both dots + text
    text=labels, 
    textposition="top center", # label placement
    marker=dict(
        size=16,
        color=point_colors
    ),
    textfont=dict(color="#FFFFFF", size=15)
))

# QUADRANTS

# Define quadrant label positions
quadrant_positions = [
    ("High Scoring<br>Unfortunate Matchups",  (x_med2 + max(x2)) / 2, (y_med2 + max(y2)) / 2, "rgba(0, 200, 0, 0.12)"),  # Q1
    ("Low Scoring<br>Unfortunate Matchups",   (x_med2 + max(x2)) / 2, (y_med2 + min(y2)) / 2, "rgba(0, 120, 255, 0.12)"), # Q2
    ("Low Scoring<br>Fortunate Matchups",    (x_med2 + min(x2)) / 2, (y_med2 + min(y2)) / 2, "rgba(255, 0, 0, 0.12)"),   # Q3
    ("High Scoring<br>Fortunate Matchups",   (x_med2 + min(x2)) / 2, (y_med2 + max(y2)) / 2, "rgba(255, 165, 0, 0.12)")  # Q4
]

# Add shaded quadrant rectangles
fig2.add_shape(
    type="rect",
    x0=x_med2, y0=y_med2, x1=max(x2), y1=max(y2),
    fillcolor="rgba(0, 200, 0, 0.05)", line=dict(width=0)
)
fig2.add_shape(
    type="rect",
    x0=x_med2, y0=min(y2), x1=max(x2), y1=y_med2,
    fillcolor="rgba(0, 120, 255, 0.05)", line=dict(width=0)
)
fig2.add_shape(
    type="rect",
    x0=min(x2), y0=min(y2), x1=x_med2, y1=y_med2,
    fillcolor="rgba(255, 0, 0, 0.05)", line=dict(width=0)
)
fig2.add_shape(
    type="rect",
    x0=min(x2), y0=y_med2, x1=x_med2, y1=max(y2),
    fillcolor="rgba(255, 165, 0, 0.05)", line=dict(width=0)
)

# Add quadrant labels (centered)
for label, x_pos, y_pos, _color in quadrant_positions:
    fig2.add_annotation(
        x=x_pos,
        y=y_pos,
        text=label,
        showarrow=False,
        font=dict(size=12, color=TEXT_COLOR),
        opacity=0.7
    )

# Vertical median line (True Win %)
fig2.add_shape(type="line",
    x0=x_med2, x1=x_med2, y0=min(y2), y1=max(y2),
    line=dict(color="#3F8EF3", dash="dot", width=2)
)
fig2.add_annotation(
    x=x_med2, y=max(y2),
    text=f"Median: {x_med2:.1f}",
    showarrow=False,
    yshift=20,
    font=dict(color="#3F8EF3", size=12)
)

# Horizontal median line (Difference)
fig2.add_shape(type="line",
    x0=min(x2), x1=max(x2), y0=y_med2, y1=y_med2,
    line=dict(color="#3F8EF3", dash="dot", width=2)
)
fig2.add_annotation(
    x=max(x2), y=y_med2,
    text=f"Median: {y_med2:.1f}",
    showarrow=False,
    xshift=40,
    font=dict(color="#3F8EF3", size=12)
)

# Layout styling
fig2.update_layout(
    height=600,
    # Background colors
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    
    # Font for axes and other text
    font=dict(color=TEXT_COLOR),
    
    # Chart title
    title=dict(
        text="TRUE WIN % vs. DIFFERENCE (TRUE - ACTUAL)",
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
        title="Difference (True Win % - Actual Win %)",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",   # subtle gray gridlines
        zeroline=False
    ),
    
    # Y-axis configuration
    yaxis=dict(
        title="True Win %",
        tickfont=dict(color=LIGHT_GREY),
        showgrid=True,
        gridcolor="#2A2A2A",   # subtle gray gridlines
        zeroline=False
    )
)

# === Matchup Heatmap ===

# --- Build the matrix of total wins (Abbrev vs Opponent) ---
h2h_df = (
    df.groupby(["Abbrev", "Opponent"])["Win"]
    .sum()
    .unstack(fill_value=0)
)

# Nullify self-matchups
for team in h2h_df.index:
    if team in h2h_df.columns:
        h2h_df.loc[team, team] = np.nan

# --- Create text labels (replace NaN with '-') ---
text_df = h2h_df.copy().fillna("")

# Sort both axes alphabetically (optional, or you can sort by True Win % instead)
h2h_df = h2h_df.reindex(sorted(h2h_df.index))
h2h_df = h2h_df[sorted(h2h_df.columns)]

# Define your color scale (use ESPN-green for high, neutral for mid, red for low)
colorscale = [
    [0.0, "#D64545"],  # few wins = red
    [0.5, "#1A1A1A"],  # neutral
    [1.0, "#21C55D"],  # many wins = green
]

# Create Plotly heatmap
fig_h2h = go.Figure(
    data=go.Heatmap(
        z=h2h_df.values,
        x=h2h_df.columns,
        y=h2h_df.index,
        colorscale=colorscale,
        zmin=h2h_df.values.min(),
        zmax=h2h_df.values.max(),
        showscale=False,
        hovertemplate="%{y} vs %{x}<br>Wins: %{z}<extra></extra>",
        # Make NaNs visually match the background
        zauto=False,
        hoverongaps=False,
        colorbar=dict(
            title=dict(
                text="Total Wins",
                font=dict(color=TEXT_COLOR)
            ),
            tickfont=dict(color=LIGHT_GREY)
        ),
        text=text_df.values,
        texttemplate="%{text}",
        textfont=dict(color=TEXT_COLOR, size=14)
    )
)


# --- Layout styling to match your theme ---
fig_h2h.update_layout(
    title=dict(
        text="HEAD-TO-HEAD WINS",
        font=dict(family="Oswald, sans-serif", size=18, color=TEXT_COLOR),
        x=0.05,
        xanchor="left"
    ),
    plot_bgcolor=CARD_BG,
    paper_bgcolor=CARD_BG,
    margin=dict(l=80, r=60, t=80, b=60),
    xaxis=dict(
        side="bottom",
        title=dict(text="Opponent", font=dict(color=TEXT_COLOR)),
        tickfont=dict(color=ESPN_BLUE, size=14)
    ),
    yaxis=dict(
        title=dict(text="Team", font=dict(color=TEXT_COLOR)),
        autorange="reversed",
        tickfont=dict(color=ESPN_BLUE, size=14)
    ),
    height=600
)



# === DISPLAY IN TABS ===
tab1, tab2, tab3, tab4 = st.tabs([
    "Standings",
    "True Win % vs. Actual Win %",
    "True Win % vs. Diff.",
    "Head-to-Head"
])

# --- Tab1: Standings ---
with tab1:
    st.markdown(table_html, unsafe_allow_html=True)

with tab2:
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.plotly_chart(fig2, use_container_width=True)    

with tab4:
    st.plotly_chart(fig_h2h, use_container_width=True)

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

# --- FOOTNOTES ---
st.markdown(
    f"""
    <div style='text-align:left; color:{LIGHT_GREY}; font-size:15px; margin-top:10px;'>
        <p>
            The <strong><span style='color:{TEXT_COLOR};'>TOTAL MATCHUPS</span></strong> standings 
            reflect the hypothetical league in which each team plays all teams every week.
        </p>
        <p>
            This provides us <span style='color:{ESPN_GREEN};'>an accurate representation of each team's weekly performance independent of 
            schedule luck</span> and can be measured by <strong><span style='color:{ESPN_GREEN};'>TRUE WIN %</span></strong>.
        </p>
        <p>
            <strong><span style='color:{ESPN_GREEN};'>TRUE WIN %</span></strong> 
            is the percentage of all hypothetical matchups that your team has won across all weeks.
        </p>
        <p>
            As a result, each team has 11 weekly matchups.
        </p>
        <p>
            If your team had the highest point total for a given week, then you will have gone 11-0 during that week.
        </p>
        <p>
            If your team instead had the 6th highest point total, then you would have outscored 6 of the 11 opposing teams,
            and therefore went 6-5 for that week.
        </p>
        <p>
            <strong><span style='color:{ESPN_BLUE};'>ACTUAL WIN %</span></strong> 
            is the percentage of scheduled weekly matchups that your team actually won over that same duration.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
