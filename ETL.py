import pandas as pd
from pathlib import Path

# Construcción segura de rutas
BASE_DIR = Path("Datos").resolve()
input_file = BASE_DIR / "Datos.csv"
output_file = BASE_DIR / "Datos_limpios.csv"

# Lectura del archivo con el argumento correcto
df = pd.read_csv(input_file, low_memory=False)

print(f"Rows loaded from raw file: {len(df)}")

# Limpieza de nombres de columnas
df.columns = (
    df.columns
      .str.lower()
      .str.strip()
      .str.replace(" ", "")
)

# Conversión de fechas
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

# Conversión de columnas numéricas
numeric_columns = [
    "cantidad",
    "precio_unitario",
    "descuento",
    "costo_envio",
    "total"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Filtros de calidad
df = df[
    (df["total"] > 0) &
    (df["cantidad"] > 0) &
    (df["precio_unitario"] > 0)
]

# Eliminación de nulos en columnas clave
df = df.dropna(subset=["fecha", "producto", "pais"])

# Eliminación de duplicados
df = df.drop_duplicates(
    subset=["fecha", "producto", "ciudad", "total"]
)

# Filtro por rango de fechas
df = df[
    (df["fecha"] >= "2015-01-01") &
    (df["fecha"] <= pd.Timestamp.today())
]

# Nuevas columnas
df["year"] = df["fecha"].dt.year
df["month"] = df["fecha"].dt.month
df["total_sales"] = df["total"]

print(f"Rows after cleaning: {len(df)}")

# Exportación del archivo limpio
df.to_csv(output_file, index=False)

print(f"Clean dataset created at: {output_file}")
