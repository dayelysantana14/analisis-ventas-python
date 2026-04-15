
import os
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# CONFIGURACIÓN
# -------------------------------
DATA_PATH = "data/ventas.csv"
OUTPUT_DIR = "output"
REPORTE_PATH = os.path.join(OUTPUT_DIR, "reporte.txt")
GRAFICO_PATH = os.path.join(OUTPUT_DIR, "grafico.png")

# -------------------------------
# CREAR CARPETA OUTPUT SI NO EXISTE
# -------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------
# LEER DATOS
# -------------------------------
try:
    df = pd.read_csv(DATA_PATH)
    print("Datos cargados correctamente")
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    exit()

# -------------------------------
# LIMPIEZA DE DATOS
# -------------------------------
df = df.dropna()

# -------------------------------
# MÉTRICAS
# -------------------------------
total_ventas = df["ventas"].sum()
promedio_ventas = df["ventas"].mean()

top_vendedor = df.sort_values(by="ventas", ascending=False).iloc[0]

top_3 = df.sort_values(by="ventas", ascending=False).head(3)

ventas_por_categoria = df.groupby("categoria")["ventas"].sum()

# -------------------------------
# MOSTRAR RESULTADOS EN CONSOLA
# -------------------------------
print("\nRESULTADOS:")
print(f"Total ventas: {total_ventas}")
print(f"Promedio ventas: {promedio_ventas:.2f}")
print(f"Top vendedor: {top_vendedor['vendedor']} ({top_vendedor['ventas']})")

print("\nTop 3 vendedores:")
print(top_3)

# -------------------------------
# GENERAR REPORTE TXT
# -------------------------------
with open(REPORTE_PATH, "w", encoding="utf-8") as f:
    f.write("REPORTE DE VENTAS\n")
    f.write("=========================\n\n")
    f.write(f"Total ventas: {total_ventas}\n")
    f.write(f"Promedio ventas: {promedio_ventas:.2f}\n\n")

    f.write(f"Top vendedor:\n")
    f.write(f"{top_vendedor['vendedor']} - {top_vendedor['ventas']}\n\n")

    f.write("Top 3 vendedores:\n")
    f.write(top_3.to_string(index=False))
    f.write("\n\nVentas por categoría:\n")
    f.write(ventas_por_categoria.to_string())

print("Reporte generado en /output/reporte.txt")

# -------------------------------
# GENERAR GRÁFICO
# -------------------------------
plt.figure()
ventas_por_categoria.plot(kind="bar")
plt.title("Ventas por Categoría")
plt.xlabel("Categoría")
plt.ylabel("Ventas")

plt.tight_layout()
plt.savefig(GRAFICO_PATH)

print("Gráfico guardado en /output/grafico.png")

# -------------------------------
# MENSAJE FINAL
# -------------------------------
print("\nProceso completado exitosamente")