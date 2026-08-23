import pandas as pd
from src.utils.formatters import quitar_espacios_str,rellenar_fechas_nulas


def transform_sales(dataframe: pd.DataFrame) -> pd.DataFrame:
  print(f'Leyendo dataframe {dataframe}')
  
  df = dataframe
  
  # 1. Quita espacios en blanco a todas las columnas str
  df = quitar_espacios_str(df)
  
  # 2. Dividimos la columna fecha_compra en dos columnas para dividir con el tiempo
  df[['fecha_de_compra', 'horario']] = df['fecha_compra'].str.split(' ', expand=True)
  df['fecha_compra'] = pd.to_datetime(df['fecha_compra'], format='mixed', dayfirst=True, errors='coerce')
  df['fecha_de_compra'] = pd.to_datetime(df['fecha_de_compra'], format='mixed', errors='coerce')
  
  # 3. Manejar ingresos negativos
  df.loc[df['ingreso_total'] < 0, 'ingreso_total'] = df['ingreso_total'] * -1
  
  # 4. Transformar horarios en timedelta
  df['horario'] = pd.to_timedelta(df['horario'], errors='coerce')
  
  # 5. Rellenar dechas y horarios nulos
  rellenar_fechas_nulas(df, ['fecha_compra', 'fecha_de_compra'])
  df['horario'] = df['horario'].fillna(pd.to_timedelta('00:00:00'))
  
  # 6. Eliminar duplicados
  df.drop_duplicates()
  
  return df

