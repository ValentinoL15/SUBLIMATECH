import pandas as pd
from src.config.database import engine

def cargar_a_stg(df: pd.DataFrame, nombre_tabla: str):
    """Carga un DataFrame directamente al entorno de Staging en SQL Server."""
    
    # 1. Validamos que el motor exista
    if not engine:
        print("❌ Error: No hay conexión al motor de base de datos.")
        return
        
    # 2. Validamos que el DataFrame no esté vacío para no borrar la tabla por accidente
    if df.empty:
        print(f"⚠️ Alerta: El DataFrame para '{nombre_tabla}' está vacío. Se omite la carga.")
        return
        
    print(f"⏳ Iniciando la carga de {len(df):,} filas en la tabla '{nombre_tabla}'...")
    
    # 3. Ejecutamos la carga segura
    df.to_sql(
        name=nombre_tabla,
        con=engine,
        schema='dbo',
        if_exists='replace',
        index=False           # No sube el índice numérico de Pandas
    )
    
    print(f"✅ Tabla '{nombre_tabla}' reemplazada y cargada exitosamente en Staging.")