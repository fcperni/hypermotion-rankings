import scrapper

def test_should_scrap_hypermotion_teams():
    df = scrapper.fetch_actual_standings()
    assert list(df.columns) == ["Equipo", "Posición", "Logo"]