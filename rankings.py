import pandas as pd

# Cargar archivos
predicciones = pd.read_csv("predicciones.csv")
real = pd.read_csv("clasificacion_real.csv")

# Unir las predicciones con la tabla real
df = predicciones.merge(real, on="equipo")

# Calcular si es acierto exacto
df["acierto_exacto"] = df["posicion_predicha"] == df["posicion_real"]

# Calcular distancia entre posiciones
df["error_absoluto"] = abs(df["posicion_predicha"] - df["posicion_real"])

# Agrupar por persona
resumen = df.groupby("nombre").agg({
    "acierto_exacto": "sum",
    "error_absoluto": "sum"
}).reset_index()

# Ranking por aciertos exactos (más es mejor)
resumen["ranking_exactos"] = resumen["acierto_exacto"].rank(ascending=False, method="min")

# Ranking por aproximación (menos error es mejor)
resumen["ranking_aproximado"] = resumen["error_absoluto"].rank(ascending=True, method="min")

# Mostrar resultados
print(resumen.sort_values("ranking_exactos"))
