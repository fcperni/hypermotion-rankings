
def evaluate_predictions(predictions_df, rankings_df):
    merged = predictions_df.merge(rankings_df, on="Equipo", how="left")
    merged["Posición exacta"] = merged["Predicción"] == merged["Posicion"]
    merged["Error absoluto"] = abs(merged["Predicción"] - merged["Posicion"])

    summary = merged.groupby("Nombre").agg({
        "Posición exacta": "sum",
        "Error absoluto": "sum"
    }).reset_index()

    summary["Ranking exacto"] = summary["Posición exacta"].rank(ascending=False, method="min")
    summary["Ranking aproximaciones"] = summary["Error absoluto"].rank(ascending=True, method="min")
    return summary, merged