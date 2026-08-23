import pandas as pd

def extract_logistics() -> pd.DataFrame:
  return pd.read_excel('data/raw/logistics/logistica_envios.xlsx')
