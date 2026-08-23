import pandas as pd

def extract_sales() -> pd.DataFrame:
  return pd.read_csv('data/raw/sales/ventas_ecommerce.csv') 
