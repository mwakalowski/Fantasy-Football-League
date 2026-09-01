# utils.py
import streamlit as st
import pandas as pd


def available_seasons(path: str = "team_weekly.csv") -> list[int]:
    """Return the sorted seasons present in the app's aggregated data."""
    season_data = pd.read_csv(path, usecols=["Season"])
    seasons = sorted(
        season_data["Season"].dropna().astype(int).unique().tolist()
    )
    if not seasons:
        raise ValueError(f"No seasons were found in {path}")
    return seasons


def render_season_filter() -> int:
    """Render the global Season filter and default to the latest season."""
    seasons = available_seasons()
    selected = st.session_state.get("season")
    if selected not in seasons:
        selected = seasons[-1]
        st.session_state["season"] = selected

    season = st.sidebar.selectbox(
        "Season",
        seasons,
        index=seasons.index(selected),
    )

    st.session_state["season"] = season
    return season


def load_and_filter_csv(path: str, season: int) -> pd.DataFrame:
    """Load a CSV and filter by Season if column exists."""
    df = pd.read_csv(path)
    if "Season" in df.columns:
        df = df[df["Season"] == season]
    return df
