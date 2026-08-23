import pandas as pd
import json

def extract_production() -> pd.DataFrame:
    with open('data/raw/production/produccion_taller.json', 'r', encoding='UTF-8') as archivo:
        data_parsed = json.load(archivo)
        
    df_production = pd.json_normalize(data_parsed)
    
    return df_production
