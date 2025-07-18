
def evaluate_predictions(predictions_df, rankings_df):
    merged = predictions_df.merge(rankings_df, on="Equipo", how="left")
    merged["Posiciones exactas"] = merged["Predicción"] == merged["Posición"]
    merged["Error absoluto"] = abs(merged["Predicción"] - merged["Posición"])

    summary = merged.groupby("Nombre").agg({
        "Posiciones exactas": "sum",
        "Error absoluto": "sum"
    }).reset_index()

    summary["Ranking exacto"] = summary["Posiciones exactas"].rank(ascending=False, method="min")
    summary["Ranking aproximaciones"] = summary["Error absoluto"].rank(ascending=True, method="min")
    return summary, merged