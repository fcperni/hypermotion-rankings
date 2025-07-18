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

def normalize_team_names(df):
    df["Equipo"] = df["Equipo"].replace(team_name_map)
    return df

def transpose_df(df):
    transposed = df.set_index(df.columns[0]).T
    transposed.index.name = None  # optional: remove "name" of index
    return transposed.reset_index().rename(columns={"index": df.columns[0]})