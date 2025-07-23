import streamlit as st
import pandas as pd

import utils, scrapper, predictor

# --- Streamlit UI ---
st.title("⚽ Predicciones de la Liga Hypermotion")
st.write("Sube tus Predicciones para ver cómo de exactas han sido.")
st.session_state['language'] = 'es'

uploaded_file = st.file_uploader("Sube tus Predicciones.csv", type="csv")

if uploaded_file:
    predictions_df = pd.read_csv(uploaded_file)
    predictions_df = utils.normalize_team_names(predictions_df)

    st.subheader("📥 Predicciones")
    # st.dataframe(predictions_df.reset_index(drop=True).rename_axis("#").rename(lambda x: x + 1))
    pivoted_df = predictions_df.pivot(index="Predicción", columns="Nombre", values="Equipo")
    st.dataframe(pivoted_df.reset_index(drop=True).rename_axis("#").rename(lambda x: x + 1))

    st.subheader("📡 Clasificación de La Liga Hypermotion")
    actual_standings_df = scrapper.fetch_actual_standings()

    actual_standings_df = utils.normalize_team_names(actual_standings_df)
    st.dataframe(actual_standings_df.drop(columns=["Posición"]).reset_index(drop=True).rename_axis("Posición").rename(lambda x: x + 1))

    st.subheader("🏁 Evaluación de Resultados")
    summary_df, detailed_df = predictor.evaluate_predictions(predictions_df, actual_standings_df)
    st.dataframe(summary_df.sort_values("Ranking exacto").reset_index(drop=True).rename_axis("Posición").rename(lambda x: x + 1))

    st.subheader("🔎 Comparativa Detallada")
    st.dataframe(detailed_df.sort_values(["Nombre", "Posición"]).reset_index(drop=True).rename_axis("Posición"))