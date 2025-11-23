# 7_Draft.py
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
ESPN_BLUE = "#409CFF"
ESPN_GREEN = "#00FF66" # ESPN green for active page border
RED_DARK = "#B22222"

# --- NFL TEAM LOGO MAPPING ---
nfl_logo_map = {
    "ARI": "https://a.espncdn.com/i/teamlogos/nfl/500/ari.png",
    "ATL": "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png",
    "BAL": "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png",
    "BUF": "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png",
    "CAR": "https://a.espncdn.com/i/teamlogos/nfl/500/car.png",
    "CHI": "https://a.espncdn.com/i/teamlogos/nfl/500/chi.png",
    "CIN": "https://a.espncdn.com/i/teamlogos/nfl/500/cin.png",
    "CLE": "https://a.espncdn.com/i/teamlogos/nfl/500/cle.png",
    "DAL": "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png",
    "DEN": "https://a.espncdn.com/i/teamlogos/nfl/500/den.png",
    "DET": "https://a.espncdn.com/i/teamlogos/nfl/500/det.png",
    "GB":  "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
    "HOU": "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png",
    "IND": "https://a.espncdn.com/i/teamlogos/nfl/500/ind.png",
    "JAX": "https://a.espncdn.com/i/teamlogos/nfl/500/jax.png",
    "KC":  "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "LV":  "https://a.espncdn.com/i/teamlogos/nfl/500/lv.png",
    "LAC": "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png",
    "LAR": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png",
    "MIA": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png",
    "MIN": "https://a.espncdn.com/i/teamlogos/nfl/500/min.png",
    "NE":  "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png",
    "NO":  "https://a.espncdn.com/i/teamlogos/nfl/500/no.png",
    "NYG": "https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png",
    "NYJ": "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png",
    "PHI": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png",
    "PIT": "https://a.espncdn.com/i/teamlogos/nfl/500/pit.png",
    "SF":  "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "SEA": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png",
    "TB":  "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png",
    "TEN": "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png",
    "WSH": "https://a.espncdn.com/i/teamlogos/nfl/500/wsh.png"
}

# === PAGE CONFIG ===
st.set_page_config(page_title="Draft", layout="wide")
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
    Draft
</h1>    

""", unsafe_allow_html=True)

# Access the global season from session_state
season = st.session_state.get("season", 2024)

# === LOAD DATA ===
df = load_and_filter_csv("draft.csv", season)

# --- FILTER: TEAM ABBREV (in sidebar, matching season filter style) ---
with st.sidebar:
    selected_team = st.selectbox(
        "Team",
        sorted(df['Team'].unique()),
        key="team_selector"
    )

# --- Create Latest Pos Rank (accounting for nulls) ---
def latest_pos_rank(row):
    if pd.notna(row["Position"]) and pd.notna(row["Position Rank"]):
        try:
            return f"{row['Position']}{int(row['Position Rank'])}"
        except Exception:
            return ""
    else:
        return ""

df["Latest Pos Rank"] = df.apply(latest_pos_rank, axis=1)

# --- Prepare for Drafted Pos Rank calculation ---
df['Overall Pick'] = df['Overall Pick'].fillna(9999)  # Missing picks rank last
df['Position'] = df['Position'].fillna('')  # Temporarily fill nulls to avoid errors

# Calculate draft position rank number within each position group
df['Drafted Pos Rank Num'] = df.groupby('Position')['Overall Pick'].rank(method='first')

# Safely combine into Drafted Pos Rank string
def drafted_pos_rank(row):
    if row['Position'] != '' and pd.notna(row['Drafted Pos Rank Num']):
        try:
            return f"{row['Position']}{int(row['Drafted Pos Rank Num'])}"
        except Exception:
            return ""
    else:
        return ""

df['Drafted Pos Rank'] = df.apply(drafted_pos_rank, axis=1)

# Drop helper column
df.drop(columns=['Drafted Pos Rank Num'], inplace=True)

# === FILTER DF FOR SELECTED TEAM ===
team_df = df[df["Team"] == selected_team].copy()

# --- SELECT COLUMNS & FORMAT ---
display_df = team_df[[
    "Round",
    "Pick Number",
    "Overall Pick",
    "Player",
    "Player ID",
    "Team",
    "Position",
    "NFL Team",
    "Drafted Pos Rank",
    "Latest Pos Rank"
]].copy()

# --- CUSTOM HEADER NAMES ---
header_map = {
    "Round": "Rd",
    "Pick Number": "Pick",
    "Overall Pick": "Overall",
    "Player": "Player",
    "Position": "Pos",
    "Team": "Team",
    "NFL Team": "NFL Team",
    "Drafted Pos Rank": "Drafted Pos Rank",
    "Latest Pos Rank": "Latest Pos Rank"
}

# Define the columns to display (exclude "Opponent Owner")
display_columns = [
    "Round",
    "Pick Number",
    "Overall Pick",
    "Headshot",
    "Player",
    "Drafted Pos Rank",
    "Latest Pos Rank"
]

# --- BUILD HTML TABLE ---
table_html = f"""
<table style='background-color:{CARD_BG}; border-collapse:collapse; width:100%; text-align:center; border:none;'>
    <thead>
        <tr style='color:white; text-transform:uppercase;'>
"""
# Column headers
for col in display_columns:

    if col == "Headshot":
        # Empty header for logo column
        table_html += (
            f"<th style='padding:8px; border-bottom:1px solid #444; border-left: none; border-right: none;"
            f"background-color:{ROW_ALT}; font-family: Oswald, sans-serif; font-weight:175; text-align:left;'></th>"
        )

    elif col == "Player":
        # Left-align Player header
        header_label = header_map.get(col, col)
        table_html += (
            f"<th style='padding:8px; border-bottom:1px solid #444; border-left: none; border-right: none;"
            f"font-family: Oswald, sans-serif; font-weight:175; text-align:left;"
            f"background-color:{ROW_ALT};'>{header_label}</th>"
        )

    else:
        header_label = header_map.get(col, col)
        table_html += (
            f"<th style='padding:8px; border-bottom:1px solid #444; border-left: none; border-right: none;"
            f"font-family: Oswald, sans-serif; font-weight: 175; "
            f"background-color:{ROW_ALT};'>{header_label}</th>"
        )
table_html += "</tr></thead><tbody>"

# --- Define Acquisition Type colors ---
acq_colors = {
    "DRAFT": ESPN_BLUE,
    "ADD": ESPN_GREEN,
    "TRADE": "#F2C94C",  # yellow that complements ESPN blue/green
    "DROPPED": RED_DARK
}

# Table rows
for i, (_, row) in enumerate(display_df.iterrows()):
    # Choose background color based on even/odd row
    bg_color = CARD_BG if i % 2 == 0 else ROW_ALT
    
    table_html += f"<tr style='background-color:{bg_color}; border:none;'>"
    
    for col in display_columns:
        style = "border:none;"

        if col == "Player":
            # Combine Player Name + NFL team logo + Position in one cell
            style += " text-align: left;"

            nfl_team_abbrev = row["NFL Team"]
            logo_url = nfl_logo_map.get(nfl_team_abbrev, "")
            logo_html = f"<img src='{logo_url}' style='height:22px; vertical-align:middle; margin:0 6px;'>" if logo_url else ""

            cell_html = (
                f"<span style='color:{TEXT_COLOR}; font-weight:400; '>{row['Player']}</span>"
                f"{logo_html}"
                f"<span style='color:{LIGHT_GREY}; font-size:0.9em;'>{row['Position']}</span>"
            )

            table_html += f"<td style='padding:8px; {style}'>{cell_html}</td>"

        elif col == "Headshot":
            player_id = row.get("Player ID", None)
            pos_value = row.get("Position", "")
            team_abbrev_nfl = row.get("NFL Team", "")

            # Show NFL team logo if D/ST, else player headshot
            if pos_value == "D/ST":
                headshot_url = nfl_logo_map.get(team_abbrev_nfl, "")
                headshot_html = f"<img src='{headshot_url}' style='height:40px; border-radius:4px;'>"
            elif pd.notna(player_id):
                headshot_url = f"https://a.espncdn.com/i/headshots/nfl/players/full/{int(player_id)}.png"
                headshot_html = f"<img src='{headshot_url}' style='height:40px; border-radius:4px;'>"
            else:
                headshot_html = ""

            table_html += f"<td style='padding:8px; text-align:center; border:none;'>{headshot_html}</td>"

        else:
            cell_value = row[col]

            # --- Apply Acquisition Type colors ---
            if col == "Acquisition Type":
                acq_color = acq_colors.get(cell_value, LIGHT_GREY)
                cell_html = f"<span style='color:{acq_color}; font-weight:400;'>{cell_value}</span>"
            
            # Apply color for "Overall Pick"
            elif col == "Overall Pick":
                cell_html = f"<span style='color:{ESPN_BLUE};'>{cell_value}</span>"
            elif col == "Round":
                cell_html = f"<span style='color:{LIGHT_GREY};'>{cell_value}</span>"
            elif col == "Pick Number":
                cell_html = f"<span style='color:{LIGHT_GREY};'>{cell_value}</span>"
            else:
                cell_html = cell_value

            table_html += f"<td style='padding:8px; {style}'>{cell_html}</td>"

    table_html += "</tr>"

table_html += "</tbody></table>"

# --- DISPLAY TABLE ---
st.markdown(table_html, unsafe_allow_html=True)