# pages/3_Scoreboard.py

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

# === PAGE CONFIG ===
st.set_page_config(layout="centered")

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

# --- CUSTOM CSS STYLING ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&display=swap');
            
            
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

/* Ensure paragraphs inside our cards have no default spacing */
.matchup-card p {{ margin: 0 !important; padding: 0 !important; }}

/* Team abbreviation -- make bigger and uppercase */
.team-name {{
    color: {TEXT_COLOR};
    font-size: 40px !important;
    font-weight: 500 !important;
    font-family: 'Oswald', sans-serif !important;
    margin: 0 !important;
    line-height: 1.3 !important;
    text-transform: uppercase !important;
}}

/* Owner / record / rank lines */
.owner-info {{
    color: {LIGHT_GREY};
    font-size: 18px;
    margin: 0 !important;
    line-height: 1.32; /* slightly looser so lines don't collide */
}}

/* Score Rank */
.score-rank-info {{
    color: {ESPN_BLUE};
    font-size: 18px;
    margin: 0 !important;
    line-height: 1.32; /* slightly looser so lines don't collide */
}}

/* Prominent team score (right column) */
.team-score {{
    color: {TEXT_COLOR};
    font-size: 40px !important;
    font-weight: 500 !important;
    font-family: 'Oswald', sans-serif !important;
    margin: 0 !important;
    line-height: 1.3 !important;
    text-align: center !important;
}}

/* Projected score text (right column) */
.projected-info {{
    color: {LIGHT_GREY};
    font-size: 18px !important;
    font-family: 'Oswald', sans-serif !important;
    margin: 0 !important;
    line-height: 1.3 !important;
    text-align: center !important;
}}

/* Card that wraps a matchup (both teams) */
.matchup-card {{
    background-color: {CARD_BG};
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 4px;
    border: 1px solid rgba(255,255,255,0.04);
    box-sizing: border-box;
}}

/* Inner layout for a single team row (left + right) */
.matchup-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;   /* vertical center alignment */
    min-height: 62px;      /* keeps left/right vertically aligned */
    gap: 12px;
}}

/* 1st column stacks team name / owner / rank */
.team-left {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 4px;
}}

/* 2nd column stacks projected above score and right-aligns */
.team-right {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-right: 2px solid rgba(255,255,255,0.04);  /* vertical separator */
    padding-right: 36px;  
    margin-right: 0px;
    min-width: 120px; /* consistent width so numbers align across cards */
    gap: 8px; /* increase to add vertical spacing */
}}

/* thin separator between teams inside the same card */
hr.matchup-sep {{
    border: none;
    border-top: 2px solid rgba(255,255,255,0.04);
    margin: 10px 0;
}}

/* Third column for top performer */
.team-top {{
    display: flex;
    flex-direction: column;  /* stack header + player card vertically */
    justify-content: flex-start; /* align to top */
    align-items: flex-start;    /* align everything to the left */
    width: 160px;           /* adjust as needed */
    text-align: left;
    margin-left: -24px; /* pull column 20px to the left */
}}

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
    Scoreboard
</h1>

""", unsafe_allow_html=True)

# Access the global season from session_state
season = st.session_state.get("season", 2024)

# Load data
try:
    df = load_and_filter_csv("weekly_matchups.csv", season)
except FileNotFoundError:
    st.error("weekly_matchups.csv not found. Please check the file path.")
    st.stop()

selected_season = st.session_state.get("selected_season", 2024)

# Filter your dataframe
df_filtered = df[df["Season"] == selected_season]

# === Helper: build player card ===
def build_player_card(row, metric_text):
    pos_value = row.get("Position", "")
    player_id = row.get("Player ID", None)
    team_abbrev_nfl = row.get("NFL Team", "")
    slot = row.get("Slot", "")

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

    # Append "on bench" if Slot == "BE"
    if slot == "BE":
        metric_text = f"{metric_text} (on bench)"

    return (
        f"<div style='display:flex;flex-direction:column;'>"
        f"  <div style='color:{LIGHT_GREY}; font-family:Oswald,sans-serif; font-size:16px; margin-bottom:8px;'>TOP PERFORMER</div>"
        f"  <div style='display:flex;align-items:center;'>"
        f"    <img src='{headshot}' style='width:50px;height:45px;border-radius:4px;margin-right:10px;'>"
        f"    <div>"
        f"      <div style='font-size:16px;color:{TEXT_COLOR};font-weight:600;'>"
        f"        {player_name}"
        f"        <img src='{team_logo}' style='width:20px;height:20px;vertical-align:middle;margin-left:4px;'>"
        f"        <span style='color:{LIGHT_GREY};margin-left:4px; font-size:0.9em;'>{pos}</span>"
        f"      </div>"
        f"      <div style='font-size:14px;color:{LIGHT_GREY};'>{metric_text}</div>"
        f"    </div>"
        f"  </div>"
        f"</div>"
    )

# --- HEADER & WEEK FILTER (in sidebar) ---
with st.sidebar:
    selected_week = st.selectbox(
        "Week",  # Label (will use default Streamlit styling)
        sorted(df['Week'].unique()),
        key="week_selector",
        format_func=lambda x: f"NFL Week {x}"
    )

# Filter data for selected week
week_df = df[df["Week"] == selected_week].copy()

# --- MAIN DISPLAY (RENDER MATCHUPS WITH 3 COLUMNS, INCLUDING TOP PERFORMER) ---
unique_matchup_ids = week_df["MatchupID"].unique()

def fmt_num(x):
    try:
        return f"{float(x):.2f}"
    except Exception:
        return "" if pd.isna(x) else str(x)
    
# --- Compute sorting metric per matchup ---
# Sort by sum of Team Score + Points Against for both teams
matchup_metrics = week_df.groupby("MatchupID").apply(
    lambda df: pd.Series({
        "sort_metric": df["Team Score"].sum() + df["Points Against"].sum()
    })
).reset_index()

# Sorted list of MatchupIDs
sorted_matchup_ids = matchup_metrics.sort_values("sort_metric", ascending=False)["MatchupID"].tolist()

for matchup_id in sorted_matchup_ids:
    matchup_df = week_df[week_df["MatchupID"] == matchup_id]

    teams = []
    for abbrev in matchup_df["Abbrev"].unique():
        team_df = matchup_df[matchup_df["Abbrev"] == abbrev]
        row = team_df.iloc[0]

        team_score = fmt_num(row.get("Team Score", ""))
        team_proj = fmt_num(row.get("Team Projected", ""))
        owner = row["Owner"]
        wins = int(row["Wins"])
        losses = int(row["Losses"])
        score_rank = row["Weekly Score Rank"]

        # --- find top performer row ---
        top_player_row = team_df.loc[team_df["Points"].astype(float).idxmax()]

        teams.append({
            "Abbrev": abbrev,
            "Owner": owner,
            "Wins": wins,
            "Losses": losses,
            "ScoreRank": score_rank,
            "Score": team_score,
            "Proj": team_proj,
            "TopRow": top_player_row  # keep the full row for rendering
        })

    if len(teams) != 2:
        continue

    team1, team2 = teams

    # Build player cards
    team1_card = build_player_card(team1["TopRow"], f"{fmt_num(team1['TopRow']['Points'])} Pts")
    team2_card = build_player_card(team2["TopRow"], f"{fmt_num(team2['TopRow']['Points'])} Pts")

    # --- render container ---
    st.markdown(f"""
    <div class="matchup-card">

      <!-- Team 1 -->
      <div class="matchup-row">
        <div class="team-left">
          <p class="team-name">{team1['Abbrev']}</p>
          <p class="owner-info">{team1['Owner']}  |  {team1['Wins']}-{team1['Losses']}</p>
          <p class="score-rank-info">Weekly Score Rank: {team1['ScoreRank']}</p>
        </div>
        <div class="team-right">
          <p class="team-score">{team1['Score']}</p>
          <p class="projected-info">{team1['Proj']}</p>
        </div>
        <div class="team-top" style="width:240px; text-align:left;">
          {team1_card}
        </div>
      </div>

      <hr class="matchup-sep" />

      <!-- Team 2 -->
      <div class="matchup-row">
        <div class="team-left">
          <p class="team-name">{team2['Abbrev']}</p>
          <p class="owner-info">{team2['Owner']}  |  {team2['Wins']}-{team2['Losses']}</p>
          <p class="score-rank-info">Weekly Score Rank: {team2['ScoreRank']}</p>
        </div>
        <div class="team-right">
          <p class="team-score">{team2['Score']}</p>
          <p class="projected-info">{team2['Proj']}</p>
        </div>
        <div class="team-top" style="width:240px; text-align:left;">
          {team2_card}
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)

    # --- Add Boxscore link styled like ESPN ---
    cols = st.columns([4, .75])  # left empty, right holds the button
    with cols[1]:
        if st.button("View Matchup", key=f"box_{matchup_id}"):
            st.session_state.selected_matchup = matchup_id
            st.session_state.selected_week = selected_week
            st.switch_page("pages/4_Matchups.py")

st.markdown(f"""
<style>
div[data-testid="stButton"] button {{
    background: none;
    border: none;
    color: {ESPN_BLUE};
    font-family: 'Oswald', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500;
    text-decoration: underline;
    text-align: right !important;
    padding: 0;
    cursor: pointer;
}}
div[data-testid="stButton"] button:hover {{
    color: white;
}}
</style>
""", unsafe_allow_html=True)

