import pandas as pd
import requests
from bs4 import BeautifulSoup

import utils


def fetch_actual_standings():
    url = "https://www.espn.com/soccer/standings/_/league/ESP.2"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table")

    # Pick the first table that has "Team" in the header
    target_table = None
    for table in tables:
        if "Valladolid" in table.text:
            target_table = table
            break

    if not target_table:
        raise ValueError("❌ Standings table not found on the ESPN page.")

    teams = []
    badges = []
    rows = target_table.find_all("tr")[1:]  # Skip header row
    suffix_index = 4
    for row in rows:
        if len(teams) == 9:
            suffix_index = suffix_index + 1
        team_name = row.text[suffix_index:]
        teams.append(team_name)
        badges.append(utils.team_logo_urls.get(team_name))

    df = pd.DataFrame({
        "Equipo": teams,
        "Posicion": range(1, len(teams) + 1),
        "Escudo": badges
    })

    return df