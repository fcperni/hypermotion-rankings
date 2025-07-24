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
}

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

def normalize_team_names(df):
    df["Equipo"] = df["Equipo"].replace(team_name_map)
    return df

def transpose_df(df):
    transposed = df.set_index(df.columns[0]).T
    transposed.index.name = None  # optional: remove "name" of index
    return transposed.reset_index().rename(columns={"index": df.columns[0]})
