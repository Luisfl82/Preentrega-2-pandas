"""Genera los archivos fuente de ejemplo (CSV de transacciones + Excel de productos)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# --- Maestro de productos (Excel) ---
productos = pd.DataFrame({
    "id_producto": [101, 102, 103, 104, 105, 106, 107, 108],
    "nombre_producto": ["Cuaderno A4", "Lapicera azul", "Mochila", "Calculadora",
                        "Resaltador", "Carpeta", "Regla 30cm", "Mouse USB"],
    "precio_unitario": [1500.0, 450.0, 18000.0, 9500.0, 700.0, 2300.0, 600.0, 7800.0],
})
productos.to_excel("data/productos.xlsx", index=False)

# --- Transacciones (CSV) ---
n = 60
trans = pd.DataFrame({
    "id_producto": rng.choice([101, 102, 103, 104, 105, 106, 107, 108, 999], size=n),
    "cantidad": rng.integers(1, 6, size=n).astype(float),
    "fecha": pd.date_range("2025-01-01", periods=n, freq="D").strftime("%Y-%m-%d"),
})
# Ensucio un poco los datos a propósito (nulos) para practicar la limpieza
trans.loc[[5, 17], "cantidad"] = np.nan
trans.loc[[9], "fecha"] = None
trans.to_csv("data/transacciones.csv", index=False)
print("Archivos de ejemplo creados en la carpeta data/")
