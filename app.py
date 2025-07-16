import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

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

# --- Evaluation Logic ---
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
st.title("⚽ La Liga Predictions Ranking App")
st.write("Upload your predictions and see how close you are to the real standings.")

uploaded_file = st.file_uploader("Upload your predictions.csv", type="csv")

if uploaded_file:
    predictions_df = pd.read_csv(uploaded_file)

    st.subheader("📥 Your Predictions")
    st.dataframe(predictions_df)

    st.subheader("📡 Fetching Actual La Liga Standings...")
    actual_df = fetch_actual_standings()
    st.dataframe(actual_df)

    st.subheader("🏁 Evaluation Results")
    summary_df, detailed_df = evaluate_predictions(predictions_df, actual_df)
    st.dataframe(summary_df.sort_values("exact_rank"))

    st.subheader("🔎 Detailed Comparison")
    st.dataframe(detailed_df.sort_values(["name", "actual_position"]))

    # Optional: Downloads
    st.download_button("📤 Download Summary CSV", summary_df.to_csv(index=False, encoding="utf-8-sig"), file_name="ranking_summary.csv")
    st.download_button("📤 Download Detailed CSV", detailed_df.to_csv(index=False, encoding="utf-8-sig"), file_name="detailed_results.csv")
