import pandas as pd

from src.utils.formatters import (
  modificar_tipo_fecha,
  modificar_tipo_horarios,
  quitar_espacios_str,
)


def transform_production(dataframe: pd.DataFrame) -> pd.DataFrame:
  print(f'Leyendo dataframe {dataframe}')
  
  df = dataframe
    
  # 1. Quita espacios en blanco a todas las columnas str
  df = quitar_espacios_str(df)
  
  # 2. Cambios de nombres de columnas para más comodidad
  df = df.rename(columns={ 'detalles_taller.maquina_sublimacion': 'id_maquina',
                    'detalles_taller.operador': 'operador',
                    'detalles_taller.inicio_estampado': 'inicio_estampado',
                    'detalles_taller.fin_confeccion': 'fin_confeccion',
                    'detalles_taller.control_calidad_ok': 'control_calidad'})
  
  # 3. Separar la fecha y hora en columnas diferentes
  df[['fecha_inicio_estampado', 'hora_inicio_estampado']] = df['inicio_estampado'].str.split('T', expand=True)
  df[['fecha_fin_confeccion', 'hora_fin_confeccion']] = df['fin_confeccion'].str.split('T', expand=True)
  
  # 4. Pasamos los horarios y las fechas a sus respectivos formatos
  modificar_tipo_fecha(df,['fecha_inicio_estampado', 'fecha_fin_confeccion'])
  modificar_tipo_horarios(df,['hora_inicio_estampado', 'hora_fin_confeccion'])
  
  # 5. Completar los nombres nulos en 'Desconocido'
  df['operador'] = df['operador'].fillna('Desconocido')
  
  
  # 6. Normalizar los pedidos que no vienen con ORD- al principio 
  df['pedido_ref'] = df['pedido_ref'].str.strip().str.upper()

  mascara = df['pedido_ref'].str.startswith('ORD')

  df[~mascara]

  df.loc[~mascara, 'pedido_ref'] = "ORD-" + df['pedido_ref']
  
  # 7. Borrar duplicados
  df.drop_duplicates()
  
  return df
