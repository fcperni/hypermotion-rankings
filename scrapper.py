import requests
from bs4 import BeautifulSoup
import pandas as pd

team_logo_urls = {
    "Albacete": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/950.png",
    "Almería": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/1564.png",
    "Burgos": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/951.png",
    "Castellón": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/2500.png",
    "Ceuta": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/3556.png",
    "Cultural Leonesa": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/2506.png",
    "Cádiz": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/1737.png",
    "Córdoba": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/952.png",
    "Deportivo La Coruña": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/180.png",
    "Eibar": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/953.png",
    "FC Andorra": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/16310.png",
    "Granada": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/5683.png",
    "Huesca": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/2894.png",
    "Las Palmas": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/407.png",
    "Leganés": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/957.png",
    "Mirandés": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/5741.png",
    "Málaga": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/182.png",
    "Racing Santander": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/189.png",
    "2Real Sociedad II": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/3567.png",
    "Real Valladolid": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/192.png",
    "Real Zaragoza": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/190.png",
    "Sporting Gijón": "https://e00-marca.uecdn.es/assets/sports/logos/football/png/144x144/616.png"
}

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

    teams = []
    badges = []
    rows = target_table.find_all("tr")[1:]  # Skip header row
    suffix_index = 4
    for row in rows:
        if len(teams) == 9:
            suffix_index = suffix_index + 1
        team_name = row.text[suffix_index:]
        teams.append(team_name)
        badges.append(team_logo_urls.get(team_name))

    df = pd.DataFrame({
        "Equipo": teams,
        "Posicion": range(1, len(teams) + 1),
        "Escudo": badges
    })

    return df