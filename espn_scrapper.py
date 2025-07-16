import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_current_standings():
    url = "https://www.espn.com/soccer/standings/_/league/ESP.2"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    tables = soup.find_all("table")
    if not tables:
        raise ValueError("❌ No tables found in the page. Site might be blocking or structure changed.")

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


def normalize_team_names(df, name_map):
    df["team"] = df["team"].replace(name_map)
    return df


def evaluate_predictions(pred_file, real_df):
    preds = pd.read_csv(pred_file)

    # Merge predictions with real standings
    merged = preds.merge(real_df, on="team", how="left")

    # Exact matches
    merged["exact_match"] = merged["predicted_position"] == merged["actual_position"]

    # Absolute error
    merged["abs_error"] = abs(merged["predicted_position"] - merged["actual_position"])

    # Summary by person
    summary = merged.groupby("name").agg({
        "exact_match": "sum",
        "abs_error": "sum"
    }).reset_index()

    summary["exact_rank"] = summary["exact_match"].rank(ascending=False, method="min")
    summary["approx_rank"] = summary["abs_error"].rank(ascending=True, method="min")

    return summary, merged


if __name__ == "__main__":
    # Optional: mapping for team name consistency
    team_name_map = {
        "2Real Sociedad II": "Real Sociedad B",
        "Real Betis": "Betis",
        "Atlético Madrid": "Atletico Madrid",
        "Rayo Vallecano": "Rayo",
        "Cádiz": "Cadiz",
        "Alavés": "Alaves",
        "Mallorca": "RCD Mallorca"
        # Add more mappings if needed
    }

    try:
        real_standings = fetch_current_standings()
        print("✅ Standings fetched successfully.")
    except Exception as e:
        print("❌ Error fetching standings:", e)
        exit(1)

    # Normalize team names
    real_standings = normalize_team_names(real_standings, team_name_map)

    real_standings.to_csv("actual_standings.csv", index=False, encoding="utf-8-sig")

    # Predictions CSV must contain: name, team, predicted_position
    summary_df, detailed_df = evaluate_predictions("predictions.csv", real_standings)

    summary_df.to_csv("ranking_summary.csv", index=False)
    detailed_df.to_csv("detailed_results.csv", index=False)

    print("\n🏆 Ranking Summary:")
    print(summary_df.sort_values("exact_rank"))
