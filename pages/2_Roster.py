# 2_Roster.py
import streamlit as st
import pandas as pd
import numbers
from utils import render_season_filter, load_and_filter_csv

# Show the global filters
season = render_season_filter()

# Define theme colors for consistency
DARK_BG = "#121212"
CARD_BG = "#202124"
ROW_ALT = "#1A1A1A"
TEXT_COLOR = "#FFFFFF"
LIGHT_GREY = "#A9A9A9"
RED = "#FF0000"
ESPN_BLUE = "#3F8EF3"
ESPN_GREEN = "#00FF66" # ESPN green for active page border
GREEN_DARK = "#228B22"
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
st.set_page_config(page_title="Roster", layout="wide")
st.markdown(f"<style>body {{ background-color: {DARK_BG}; }}</style>", unsafe_allow_html=True)

# === BACKGROUND COLOR + FILTER STYLE ===
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
    Roster
</h1>

""", unsafe_allow_html=True)

# Access the global season from session_state
season = st.session_state.get("season", 2024)

# === LOAD DATA ===
df = load_and_filter_csv("roster.csv", season)

# --- FILTER: TEAM ABBREV (in sidebar, matching season filter style) ---
with st.sidebar:
    selected_team = st.selectbox(
        "Team",
        sorted(df['Abbrev'].unique()),
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

df["Pos Rank"] = df.apply(latest_pos_rank, axis=1)

# === FILTER DF FOR SELECTED TEAM ===
team_df = df[df["Abbrev"] == selected_team].copy()

# Custom sort order for "Slot"
slot_order = {
    "QB": 1,
    "RB": 2,
    "WR": 3,
    "TE": 4,
    "FLEX": 5,
    "D/ST": 6,
    "K": 7,
    "BE": 8,
    "IR": 9
}

# Create a helper column for sorting
team_df["Slot_sort"] = team_df["Slot"].map(slot_order)

# Sort by that column, then drop it
team_df = team_df.sort_values(by="Slot_sort", kind="stable").drop(columns="Slot_sort")

# Drop duplicates
team_df = team_df.drop_duplicates(subset=["Player"], keep="first")

# Calculate scoring difference
team_df["Difference"] = np.where(
    team_df["Points (Avg)"] != 0,
    team_df["Points (Avg)"] - team_df["Projected (Avg)"],
    np.nan
)

# --- SELECT COLUMNS & FORMAT ---
display_df = team_df[[
    "Slot",
    "Player",
    "Player ID",
    "Abbrev",
    "Position",
    "NFL Team",
    "Points (Total)",
    "Points (Avg)",
    "Projected (Avg)",
    "Difference",
    "Projected (Total)",
    "Percent Rostered",
    "Percent Started",
    "Acquisition Type",
    "Pos Rank"
]].copy()

# --- CUSTOM HEADER NAMES ---
header_map = {
    "Slot":"",
    "Player":"Player",
    "Position":"Pos",
    "NFL Team":"NFL Team",
    "Points (Total)":"Pts",
    "Points (Avg)":"Avg",
    "Projected (Avg)":"Avg (Proj)",
    "Projected (Total)":"Pts (Proj)",
    "Percent Rostered":"%Rost",
    "Percent Started":"%Start",
    "Acquisition Type":"Acq Type",
    "Pos Rank":"Pos Rk",
    "Difference":"+/-"
}

# Define the columns to display (exclude "Opponent Owner")
display_columns = [
    "Slot",
    "Headshot",
    "Player",
    "Pos Rank",
    "Points (Total)",
    "Projected (Total)",
    "Points (Avg)",
    "Projected (Avg)",
    "Difference",
    "Percent Rostered",
    "Percent Started",
    "Acquisition Type"
]

# === TEAM INFO CONTAINER ===
team_abbrev = team_df["Abbrev"].iloc[0]
team_owner = team_df["Owner"].iloc[0]
team_record = team_df["Record"].iloc[0]

# === POSITION COUNTS ===
position_counts = team_df['Position'].value_counts()

# Desired position order
pos_order = ["QB", "RB", "WR", "TE", "D/ST", "K"]
pos_order = [pos for pos in pos_order if pos in position_counts.index]

COL_WIDTH = "60px"  # fixed width for alignment

pos_labels_html = ""
pos_counts_html = ""

for pos in pos_order:
    count = position_counts.get(pos, 0)
    # Row 1: ovals
    pos_labels_html += f"<div style='display:inline-block;width:{COL_WIDTH};text-align:center;'>" \
                       f"<div style='display:inline-block;padding:2px 16px;border:1px solid {ESPN_BLUE};" \
                       f"border-radius:16px;color:{ESPN_BLUE};font-family:Oswald,sans-serif;font-size:0.85em; white-space:nowrap'>{pos}</div></div>"
    # Row 2: counts
    pos_counts_html += f"<div style='display:inline-block;width:{COL_WIDTH};text-align:center;color:{TEXT_COLOR};" \
                       f"font-size:16px;font-family:Oswald,sans-serif;margin-top:2px;'>{str(count)}</div>"

# === LEFT PANEL PARTS (team info + position counts, inner only; outer card added below) ===
left_panel_inner = f"""
<div>
  <div style='margin-left:8px;margin-top: 8px;'>
    <div style='color:white; font-family:Oswald,sans-serif; font-size:28px; line-height:1;'>{team_abbrev}</div>
    <div style='color:{LIGHT_GREY}; font-size:16px; margin-top:6px;'>{team_owner} | {team_record}</div>
  </div>
  <div style='margin-top:16px;'>
    <div>{pos_labels_html}</div>
    <div style='margin-top:6px;'>{pos_counts_html}</div>
  </div>
</div>
"""

# === TOP PERFORMERS (by Points Avg) ===
# Ensure numeric & safe ranking
team_df["Points (Avg)"] = pd.to_numeric(team_df["Points (Avg)"], errors="coerce")
team_df["Projected (Avg)"] = pd.to_numeric(team_df["Projected (Avg)"], errors="coerce")

top_performers = team_df.dropna(subset=["Points (Avg)"]).nlargest(2, "Points (Avg)")

# === BIGGEST UNDERACHIEVERS ===

team_df = team_df.copy()

# Compute safely — avoid division by zero
team_df["Performance"] = team_df.apply(
    lambda row: (
        (row["Points (Avg)"] - row["Projected (Avg)"]) / row["Points (Avg)"]
        if row["Points (Avg)"] != 0
        else None
    ),
    axis=1
)

# Convert to numeric so nsmallest() works
team_df["Performance"] = pd.to_numeric(team_df["Performance"], errors="coerce")

# Select the bottom 2 valid performers
underachievers = team_df.dropna(subset=["Performance"]).nsmallest(2, "Performance")

# === Helper: build player card ===
def build_player_card(row, metric_text):
    pos_value = row.get("Position", "")
    player_id = row.get("Player ID", None)
    team_abbrev_nfl = row.get("NFL Team", "")

    # Headshot: use team logo if D/ST, else player headshot
    if pos_value == "D/ST":
        headshot = nfl_logo_map.get(team_abbrev_nfl, "https://a.espncdn.com/i/headshots/nophoto.png")
    elif pd.notna(player_id):
        headshot = f"https://a.espncdn.com/i/headshots/nfl/players/full/{int(player_id)}.png"
    else:
        headshot = "https://a.espncdn.com/i/headshots/nophoto.png"

    # NFL team logo
    team_logo = nfl_logo_map.get(team_abbrev_nfl, "https://a.espncdn.com/i/teamlogos/nfl/500/default.png")

    player_name = row.get("Player", "")
    pos = row.get("Position", "")

    return (
        f"<div style='display:flex;align-items:center;margin-bottom:10px;'>"
        f"  <img src='{headshot}' style='width:50px;height:45px;border-radius:4px;margin-right:10px;'>"
        f"  <div>"
        f"    <div style='font-size:16px;color:{TEXT_COLOR};font-weight:600;'>"
        f"      {player_name}"
        f"      <img src='{team_logo}' style='width:20px;height:20px;vertical-align:middle;margin-left:4px;'>"
        f"      <span style='color:{LIGHT_GREY};margin-left:4px; font-size:0.9em;'>{pos}</span>"
        f"    </div>"
        f"    <div style='font-size:14px;color:{LIGHT_GREY};'>{metric_text}</div>"
        f"  </div>"
        f"</div>"
    )

# === Build performer cards ===
top_html = "".join(
    build_player_card(row, f"{row['Points (Avg)']:.1f} PPG")
    for _, row in top_performers.iterrows()
)

under_html = "".join(
    build_player_card(row, f"{row['Performance']*100:.1f}% Below Avg. Proj.")
    for _, row in underachievers.iterrows()
)

# === RIGHT PANEL (two columns) ===
right_panel_inner = (
    f"<div style='display:flex;'>"
    f"  <div style='flex:1; padding-right:4px;'>"
    f"    <div style='color:{LIGHT_GREY}; font-family:Oswald,sans-serif; font-size:16px; margin-bottom:8px;'>TOP PERFORMERS</div>"
    f"    {top_html}"
    f"  </div>"
    f"  <div style='width:1px; background-color:{LIGHT_GREY}; opacity:0.5; margin:0 8px;'></div>"
    f"  <div style='flex:1; padding-left:4px;'>"
    f"    <div style='color:{LIGHT_GREY}; font-family:Oswald,sans-serif; font-size:16px; margin-bottom:8px;'>BIGGEST UNDERACHIEVERS</div>"
    f"    {under_html}"
    f"  </div>"
    f"</div>"
)

# === TOP BAND: left + right, side-by-side ===
top_band_html = (
    f"<div style='display:flex; gap:0px; margin:0px;'>"
    f"  <div style='flex:1.8; background-color:{CARD_BG}; border-radius:0px; padding:12px;'>{left_panel_inner}</div>"
    f"  <div style='flex:2.2; background-color:{CARD_BG}; border-radius:0px; padding:12px;'>{right_panel_inner}</div>"
    f"</div>"
)

# === DISPLAY TOP BAND ONCE ===
st.markdown(top_band_html, unsafe_allow_html=True)

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
            f"<th style='padding:4px; border-bottom:1px solid #444; border-left: none; border-right: none;"
            f"background-color:{ROW_ALT}; font-family: Oswald, sans-serif; font-weight:175; text-align:left;'></th>"
        )

    elif col == "Player":
        # Left-align Player header
        header_label = header_map.get(col, col)
        table_html += (
            f"<th style='padding:4px; border-bottom:1px solid #444; border-left: none; border-right: none;"
            f"font-family: Oswald, sans-serif; font-weight:175; text-align:left;"
            f"background-color:{ROW_ALT};'>{header_label}</th>"
        )

    else:
        header_label = header_map.get(col, col)
        table_html += (
            f"<th style='padding:4px; border-bottom:1px solid #444; border-left: none; border-right: none;"
            f"font-family: Oswald, sans-serif; font-weight: 175; "
            f"background-color:{ROW_ALT};'>{header_label}</th>"
        )
table_html += "</tr></thead><tbody>"

# --- Define Acquisition Type colors ---
acq_colors = {
    "DRAFT": ESPN_BLUE,
    "ADD": ESPN_GREEN,
    "TRADE": "#F2C94C"  # yellow that complements ESPN blue/green
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

            table_html += f"<td style='padding:6px; {style}'>{cell_html}</td>"

        elif col == "Acquisition Type":
            # Apply color mapping
            color = acq_colors.get(row[col], TEXT_COLOR)
            table_html += f"<td style='padding:6px; {style}; color:{color}; font-weight:400; font-size: 0.9em;'>{row['Acquisition Type']}</td>"

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
                headshot_html = f"<img src='{headshot_url}' style='height:36px; border-radius:4px;'>"
            else:
                headshot_html = ""

            table_html += f"<td style='padding:6px; text-align:center; border:none;'>{headshot_html}</td>"

        elif col == "Slot":
            slot_value = row["Slot"]
            pill_html = (
                f"<span style='border: 1px solid {ESPN_BLUE}; "
                f"color:{ESPN_BLUE}; "
                f"padding:2px 16px; "
                f"border-radius:12px; "
                f"font-family: Oswald, sans-serif; "
                f"font-size:0.85em; "
                f"white-space:nowrap;'>{slot_value}</span>"
            )
            table_html += f"<td style='padding:6px; border:none; text-align:center;'>{pill_html}</td>"
        
        else:
            cell_value = row[col]
            # Round numeric values to 1 decimal
            if isinstance(cell_value, numbers.Number):
                cell_value = round(cell_value, 1)
            table_html += f"<td style='padding:6px; color: {LIGHT_GREY}; {style}'>{cell_value}</td>"

    table_html += "</tr>"

table_html += "</tbody></table>"

# --- DISPLAY TABLE ---
st.markdown(table_html, unsafe_allow_html=True)
