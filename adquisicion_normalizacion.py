"""
Preentrega 2 - Adquisición y normalización con pandas
Lee un CSV (transacciones) y un Excel (productos), los une, limpia y exporta a Parquet.
"""
import pandas as pd

RUTA_CSV = "data/transacciones.csv"
RUTA_EXCEL = "data/productos.xlsx"
RUTA_SALIDA = "output/ventas_final.parquet"


def cargar_datos():
    """ADQUISICIÓN: lee las dos fuentes de formatos distintos."""
    transacciones = pd.read_csv(RUTA_CSV)
    productos = pd.read_excel(RUTA_EXCEL, engine="openpyxl")
    print(f"Transacciones cargadas: {transacciones.shape}")
    print(f"Productos cargados:     {productos.shape}")
    return transacciones, productos


def corregir_tipos(transacciones, productos):
    """TRANSFORMACIÓN 1: tipos de datos correctos."""
    # La fecha pasa de texto a datetime (los errores quedan como NaT)
    transacciones["fecha"] = pd.to_datetime(transacciones["fecha"], errors="coerce")
    # Los IDs deben ser del MISMO tipo en ambas tablas, si no el merge falla
    transacciones["id_producto"] = transacciones["id_producto"].astype("int64")
    productos["id_producto"] = productos["id_producto"].astype("int64")
    return transacciones, productos


def manejar_nulos(transacciones):
    """TRANSFORMACIÓN 2: nulos.
    - fecha nula  -> se ELIMINA la fila (sin fecha no sirve para analizar ventas)
    - cantidad nula -> se IMPUTA con la mediana (un valor típico)
    """
    antes = len(transacciones)
    transacciones = transacciones.dropna(subset=["fecha"]).copy()
    mediana = transacciones["cantidad"].median()
    transacciones["cantidad"] = transacciones["cantidad"].fillna(mediana)
    print(f"Filas eliminadas por fecha nula: {antes - len(transacciones)}")
    print(f"Cantidades nulas imputadas con la mediana ({mediana})")
    return transacciones


def unir_y_calcular(transacciones, productos):
    """TRANSFORMACIÓN 3 + NORMALIZACIÓN: merge y columna calculada."""
    df = transacciones.merge(productos, on="id_producto", how="inner")
    df["total_venta"] = df["cantidad"] * df["precio_unitario"]
    return df


def verificar_calidad(df):
    """Chequeo final: no debe haber nulos en columnas críticas."""
    criticas = ["id_producto", "cantidad", "fecha", "precio_unitario", "total_venta"]
    nulos = df[criticas].isna().sum()
    assert nulos.sum() == 0, f"Hay nulos en columnas críticas:\n{nulos}"
    print("OK: no hay nulos en columnas críticas")


def main():
    transacciones, productos = cargar_datos()
    transacciones, productos = corregir_tipos(transacciones, productos)
    transacciones = manejar_nulos(transacciones)
    df = unir_y_calcular(transacciones, productos)
    verificar_calidad(df)

    # EXPORTACIÓN a Parquet (necesita pyarrow instalado)
    df.to_parquet(RUTA_SALIDA, index=False)
    print(f"Archivo final guardado en {RUTA_SALIDA} con {len(df)} filas")
    print(df.head())


if __name__ == "__main__":
    main()
