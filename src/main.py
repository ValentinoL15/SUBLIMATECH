from src.extract import extract_logistics, extract_production, extract_sales
from src.load.sql_loader import cargar_a_stg
from src.transform import transform_logistics, transform_production, transform_sales


def ejecutar_pipline_sublimatech():
  print("--- 🔄 Procesando pipline... ---")
  
  # 1. Extracción de dataframes
  print("Extrayendo datos...")
  df_logistics = extract_logistics()
  df_production = extract_production()
  df_sales = extract_sales()
  
  # 2. Transformación de datos
  print("Aplicando reglas de limpieza...")
  df_logistics_limpio = transform_logistics(df_logistics)
  df_production_limpio = transform_production(df_production)
  df_sales_limpio = transform_sales(df_sales)
  
  # 3. Carga al staging de sql 
  print("\nIniciando carga a la base de datos...")
  cargar_a_stg(df=df_logistics_limpio, nombre_tabla='stg_logistics')
  cargar_a_stg(df=df_production_limpio, nombre_tabla='stg_production')
  cargar_a_stg(df=df_sales_limpio, nombre_tabla='stg_sales')
  
  print("\n--- ✅ Pipeline ejecutado con éxito. ---")
  
if __name__ == "__main__":
  ejecutar_pipline_sublimatech()
  























