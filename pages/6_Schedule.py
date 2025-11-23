# 6_Schedule.py
import streamlit as st
import pandas as pd
from utils import render_season_filter, load_and_filter_csv

# Show the global filter
season = render_season_filter()

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

# === PAGE CONFIG ===
st.set_page_config(page_title="Schedule", layout="wide")
st.markdown(f"<style>body {{ background-color: {DARK_BG}; }}</style>", unsafe_allow_html=True)

# === BACKGROUND COLOR ===
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            
.stApp {{
    background-color: {DARK_BG};
    color: white;
}}  

/* Remove default page title space */
h1 {{
    display: none;
}}

.sidebar-header {{ color: {TEXT_COLOR}; font-size: 20px !important; font-weight: 450; margin-bottom: 0; font-family: 'Oswald', sans-serif !important; }}
.sidebar-text {{ color: {LIGHT_GREY}; font-size: 16px; }}
div[data-testid="stSidebarNav"] li a[aria-current="page"] {{
    border-left: 5px solid {ESPN_GREEN};
    background-color: {ROW_ALT};
}}

div[data-testid="stSidebarNav"] li a[aria-current="page"] {{
    border-left: 5px solid {ESPN_GREEN};
    background-color: {ROW_ALT};
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

/* Main app background */
.stApp {{ background-color: {DARK_BG}; }}

/* Card container used by Streamlit (keep your previous styling but smaller padding) */
.st-emotion-cache-1px2j3i {{
    background-color: {CARD_BG} !important;
    padding: 16px !important;
    border-radius: 8px !important;
    margin-bottom: 18px !important;
}}

.sidebar-header {{ color: {TEXT_COLOR}; font-size: 20px !important; font-weight: 450; margin-bottom: 0; font-family: 'Oswald', sans-serif !important; }}
.sidebar-text {{ color: {LIGHT_GREY}; font-size: 16px; }}
div[data-testid="stSidebarNav"] li a[aria-current="page"] {{
    border-left: 5px solid {ESPN_GREEN};
    background-color: {ROW_ALT};
}}

</style>

<h1 style="margin-bottom: 25px;">
    <img src="https://a.espncdn.com/combiner/i?img=i/fantasy/ffl.png&w=100&h=100&transparent=true"
         style="width:40px; height:40px; vertical-align:middle;"/>
    Schedule
</h1>
            
""", unsafe_allow_html=True)

# Access the global season from session_state
season = st.session_state.get("season", 2024)

# === LOAD DATA ===
df = load_and_filter_csv("team_weekly.csv", season)

# --- EXCLUDE ROWS WHERE TEAM SCORE IS 0 ---
df = df[df["Team Score"] != 0]

# --- FILTER: TEAM ABBREV (in sidebar, matching season filter style) ---
with st.sidebar:
    selected_team = st.selectbox(
        "Team",
        sorted(df['Abbrev'].unique()),
        key="team_selector"
    )

# Expecting: Week, Type, Abbrev, Opponent Abbrev, Score, Result, Weekly Score Rank, Rank

# === FILTER DF FOR SELECTED TEAM ===
team_df = df[df["Abbrev"] == selected_team].copy()

# --- CUMULATIVE RECORD ---
team_df["Record"] = "(" + team_df["Wins"].astype(str) + "-" + team_df["Losses"].astype(str) + ")"

# --- SELECT COLUMNS & FORMAT ---
display_df = team_df[[
    "Week",
    "Type",
    "Opponent Abbrev",
    "Opponent Owner",
    "Score",
    "Result",
    "Record",
    "Weekly Score Rank",
    "Rank"
]].copy()

# --- CUSTOM HEADER NAMES ---
header_map = {
    "Week": "Week",
    "Type": "Type",
    "Opponent Abbrev": "Opponent",
    # "Opponent Owner": "Owner",
    "Score": "Score",
    "Result": "Result",
    "Record": "Record",
    "Weekly Score Rank": "Score Rank",
    "Rank": "Standings"
}

# Define the columns to display (exclude "Opponent Owner")
display_columns = [
    "Week",
    "Type",
    "Score", #includes Result
    # "Result",
    "Opponent Abbrev",  # combined cell with Opponent Owner
    "Record",
    "Weekly Score Rank",
    "Rank"
]

# --- BUILD HTML TABLE ---
table_html = f"""
<table style='background-color:{CARD_BG}; border-collapse:collapse; width:100%; text-align:center; border:none;'>
    <thead>
        <tr style='color:{TEXT_COLOR}; text-transform:uppercase;'>
"""
# Column headers
for col in display_columns:
    header_label = header_map.get(col, col)
    table_html += (
        f"<th style='padding:8px; border-bottom:1px solid #444; border-left: none; border-right: none;"
        f"font-family: Oswald, sans-serif; font-weight: 175; "
        f"background-color:{ROW_ALT};'>{header_label}</th>"
    )
table_html += "</tr></thead><tbody>"

# Table rows
for i, (_, row) in enumerate(display_df.iterrows()):
    # Choose background color based on even/odd row
    bg_color = CARD_BG if i % 2 == 0 else ROW_ALT
    
    table_html += f"<tr style='background-color:{bg_color}; border:none; color:{LIGHT_GREY}'>"
    
    for col in display_columns:
        style = "border:none;"

        # Combine Opponent Abbrev and Opponent Owner in same cell
        if col == "Opponent Abbrev":
            style += " text-align: center "
            # Use inline spans with colors and line break
            cell_html = (
                f"<span style='color:{ESPN_BLUE}; font-weight:600; '>{row['Opponent Abbrev']}</span><br>"
                f"<span style='color:{LIGHT_GREY}; font-size:0.9em;'>{row['Opponent Owner']}</span>"
            )
            table_html += f"<td style='padding:8px; {style}'>{cell_html}</td>"

        elif col == "Week":
            style += f" color:{LIGHT_GREY};"
            table_html += f"<td style='padding:8px; {style}'>{row[col]}</td>"

        elif col == "Score":
            style += " text-align: center;"
            result_abbrev = "(W)" if row["Result"] == "Win" else "(L)" if row["Result"] == "Loss" else row["Result"]

            # Choose color
            if result_abbrev == "(W)":
                result_color = GREEN_DARK
            elif result_abbrev == "(L)":
                result_color = RED_DARK
            else:
                result_color = LIGHT_GREY

            cell_html = (
                f"<span style='color:{ESPN_BLUE};'>{row[col]}</span>  "
                f"<span style='color:{result_color}; font-weight:600;'>{result_abbrev}</span>"
            )

            table_html += f"<td style='padding:8px; {style}'>{cell_html}</td>"

        elif col == "Type":
            if row[col] == "Playoff":
                style += f" font-weight:bold; font-size:1.0em;"
            else:
                style += f" color:{LIGHT_GREY}; font-size:1.0em;"
            table_html += f"<td style='padding:8px; {style}'>{row[col]}</td>"

        elif col == "Result":
            style += f" text-align: center; color:{LIGHT_GREY};"
            display_val = "(W)" if row[col] == "Win" else "(L)" if row[col] == "Loss" else row[col]
            table_html += f"<td style='padding:8px; {style}'>{display_val}</td>"

        else:
            table_html += f"<td style='padding:8px; {style}'>{row[col]}</td>"

    table_html += "</tr>"

table_html += "</tbody></table>"

# --- DISPLAY TABLE ---
st.markdown(table_html, unsafe_allow_html=True)

# --- FOOTNOTES BELOW TABLE ---
st.markdown(
    f"""
    <div style='text-align:left; color:{LIGHT_GREY}; font-size:14px; margin-top:10px;'>
        <p><strong>SCORE RANK</strong> indicates how your weekly score ranked relative to all teams that week (1 = highest score).</p>
        <p><strong>STANDINGS</strong> reflects your place in the league standings at the completion of the listed week.</p>
    </div>
    """,
    unsafe_allow_html=True
)
