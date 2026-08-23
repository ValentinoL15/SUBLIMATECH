import pandas as pd
from src.utils.formatters import quitar_espacios_str,rellenar_fechas_nulas, rellenar_horarios_nulos, modificar_tipo_fecha, reemplazar_valores, modificar_tipo_horarios

def transform_logistics(dataframe: pd.DataFrame) -> pd.DataFrame:
  print(f'Leyendo dataframe {dataframe}')
  
  df = dataframe
  
  # 1. Quita espacios en blanco a todas las columnas str
  df = quitar_espacios_str(df)
  
  # 2. Arreglar formato de la columna orden
  df['orden'] = df['orden'].str.strip().str.upper()
  mascara = df['orden'].str.startswith('ORD')
  df.loc[~mascara, 'orden'] = "ORD-" + df['orden']
  
  # 2.1. Estandarizamos el destino de la compra del producto
  reemplazar_valores(df,'provincia_destino',['B. Aires', 'Bs As',],'Buenos Aires')
  reemplazar_valores(df,'provincia_destino',['Ciudad Autonoma de Buenos Aires'],'CABA')
  reemplazar_valores(df,'provincia_destino',['Sta Fe'],'Santa Fe')
  
  # 3. Cambiar nombre columna
  df = df.rename(columns={'fecha_despacho': 'fecha_hora_despacho',
                          'fecha_entrega': 'fecha_hora_entrega'})
  
  # 4. Dividir columnas de despacho y entrega en fecha y hora
  df[['fecha_despacho', 'hora_despacho']] = df['fecha_hora_despacho'].str.strip().str.split(' ',expand=True)
  df[['fecha_entrega', 'hora_entrega']] = df['fecha_hora_entrega'].str.strip().str.split(' ',expand=True)
  
  # 5. Cambiar tipo de datos en fechas y horas
  modificar_tipo_fecha(df, ['fecha_despacho', 'fecha_entrega'])
  modificar_tipo_horarios(df, ['hora_despacho', 'hora_entrega'])
  
  # 6. Asegurarse de valores nulos en costo_envio
  df.loc[df['costo_envio'] < 0, 'costo_envio'] = df['costo_envio'] * -1
  
  # 7. Reemplazar valores nulos
  rellenar_fechas_nulas(df, ['fecha_despacho', 'fecha_entrega', 'fecha_hora_entrega'])
  rellenar_horarios_nulos(df, ['hora_despacho', 'hora_entrega'])
  
  # 8. Eliminar duplicados
  df = df.drop_duplicates()
  
  return df