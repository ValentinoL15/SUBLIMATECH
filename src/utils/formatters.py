import pandas as pd
import datetime as dt

# Cambiamos el tipo de retorno de None a pd.DataFrame
def quitar_espacios_str(df: pd.DataFrame) -> pd.DataFrame:
    # Retornamos el nuevo dataframe modificado
    return df.apply(lambda x: x.str.strip() if x.dtype == 'object' or x.dtype == 'string' else x)
  
def rellenar_fechas_nulas(df: pd.DataFrame, cols: list) -> None:
  for col in cols:
    df[col] = df[col].fillna(pd.to_datetime('1900-01-01'))
    
def rellenar_horarios_nulos(df: pd.DataFrame, cols: list ) -> None:
  for col in cols:
    df[col] = df[col].fillna(dt.time(0, 0, 0))
    
def modificar_tipo_fecha(df: pd.DataFrame, cols: list) -> None:
  for col in cols:
    df[col] = pd.to_datetime(df[col], format='mixed', dayfirst=True, errors='coerce')
    
def modificar_tipo_horarios(df: pd.DataFrame, cols: list):
  for col in cols:
    df[col] = pd.to_datetime(df[col], format='mixed', errors='coerce').dt.time
    
def reemplazar_valores(df: pd.DataFrame, col: str ,words_to_replace: list[str], to: str) -> None:
  df[col] = df[col].replace(words_to_replace,to, regex=False)