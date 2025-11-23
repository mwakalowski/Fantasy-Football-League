# app.py
import streamlit as st
import pandas as pd
from utils import render_season_filter

st.set_page_config(layout="wide")

# ✅ Show the global Season filter in the sidebar
season = render_season_filter()

# === THEME COLORS ===
DARK_BG = "#121212"
CARD_BG = "#202124"
ROW_ALT = "#1A1A1A"
TEXT_COLOR = "#FFFFFF"
LIGHT_GREY = "#A9A9A9"
ESPN_BLUE = "#3F8EF3"
ESPN_GREEN = "#00FF66"  # ESPN green for active page border
GOLD = "#FFD700"
SILVER = "#C0C0C0"
BRONZE = "#CD7F32"

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
    D3 Fantasy Football League
</h1>

""", unsafe_allow_html=True)

# --- LEAGUE WINNERS TABLE ---
data = [
    {"Season": 2024, "🥇": "Zac Edwards", "🥈": "Mike Wakalowski", "🥉": "Jon Harned", "Top Scorer": "Jon Harned"},
    {"Season": 2023, "🥇": "Mike Wakalowski", "🥈": "Dave Craig", "🥉": "Dave Reingold", "Top Scorer": "Jay Puglisi"},
]

df_winners = pd.DataFrame(data)

# --- BUILD CUSTOM HTML TABLE ---
rows_html = ""
for i, row in df_winners.iterrows():
    rows_html += (
        f"<tr style='background-color:{ROW_ALT}; color:{LIGHT_GREY};'>"
        f"<td style='padding:8px;'><span style='color:{ESPN_BLUE};'>{row['Season']}</span></td>"
        f"<td style='padding:8px;'>{row['🥇']}</td>"
        f"<td style='padding:8px;'>{row['🥈']}</td>"
        f"<td style='padding:8px;'>{row['🥉']}</td>"
        f"<td style='padding:8px;'>{row['Top Scorer']}</td>"
        f"</tr>"
    )

table_html = f"""
<div style='display:flex; justify-content:center; margin-top:20px;'>
<table style='background-color:{ROW_ALT}; border-collapse:collapse; width:80%; text-align:center; border:none;'>
    <thead style='background-color:{CARD_BG};'>
        <tr style='color:{TEXT_COLOR}; font-family:Oswald, sans-serif; text-transform:uppercase;'>
            <th style='padding:10px; border-bottom:1px solid #444;'>Season</th>
            <th style='padding:10px; border-bottom:1px solid #444; color:{GOLD};'>🥇 1st</th>
            <th style='padding:10px; border-bottom:1px solid #444; color:{SILVER};'>🥈 2nd</th>
            <th style='padding:10px; border-bottom:1px solid #444; color:{BRONZE};'>🥉 3rd</th>
            <th style='padding:10px; border-bottom:1px solid #444; color:{TEXT_COLOR};'>🔥 Top Scorer</th>
        </tr>
    </thead>
    <tbody>
        {rows_html}
    </tbody>
</table>
</div>
"""

st.markdown(table_html, unsafe_allow_html=True)
