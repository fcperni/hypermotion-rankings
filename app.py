import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

team_name_map = {
    "2Real Sociedad II": "Real Sociedad B",
    "Andorra": "FC Andorra",
    "Almeria": "Almería",
    "Castellon": "Castellón",
    "Cadiz": "Cádiz",
    "Cordoba": "Córdoba",
    "Deportivo": "Deportivo La Coruña",
    "Leganes": "Leganés",
    "Mirandes": "Mirandés",
    "Malaga": "Málaga",
    "Zaragoza": "Real Zaragoza",
    "Valladolid": "Real Valladolid",
    "Sporting": "Sporting Gijón",
    "Sporting Gijon": "Sporting Gijón"
    # Add more mappings if needed
}

def normalize_team_names(df, name_map):
    df["Equipo"] = df["Equipo"].replace(name_map)
    return df

def transpose_df(df):
    transposed = df.set_index(df.columns[0]).T
    transposed.index.name = None  # optional: remove "name" of index
    return transposed.reset_index().rename(columns={"index": df.columns[0]})

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
        "Equipo": teams,
        "Posición": range(1, len(teams) + 1)
    })

    return df

def evaluate_predictions(preds_df, rankings_df):
    merged = preds_df.merge(rankings_df, on="Equipo", how="left")
    merged["Posiciones exactas"] = merged["Predicción"] == merged["Posición"]
    merged["Error absoluto"] = abs(merged["Predicción"] - merged["Posición"])

    summary = merged.groupby("Nombre").agg({
        "Posiciones exactas": "sum",
        "Error absoluto": "sum"
    }).reset_index()

    summary["Ranking exacto"] = summary["Posiciones exactas"].rank(ascending=False, method="min")
    summary["Ranking aproximaciones"] = summary["Error absoluto"].rank(ascending=True, method="min")
    return summary, merged

# --- Streamlit UI ---
st.title("⚽ Predicciones de la Liga Hypermotion")
st.write("Sube tus Predicciones para ver cómo de exactas han sido.")
st.session_state['language'] = 'es'

uploaded_file = st.file_uploader("Sube tus Predicciones.csv", type="csv")

if uploaded_file:
    predictions_df = pd.read_csv(uploaded_file)
    predictions_df = normalize_team_names(predictions_df, team_name_map)

    st.subheader("📥 Tus Predicciones:")
    # st.dataframe(predictions_df.reset_index(drop=True).rename_axis("#").rename(lambda x: x + 1))
    pivoted_df = predictions_df.pivot(index="Predicción", columns="Nombre", values="Equipo")
    st.dataframe(pivoted_df.reset_index(drop=True).rename_axis("#").rename(lambda x: x + 1))

    st.subheader("📡 Obteniendo la clasificación de La Liga Hypermotion...")
    actual_standings_df = fetch_actual_standings()

    actual_standings_df = normalize_team_names(actual_standings_df, team_name_map)
    st.dataframe(actual_standings_df.drop(columns=["Posición"]).reset_index(drop=True).rename_axis("Posición").rename(lambda x: x + 1))

    st.subheader("🏁 Evaluación de Resultados")
    summary_df, detailed_df = evaluate_predictions(predictions_df, actual_standings_df)
    st.dataframe(summary_df.sort_values("Ranking exacto").reset_index(drop=True).rename_axis("Posición").rename(lambda x: x + 1))

    st.subheader("🔎 Comparativa Detallada")
    st.dataframe(detailed_df.sort_values(["Nombre", "Posición"]))