import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =================================================================
# 1. CONFIGURACIÓN DE RUTAS Y CONSTANTES
# =================================================================
# Definimos las rutas de forma centralizada para facilitar el mantenimiento
DATA_PATH = "data/ventas.csv"
OUTPUT_DIR = "output"
REPORTE_PATH = os.path.join(OUTPUT_DIR, "reporte_ventas.txt")
GRAFICO_PATH = os.path.join(OUTPUT_DIR, "grafico_pro.png")

def procesar_datos(path):
    """
    Carga el dataset y realiza el pre-procesamiento inicial (Data Cleaning).
    """
    try:
        # Lectura del archivo fuente
        df = pd.read_csv(path)
        
        # Estandarización de fechas: Convierte strings a objetos datetime
        # Si la columna no existe, usa la fecha actual como fallback
        df['fecha'] = pd.to_datetime(df.get('fecha', pd.Timestamp.now()))
        
        # Limpieza de registros críticos: Eliminamos filas sin ventas o sin categoría
        # Esto asegura la integridad de los cálculos posteriores
        df = df.dropna(subset=['ventas', 'categoria'])
        
        return df
    except Exception as e:
        # Manejo de excepciones para evitar que el script falle por errores de archivo
        print(f"Error en la carga de datos: {e}")
        return None

def generar_entregables(df):
    """
    Transforma los datos en información de valor (Métricas y Gráficos).
    """
    # --- ANÁLISIS DESCRIPTIVO (Métricas Clave) ---
    total_ventas = df["ventas"].sum()
    promedio_ventas = df["ventas"].mean()
    
    # Identificación de los registros con mayor impacto
    top_3 = df.sort_values(by="ventas", ascending=False).head(3)
    
    # Agregación de datos por categoría para análisis comparativo
    ventas_por_cat = df.groupby("categoria")["ventas"].sum().sort_values(ascending=False)

    # --- GENERACIÓN DE REPORTE DE TEXTO (Persistencia de Datos) ---
    # Usamos 'with open' para garantizar el cierre correcto del archivo tras escribir
    with open(REPORTE_PATH, "w", encoding="utf-8") as f:
        f.write("REPORTE DE ANÁLISIS DE VENTAS\n")
        f.write("="*30 + "\n\n")
        # Formateamos números con separadores de miles y 2 decimales
        f.write(f"Ventas Totales: ${total_ventas:,.2f}\n")
        f.write(f"Promedio de Venta: ${promedio_ventas:,.2f}\n\n")
        
        f.write("TOP 3 TRANSACCIONES:\n")
        f.write(top_3[['vendedor', 'ventas', 'categoria']].to_string(index=False))
        
        f.write("\n\nRESUMEN POR CATEGORÍA:\n")
        f.write(ventas_por_cat.to_string())

    print(f"Reporte generado: {REPORTE_PATH}")

    # --- GENERACIÓN DE VISUALIZACIÓN (Data Storytelling) ---
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid") # Estética moderna y legible
    
    # Gráfico de barras optimizado (Evitando Warnings de Seaborn)
    ax = sns.barplot(
        x=ventas_por_cat.index, 
        y=ventas_por_cat.values, 
        hue=ventas_por_cat.index, 
        palette="viridis",
        legend=False
    )
    
    # Personalización de etiquetas para presentación ejecutiva
    plt.title("Distribución de Ventas Totales por Categoría", fontsize=14, fontweight='bold')
    plt.ylabel("Ventas Acumuladas ($)")
    plt.xlabel("Categoría de Producto")
    
    plt.tight_layout() # Ajusta los márgenes para que nada se corte
    plt.savefig(GRAFICO_PATH)
    plt.close() # Cerramos la figura para liberar memoria RAM
    print(f"Gráfico exportado: {GRAFICO_PATH}")

# =================================================================
# 2. ORQUESTACIÓN (Punto de Entrada)
# =================================================================
if __name__ == "__main__":
    # Verificación de infraestructura: Aseguramos que existan los directorios necesarios
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Directorio '{OUTPUT_DIR}' creado.")

    # Ejecución del pipeline de datos
    datos = procesar_datos(DATA_PATH)
    
    if datos is not None:
        generar_entregables(datos)
        print("\nPipeline ejecutado correctamente. El proyecto está listo para su revisión.")