import sqlalchemy
from sqlalchemy import text

cadena_conexion = r'mssql+pyodbc://DESKTOP-2BA7LT9\SQLEXPRESS/sublimatech?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'

# Instanciamos el motor
engine = sqlalchemy.create_engine(cadena_conexion)

# --- PRUEBA DE CONEXIÓN ---
try:
    # Intentamos establecer la conexión
    with engine.connect() as connection:
        # Ejecutamos una consulta mínima para que el servidor responda
        connection.execute(text("SELECT 1"))
        print("✅ ¡Conexión exitosa a SQL Server!")
        
except Exception as e:
    print("❌ Error al intentar conectar con la base de datos.")
    print(f"Detalle del error:\n{e}")