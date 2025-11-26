# 4_Matchups.py
import streamlit as st
import pandas as pd
import numbers
from utils import render_season_filter, load_and_filter_csv

# Show the global filter
season = render_season_filter()


# Define theme colors for consistency
DARK_BG = "#121212"
CARD_BG = "#202124"
ROW_ALT = "#1A1A1A"
TEXT_COLOR = "#FFFFFF"
LIGHT_GREY = "#A9A9A9"
GREY = "#4C4C4C"
RED = "#FF0000"
ESPN_BLUE = "#3F8EF3"
ESPN_GREEN = "#00FF66"  # ESPN green for active page border
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
    "GB": "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png",
    "HOU": "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png",
    "IND": "https://a.espncdn.com/i/teamlogos/nfl/500/ind.png",
    "JAX": "https://a.espncdn.com/i/teamlogos/nfl/500/jax.png",
    "KC": "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png",
    "LV": "https://a.espncdn.com/i/teamlogos/nfl/500/lv.png",
    "LAC": "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png",
    "LAR": "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png",
    "MIA": "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png",
    "MIN": "https://a.espncdn.com/i/teamlogos/nfl/500/min.png",
    "NE": "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png",
    "NO": "https://a.espncdn.com/i/teamlogos/nfl/500/no.png",
    "NYG": "https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png",
    "NYJ": "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png",
    "PHI": "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png",
    "PIT": "https://a.espncdn.com/i/teamlogos/nfl/500/pit.png",
    "SF": "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png",
    "SEA": "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png",
    "TB": "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png",
    "TEN": "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png",
    "WSH": "https://a.espncdn.com/i/teamlogos/nfl/500/wsh.png",
}

# === PAGE CONFIG ===
st.set_page_config(page_title="Matchups", layout="wide")
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
    Matchups
</h1>

""", unsafe_allow_html=True)

# Access the global season from session_state
season = st.session_state.get("season", 2024)

# === LOAD DATA ===
def load_data():
    df = load_and_filter_csv("weekly_matchups.csv", season)  # replace with your actual file

    # Create Record field
    df["Record"] = df["Wins"].astype(str) + "-" + df["Losses"].astype(str)

    # Build Headshot URL dynamically
    def build_headshot(row):
        if row["Position"] == "D/ST":
            # For defenses, use team logo from nfl_logo_map
            return nfl_logo_map.get(row["NFL Team"], "")
        else:
            # For players, use ESPN headshot
            return f"https://a.espncdn.com/i/headshots/nfl/players/full/{int(row['Player ID'])}.png"

    df["Headshot"] = df.apply(build_headshot, axis=1)

    return df

df = load_data()


# --- WEEK PICKER SEGMENTED CONTROL ---
weeks = sorted(df["Week"].unique())
week_labels = [f"Wk {w}" for w in weeks]

# Initialize session_state only once
if "selected_week" not in st.session_state:
    st.session_state.selected_week = weeks[0]

# Inject CSS to style the segmented control
st.markdown(f"""
<style>
/* Segmented control container */
div[data-testid="stSegmentedControl"] button {{
    background-color: {CARD_BG};
    color: {LIGHT_GREY} !important;
    border: 1px solid #444;
    border-radius: 8px;
    margin: 0 2px;
    padding: 0.4rem 0.8rem;
    font-family: 'Oswald', sans-serif;
    font-weight: 500;
    font-size: 16px;
}}

/* Selected button */
div[data-testid="stSegmentedControl"] button[aria-pressed="true"] {{
    background-color: {ESPN_BLUE} !important;
    color: white;
    border: 1px solid {ESPN_BLUE};
}}

/* Hover effect for inactive buttons */
div[data-testid="stSegmentedControl"] button:hover {{
    border-color: {ESPN_BLUE};
}}
</style>
""", unsafe_allow_html=True)

# --- Week labels as plain numbers ---
week_labels = [str(w) for w in sorted(df['Week'].unique())]

# --- Render segmented control centered ---
col1, col2, col3 = st.columns([.5, 4, .5])
with col2:
    selected_label = st.segmented_control(
        "NFL Week",  # no label
        options=week_labels,
        default=str(st.session_state.selected_week),  # just the number
        selection_mode="single",
    )

# Sync session_state
st.session_state.selected_week = int(selected_label)

# Clear old matchup if user manually changes week
if "selected_matchup" in st.session_state:
    if df[df["MatchupID"] == st.session_state.selected_matchup]["Week"].iloc[0] != st.session_state.selected_week:
        st.session_state.pop("selected_matchup")

# Filter DataFrame using the current selection
week_df = df[df["Week"] == st.session_state.selected_week]



# === MATCHUP FILTER SORTED BY TEAM SCORE ===
# Compute total score per matchup
matchup_scores = (
    week_df.groupby("MatchupID")["Team Score"]
    .sum()
    .sort_values(ascending=False)  # highest scoring matchup first
)

# Build labels in that order
matchup_labels = {}
for matchup_id in matchup_scores.index:
    matchup_df_temp = week_df[week_df["MatchupID"] == matchup_id]
    teams_temp = matchup_df_temp["Abbrev"].unique()
    if len(teams_temp) == 2:
        matchup_labels[matchup_id] = f"{teams_temp[0]} vs. {teams_temp[1]}"
    else:
        matchup_labels[matchup_id] = f"Matchup {matchup_id}"

# Before the selectbox
st.markdown('<div class="matchup-filter-marker"></div>', unsafe_allow_html=True)


# --- PICK MATCHUP ---
week_matchups = df[df["Week"] == st.session_state.selected_week]["MatchupID"].unique()

# Build labels for this week's matchups
week_matchup_labels = {mid: matchup_labels[mid] for mid in week_matchups}

# Decide default matchup
default_matchup = (
    st.session_state.selected_matchup
    if "selected_matchup" in st.session_state and st.session_state.selected_matchup in week_matchups
    else week_matchups[0]
)

# --- MATCHUP FILTER (in sidebar) ---
with st.sidebar:
    selected_matchup = st.selectbox(
        "Matchup",  # You can keep or hide this label
        options=list(week_matchup_labels.keys()),
        format_func=lambda mid: week_matchup_labels[mid],
        index=list(week_matchup_labels.keys()).index(default_matchup),
        key="matchup_selectbox",
        label_visibility="visible",  # hides label for clean look
    )

# Sync session_state
st.session_state.selected_matchup = selected_matchup


# === SPLIT TEAMS ===
matchup_df = week_df[week_df["MatchupID"] == selected_matchup]
teams = matchup_df["Abbrev"].unique()
if len(teams) != 2:
    st.error("Expected exactly 2 teams per matchup.")
    st.stop()

team1_df = matchup_df[matchup_df["Abbrev"] == teams[0]].copy()
team2_df = matchup_df[matchup_df["Abbrev"] == teams[1]].copy()



# === SLOT ORDER ===
slot_order = {
    "QB": 1, "RB": 2, "WR": 3, "TE": 4, "FLEX": 5,
    "D/ST": 6, "K": 7, "BE": 8, "IR": 9
}
team1_df["SlotOrder"] = team1_df["Slot"].map(slot_order)
team2_df["SlotOrder"] = team2_df["Slot"].map(slot_order)

team1_df = team1_df.sort_values("SlotOrder").reset_index(drop=True)
team2_df = team2_df.sort_values("SlotOrder").reset_index(drop=True)

# Pad shorter team so both align
max_len = max(len(team1_df), len(team2_df))
team1_df = team1_df.reindex(range(max_len))
team2_df = team2_df.reindex(range(max_len))


# === TEAM HEADERS ===
def render_team_header(team_df: pd.DataFrame, col, score_on_right: bool = True):
    """Render header with Abbrev (Oswald), Owner | Record (LIGHT_GREY),
    and Score/Projected on the opposite side (right for Team1, left for Team2)."""
    abbrev = team_df['Abbrev'].iloc[0]
    owner = team_df['Owner'].iloc[0]
    record = team_df['Record'].iloc[0]
    score = team_df['Team Score'].iloc[0]
    proj  = team_df['Team Projected'].iloc[0]
    rank  = team_df['Weekly Score Rank'].iloc[0]

    # Alignment settings
    text_align = "left" if score_on_right else "right"
    score_align = "right" if score_on_right else "left"

    text_block = f"""
        <div style="line-height:1.3; text-align:{text_align};">
            <div style="margin:2px 0; font-family:Oswald, sans-serif; font-size:26px; font-weight:600; color:{TEXT_COLOR};">
                {abbrev}
            </div>
            <div style="margin:6px 0; font-size:17px; color:{LIGHT_GREY};">
                {owner} | {record}
            </div>
            <div style="margin:6px 0; font-size:17px; color:{ESPN_BLUE};">
                Weekly Score Rank: {float(rank):.0f}
            </div>
        </div>
    """

    score_block = f"""
        <div style="line-height:1.3; text-align:{score_align}; min-width:96px;">
            <div style="margin:2px 0; font-family:Oswald, sans-serif; font-size:40px; font-weight:600; color:{TEXT_COLOR};">
                {float(score):.1f}
            </div>
            <div style="margin:2px 0; font-family:Oswald, sans-serif; font-size:20px; color:{LIGHT_GREY};">
                {float(proj):.1f}
            </div>
        </div>
    """

    # Horizontal layout: text | score  (left team)  OR  score | text (right team)
    content = f"{text_block}{score_block}" if score_on_right else f"{score_block}{text_block}"

    # Wrap in card-style container
    col.markdown(f"""
        <div style="
            background-color:{ROW_ALT};
            border-radius:0px;
            padding:12px;
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:0px;
            border-top: 1px solid {GREY};
            border-bottom: 1px solid {GREY};
        ">
            {content}
        </div>
    """, unsafe_allow_html=True)

# Use your existing columns
left, mid, right = st.columns([4,.3,4])

with left:
    render_team_header(team1_df, col=st, score_on_right=True)

with right:
    render_team_header(team2_df, col=st, score_on_right=False)



# === PLAYER ROWS SECTION ===

# Determine max number of rows for the matchup
max_len = max(len(team1_df), len(team2_df))

# === PLAYER ROWS SECTION ===
for i in range(max_len):
    p1 = team1_df.iloc[i] if i < len(team1_df) else None
    p2 = team2_df.iloc[i] if i < len(team2_df) else None

    left, mid, right = st.columns([4, 0.3, 4], gap="small")

    # TEAM 1 PLAYER
    with left:
        if pd.notna(p1["Player"]):
            # --- Set color for Pro Pos Rank ---
            try:
                rank = int(p1["Pro Pos Rank"])
            except (ValueError, TypeError):
                rank = None

            if rank is not None:
                if rank >= 20:
                    rank_color = GREEN_DARK
                elif rank <= 10:
                    rank_color = RED
                else:
                    rank_color = LIGHT_GREY
            else:
                rank_color = TEXT_COLOR

            # --- Set background color based on Slot ---
            if p1["Slot"] == "IR":
                bg_color = "rgba(255, 0, 0, 0.1)"  # light transparent red
            elif p1["Slot"] in ["BE"]:
                bg_color = CARD_BG
            else:
                bg_color = ROW_ALT
            # --- Clean display value for Pro Pos Rank (TEAM 1) ---
            if p1["Pro Opponent"] == "BYE" or pd.isna(p1["Pro Pos Rank"]):
                pro_rank_display_1 = ""
            else:
                try:
                    pro_rank_display_1 = str(int(p1["Pro Pos Rank"]))
                except:
                    pro_rank_display_1 = ""

            st.markdown(
                f"""
                <div style='background-color:{bg_color}; border-radius:0px; padding:14px; display:flex; align-items:center; height:75px; margin-bottom:3px;'>
                    <div style='flex:1; display:flex; align-items:center; gap:8px;'>
                        <img src='{p1['Headshot']}' width='70' style='border-radius:30%;'>
                        <div>
                            <div style='font-size:18px;'>{p1['Player']}
                                <img src='{nfl_logo_map.get(p1['NFL Team'], '')}' style='width:24px;height:24px;vertical-align:middle;margin-left:4px; margin-right:4px;'>
                                <span style='font-size:14px; color:{LIGHT_GREY}'>{p1['Position']}</span>
                            </div>
                            <div style='font-size:14px;'>
                                <span style='color:{rank_color}'>{p1['Pro Opponent']}</span> 
                                <span style='font-size:13px; color:{rank_color}'>{pro_rank_display_1}</span>
                            </div>
                        </div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='font-family:Oswald, sans-serif; font-size:22px; font-weight:500; color:{TEXT_COLOR}'>{p1['Points']}</div>
                        <div style='font-family:Oswald, sans-serif; font-size:14px; color:{LIGHT_GREY}'>{p1['Projected']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # --- SLOT COLUMN ---
    with mid:
        slot_val = ""
        if p1 is not None and pd.notna(p1["Slot"]):
            slot_val = p1["Slot"]
        elif p2 is not None and pd.notna(p2["Slot"]):
            slot_val = p2["Slot"]

        st.markdown(
            f"""
            <div style='background-color:{DARK_BG};
                        color:{LIGHT_GREY};
                        height:70px;
                        width:100%;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-family:Oswald, sans-serif;
                        font-size:18px;
                        margin-bottom:2px;'>
                {slot_val}
            </div>
            """,
            unsafe_allow_html=True
        )



    # TEAM 2 PLAYER
    with right:
        if pd.notna(p2["Player"]):
            # --- Set color for Pro Pos Rank ---
            try:
                rank = int(p2["Pro Pos Rank"])
            except (ValueError, TypeError):
                rank = None

            if rank is not None:
                if rank >= 20:
                    rank_color = GREEN_DARK
                elif rank <= 10:
                    rank_color = RED
                else:
                    rank_color = LIGHT_GREY
            else:
                rank_color = TEXT_COLOR

            # --- Set background color based on Slot ---
            if p2["Slot"] == "IR":
                bg_color = "rgba(255, 0, 0, 0.1)"  # light transparent red
            elif p2["Slot"] in ["BE"]:
                bg_color = CARD_BG
            else:
                bg_color = ROW_ALT
            # --- Clean display value for Pro Pos Rank (TEAM 2) ---
            if p2["Pro Opponent"] == "BYE" or pd.isna(p2["Pro Pos Rank"]):
                pro_rank_display_2 = ""
            else:
                try:
                    pro_rank_display_2 = str(int(p2["Pro Pos Rank"]))
                except:
                    pro_rank_display_2 = ""
            st.markdown(
                f"""
                <div style='background-color:{bg_color}; border-radius:0px; padding:14px; display:flex; align-items:center; height:75px; margin-bottom:3px;'>
                    <div style='text-align:left;'>
                        <div style='font-family:Oswald, sans-serif; font-size:22px; font-weight:500; color:{TEXT_COLOR}'>{p2['Points']}</div>
                        <div style='font-family:Oswald, sans-serif; font-size:14px; color:{LIGHT_GREY}'>{p2['Projected']}</div>
                    </div>
                    <div style='flex:1; display:flex; align-items:center; gap:8px; justify-content:flex-end;'>
                        <div style='text-align:right;'>
                            <div style='font-size:18px;'>
                                {p2['Player']} 
                                <img src='{nfl_logo_map.get(p2['NFL Team'], '')}' 
                                    style='width:24px;height:24px;vertical-align:middle;margin-left:4px; margin-right:4px;'>
                                <span style='font-size:14px; color:{LIGHT_GREY}'>{p2['Position']}</span>
                            </div>
                            <div style='font-size:14px;'>
                                <span style='color:{rank_color}'>{p2['Pro Opponent']}</span>
                                <span style='font-size:13px; color:{rank_color}'>{pro_rank_display_2}</span>
                            </div>
                        </div>
                        <img src='{p2['Headshot']}' width='70' style='border-radius:30%;'>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

