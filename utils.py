# utils.py
import streamlit as st
import pandas as pd

def render_season_filter() -> int:
    """Render a global Season filter in the sidebar and persist selection."""
    if "season" not in st.session_state:
        st.session_state["season"] = 2025  # default

    season = st.sidebar.selectbox(
        "Season",
        [2024, 2025],  # or dynamically load from data
        index=[2024, 2025].index(st.session_state["season"])
    )

    st.session_state["season"] = season
    return season


def load_and_filter_csv(path: str, season: int) -> pd.DataFrame:
    """Load a CSV and filter by Season if column exists."""
    df = pd.read_csv(path)
    if "Season" in df.columns:
        df = df[df["Season"] == season]
    return df
