# Preentrega 2 - Adquisición y normalización con pandas

Simula ventas que llegan de dos áreas en formatos distintos: un **CSV** de transacciones y un **Excel** con el maestro de productos. El script los une, los limpia y deja un archivo **Parquet** listo para analizar.

## Estructura
```
data/transacciones.csv   -> id_producto, cantidad, fecha
data/productos.xlsx      -> id_producto, nombre_producto, precio_unitario
adquisicion_normalizacion.py  -> script principal
generar_datos_ejemplo.py      -> crea los archivos de ejemplo
output/ventas_final.parquet   -> resultado final
requirements.txt
```

## Librerías necesarias
`pandas`, `openpyxl` (lee el Excel), `pyarrow` (escribe Parquet), `numpy`.

## Cómo reproducirlo
1. Clonar el repositorio y entrar a la carpeta.
2. Instalar librerías: `pip install -r requirements.txt`
3. (Opcional) regenerar los datos de ejemplo: `python generar_datos_ejemplo.py`
4. Ejecutar: `python adquisicion_normalizacion.py`
5. El resultado queda en `output/ventas_final.parquet`.

## Qué hace el script
1. **Adquisición:** `read_csv` y `read_excel`.
2. **Tipos:** `fecha` a `datetime`; `id_producto` a entero en ambas tablas (evita errores en el merge).
3. **Nulos:** se eliminan filas sin fecha; las cantidades nulas se imputan con la mediana.
4. **Merge:** `inner join` por `id_producto` (las ventas de productos que no existen en el catálogo quedan afuera).
5. **Columna calculada:** `total_venta = cantidad * precio_unitario`.
6. **Exportación:** archivo Parquet (más liviano y rápido que CSV).
