# 5_Standings.py
import streamlit as st
import pandas as pd
from utils import render_season_filter, load_and_filter_csv

# Show the global filter
season = render_season_filter()

# Define theme colors for consistency
DARK_BG = "#121212"
CARD_BG = "#202124"
ROW_ALT = "#1A1A1A"
TEXT_COLOR = "#FFFFFF"
LIGHT_GREY = "#A9A9A9"
ESPN_BLUE = "#3F8EF3"
ESPN_GREEN = "#00FF66" # ESPN green for active page border
GREEN_DARK = "#228B22"
RED_DARK = "#B22222"

# === PAGE CONFIG ===
st.set_page_config(page_title="Standings", layout="wide")
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
    Standings
</h1>
""", unsafe_allow_html=True)

# Access the global season from session_state
season = st.session_state.get("season", 2024)

# === LOAD DATA ===
df = load_and_filter_csv("team_weekly.csv", season)

# --- EXCLUDE ROWS WHERE TEAM SCORE IS 0 ---
df = df[df["Team Score"] != 0]

# --- CUMULATIVE RECORD ---
df["Record"] = "(" + df["Wins"].astype(str) + "-" + df["Losses"].astype(str) + ")"

# Ensure Week is numeric for filtering
df["Week"] = pd.to_numeric(df["Week"], errors="coerce")

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
df_max_week = df[df["Week"] == max_week][["Abbrev", "Owner", "Rank", "Record"]]

# --- MERGE cumulative sums WITH max week info ---
agg_df = pd.merge(df_max_week, cumulative_sums, on=["Abbrev", "Owner"])

# --- SORT BY RANK ASCENDING ---
agg_df = agg_df.sort_values(by="Rank", ascending=True).reset_index(drop=True)

# --- RENAME COLUMNS FOR DISPLAY ---
header_map = {
    "Rank": "",
    "Abbrev": "Team",
    "Owner": "Owner",
    "Record": "Record",
    "Team_Score_Sum": "PF",
    "Team_Projected_Sum": "PROJ",
    "Points_Against_Sum": "PA",
    "AVG": "AVG",
    "HIGH":"HIGH",
    "MED": "MED",
    "LOW": "LOW"
}

# --- COLUMNS TO DISPLAY ---
display_columns = ["Rank", "Abbrev", "Record", "Team_Score_Sum", "Team_Projected_Sum", "Points_Against_Sum", "AVG", "HIGH", "MED", "LOW"]

highlight_cols = [
    "Team_Score_Sum", 
    "Team_Projected_Sum", 
    "AVG", 
    "HIGH", 
    "MED",
    "Points_Against_Sum"
]

col_min = {col: agg_df[col].min() for col in highlight_cols}
col_max = {col: agg_df[col].max() for col in highlight_cols}

# --- BUILD HTML TABLE ---
table_html = f"""
<table style='background-color:{CARD_BG}; border-collapse:collapse; width:100%; text-align:center; border:none;'>
    <thead>
        <tr style='color:white; text-transform:uppercase;'>
"""

# Build header row
for col in display_columns:
    header_label = header_map.get(col, col)

    th_style = (
        f"padding:4px; border-bottom:1px solid #444; border-left:none; border-right:none; "
        f"font-family: Oswald, sans-serif; font-weight: 175; "
        f"background-color:{ROW_ALT};"
    )

    # Override alignment for Abbrev (Team) column only
    if col == "Abbrev":
        th_style += " text-align:left;"
    else:
        th_style += " text-align:center;"

    table_html += f"<th style='{th_style}'>{header_label}</th>"

table_html += "</tr></thead><tbody>"

# Build table body rows
for i, (_, row) in enumerate(agg_df.iterrows()):
    bg_color = CARD_BG if i % 2 == 0 else ROW_ALT
    table_html += f"<tr style='background-color:{bg_color}; border:none;'>"
    
    for col in display_columns:
        style = "border:none;"
        if col == "Abbrev":
            # Combine Abbrev + Owner in one cell with styling
            style += " text-align: left;"
            cell_html = (
                f"<span style='color:{ESPN_BLUE}; font-weight:600; '>{row['Abbrev']}</span><br>"
                f"<span style='color:{LIGHT_GREY}; font-size:0.9em;'>{row['Owner']}</span>"
            )
            table_html += f"<td style='padding:4px; {style}'>{cell_html}</td>"

        elif col == "Rank":
            style += f" color:{LIGHT_GREY};"
            table_html += f"<td style='padding:8px; {style}'>{row[col]}</td>"

        elif col == "Record":
            style += f" color:{LIGHT_GREY};"
            table_html += f"<td style='padding:8px; {style}'>{row[col]}</td>"

        else:
            style += " text-align: center;"
            value = row[col]  # define once for all numeric columns
        
            # --- Columns where MAX = GREEN, MIN = RED ---
            if col in ["Team_Score_Sum", "Team_Projected_Sum", "AVG", "HIGH", "MED", "LOW"]:
                if value == col_max[col]:
                    color = GREEN_DARK
                elif value == col_min[col]:
                    color = RED_DARK
                else:
                    color = LIGHT_GREY
        
            # --- Points Against: MAX = RED, MIN = GREEN ---
            elif col == "Points_Against_Sum":
                if value == col_max[col]:
                    color = RED_DARK
                elif value == col_min[col]:
                    color = GREEN_DARK
                else:
                    color = LIGHT_GREY
        
            else:
                color = LIGHT_GREY  # fallback
        
            style += f" color:{color};"
            cell_html = f"{value:,.1f}"
            table_html += f"<td style='padding:8px; {style}'>{cell_html}</td>"

        
    table_html += "</tr>"

table_html += "</tbody></table>"

# --- DISPLAY TABLE ---
st.markdown(table_html, unsafe_allow_html=True)

