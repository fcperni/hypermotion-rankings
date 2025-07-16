import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

team_name_map = {
    "2Real Sociedad II": "Real Sociedad B"
    # Add more mappings if needed
}

def normalize_team_names(df, name_map):
    df["team"] = df["team"].replace(name_map)
    return df

# --- Scrape actual standings from ESPN ---
@st.cache_data
def fetch_actual_standings():
    url = "https://www.espn.com/soccer/standings/_/league/ESP.2"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table")
    
    # Pick the first table that has "Team" in header
    target_table = None
    for table in tables:
        if "Valladolid" in table.text:
            target_table = table
            break

    if not target_table:
        raise ValueError("❌ Standings table not found on the ESPN page.")

    rows = target_table.find_all("tr")[1:]  # Skip header row
    teams = []
    suffix_index = 4
    for row in rows:
        if len(teams) == 9:
            suffix_index = suffix_index + 1
        teams.append(row.text[suffix_index:])

    df = pd.DataFrame({
        "team": teams,
        "actual_position": range(1, len(teams) + 1)
    })

    return df

def evaluate_predictions(preds_df, rankings_df):
    merged = preds_df.merge(rankings_df, on="team", how="left")
    merged["exact_match"] = merged["predicted_position"] == merged["actual_position"]
    merged["abs_error"] = abs(merged["predicted_position"] - merged["actual_position"])

    summary = merged.groupby("name").agg({
        "exact_match": "sum",
        "abs_error": "sum"
    }).reset_index()

    summary["exact_rank"] = summary["exact_match"].rank(ascending=False, method="min")
    summary["approx_rank"] = summary["abs_error"].rank(ascending=True, method="min")
    return summary, merged

# --- Streamlit UI ---
st.title("⚽ Predicciones de la Liga Hypermotion")
st.write("Sube tus predicciones para ver cómo de exactas han sido.")

uploaded_file = st.file_uploader("Sube tus predicciones.csv", type="csv")

if uploaded_file:
    predictions_df = pd.read_csv(uploaded_file)
    predictions_df = normalize_team_names(predictions_df, team_name_map)

    st.subheader("📥 Tus predicciones:")
    st.dataframe(predictions_df)

    st.subheader("📡 Obteniendo la clasificación de La Liga Hypermotion...")
    actual_standings_df = fetch_actual_standings()

    actual_standings_df = normalize_team_names(actual_standings_df, team_name_map)
    st.dataframe(actual_standings_df)

    st.subheader("🏁 Evaluación de Resultados")
    summary_df, detailed_df = evaluate_predictions(predictions_df, actual_standings_df)
    st.dataframe(summary_df.sort_values("exact_rank"))

    st.subheader("🔎 Comparativa Detallada")
    st.dataframe(detailed_df.sort_values(["name", "actual_position"]))