"""
Tests para src/utils/formatters.py y src/transform/transform_*.py
 
Ubicación sugerida en el repo: tests/test_formatters_and_transform.py
"""
import datetime as dt

import pandas as pd

from src.transform.transform_logistics import transform_logistics
from src.transform.transform_production import transform_production
from src.transform.transform_sales import transform_sales
from src.utils.formatters import (
    modificar_tipo_fecha,
    modificar_tipo_horarios,
    quitar_espacios_str,
    reemplazar_valores,
    rellenar_fechas_nulas,
    rellenar_horarios_nulos,
)

# ---------------------------------------------------------------------------
# formatters.quitar_espacios_str
# ---------------------------------------------------------------------------
 
def test_quitar_espacios_str_recorta_columnas_texto():
    df = pd.DataFrame({
        'nombre': [' Juan ', 'Ana  ', '  Luis'],
        'numero': [1, 2, 3],
    })
    resultado = quitar_espacios_str(df)
    assert resultado['nombre'].tolist() == ['Juan', 'Ana', 'Luis']
 
 
def test_quitar_espacios_str_no_toca_columnas_numericas():
    df = pd.DataFrame({
        'nombre': [' Juan '],
        'numero': [10],
    })
    resultado = quitar_espacios_str(df)
    assert resultado['numero'].tolist() == [10]
 
 
def test_quitar_espacios_str_retorna_nuevo_dataframe():
    df = pd.DataFrame({'col': [' a ', ' b ']})
    resultado = quitar_espacios_str(df)
    assert isinstance(resultado, pd.DataFrame)
    assert resultado['col'].tolist() == ['a', 'b']
 
 
# ---------------------------------------------------------------------------
# formatters.reemplazar_valores
# ---------------------------------------------------------------------------
 
def test_reemplazar_valores_un_solo_valor():
    df = pd.DataFrame({'provincia_destino': ['Sta Fe', 'Cordoba']})
    reemplazar_valores(df, 'provincia_destino', ['Sta Fe'], 'Santa Fe')
    assert df['provincia_destino'].tolist() == ['Santa Fe', 'Cordoba']
 
 
def test_reemplazar_valores_lista_de_valores():
    df = pd.DataFrame({'provincia_destino': ['B. Aires', 'Bs As', 'Santa Fe']})
    reemplazar_valores(df, 'provincia_destino', ['B. Aires', 'Bs As'], 'Buenos Aires')
    assert df['provincia_destino'].tolist() == ['Buenos Aires', 'Buenos Aires', 'Santa Fe']
 
 
def test_reemplazar_valores_no_afecta_valores_no_listados():
    df = pd.DataFrame({'provincia_destino': ['Mendoza']})
    reemplazar_valores(df, 'provincia_destino', ['Sta Fe'], 'Santa Fe')
    assert df['provincia_destino'].tolist() == ['Mendoza']
 
 
# ---------------------------------------------------------------------------
# formatters.modificar_tipo_fecha
# ---------------------------------------------------------------------------
 
def test_modificar_tipo_fecha_convierte_a_datetime():
    df = pd.DataFrame({'fecha': ['05/01/2024', '20/03/2024']})
    modificar_tipo_fecha(df, ['fecha'])
    assert pd.api.types.is_datetime64_any_dtype(df['fecha'])
    # dayfirst=True -> 05/01/2024 es 5 de enero
    assert df['fecha'].iloc[0] == pd.Timestamp('2024-01-05')
 
 
def test_modificar_tipo_fecha_valor_invalido_es_nat():
    df = pd.DataFrame({'fecha': ['no es una fecha']})
    modificar_tipo_fecha(df, ['fecha'])
    assert pd.isna(df['fecha'].iloc[0])
 
 
def test_modificar_tipo_fecha_multiples_columnas():
    df = pd.DataFrame({
        'fecha_a': ['01/01/2024'],
        'fecha_b': ['15/06/2024'],
    })
    modificar_tipo_fecha(df, ['fecha_a', 'fecha_b'])
    assert pd.api.types.is_datetime64_any_dtype(df['fecha_a'])
    assert pd.api.types.is_datetime64_any_dtype(df['fecha_b'])
 
 
# ---------------------------------------------------------------------------
# formatters.modificar_tipo_horarios
# ---------------------------------------------------------------------------
 
def test_modificar_tipo_horarios_convierte_a_time():
    df = pd.DataFrame({'hora': ['14:30:00', '08:05:00']})
    modificar_tipo_horarios(df, ['hora'])
    assert df['hora'].iloc[0] == dt.time(14, 30, 0)
    assert df['hora'].iloc[1] == dt.time(8, 5, 0)
 
 
def test_modificar_tipo_horarios_valor_invalido_es_nat():
    df = pd.DataFrame({'hora': ['no es una hora']})
    modificar_tipo_horarios(df, ['hora'])
    assert pd.isna(df['hora'].iloc[0])
 
 
# ---------------------------------------------------------------------------
# formatters.rellenar_fechas_nulas
# ---------------------------------------------------------------------------
 
def test_rellenar_fechas_nulas_completa_con_1900():
    df = pd.DataFrame({'fecha': [pd.NaT, pd.Timestamp('2024-01-01')]})
    rellenar_fechas_nulas(df, ['fecha'])
    assert df['fecha'].iloc[0] == pd.Timestamp('1900-01-01')
    assert df['fecha'].iloc[1] == pd.Timestamp('2024-01-01')
 
 
def test_rellenar_fechas_nulas_no_pisa_valores_existentes():
    df = pd.DataFrame({'fecha': [pd.Timestamp('2024-05-05')]})
    rellenar_fechas_nulas(df, ['fecha'])
    assert df['fecha'].iloc[0] == pd.Timestamp('2024-05-05')
 
 
# ---------------------------------------------------------------------------
# formatters.rellenar_horarios_nulos
# ---------------------------------------------------------------------------
 
def test_rellenar_horarios_nulos_completa_con_medianoche():
    df = pd.DataFrame({'hora': [None, dt.time(9, 0, 0)]})
    rellenar_horarios_nulos(df, ['hora'])
    assert df['hora'].iloc[0] == dt.time(0, 0, 0)
    assert df['hora'].iloc[1] == dt.time(9, 0, 0)
 
 
# ---------------------------------------------------------------------------
# transform_logistics
# ---------------------------------------------------------------------------
 
def _df_logistics_crudo():
    return pd.DataFrame({
        'orden': [' ord001 ', 'ORD002', ' 003'],
        'provincia_destino': ['B. Aires', 'Sta Fe', 'CABA'],
        'fecha_despacho': ['01/02/2024 10:00:00', '02/02/2024 11:30:00', None],
        'fecha_entrega': ['03/02/2024 15:00:00', None, '05/02/2024 09:00:00'],
        'costo_envio': [100.0, -50.0, 200.0],
    })
 
 
def test_transform_logistics_normaliza_columna_orden():
    df = transform_logistics(_df_logistics_crudo())
    assert df['orden'].tolist() == ['ORD001', 'ORD002', 'ORD-003']
 
 
def test_transform_logistics_estandariza_provincia():
    df = transform_logistics(_df_logistics_crudo())
    assert df['provincia_destino'].tolist() == ['Buenos Aires', 'Santa Fe', 'CABA']
 
 
def test_transform_logistics_divide_fecha_y_hora():
    df = transform_logistics(_df_logistics_crudo())
    assert 'fecha_despacho' in df.columns
    assert 'hora_despacho' in df.columns
    assert 'fecha_entrega' in df.columns
    assert 'hora_entrega' in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df['fecha_despacho'])
 
 
def test_transform_logistics_costo_envio_siempre_positivo():
    df = transform_logistics(_df_logistics_crudo())
    assert (df['costo_envio'] >= 0).all()
 
 
def test_transform_logistics_rellena_fechas_y_horas_nulas():
    df = transform_logistics(_df_logistics_crudo())
    # Ninguna fecha/hora debería quedar nula tras el paso de relleno
    assert not df['fecha_despacho'].isna().any()
    assert not df['fecha_entrega'].isna().any()
    assert not df['hora_despacho'].isna().any()
    assert not df['hora_entrega'].isna().any()
 
 
def test_transform_logistics_elimina_duplicados():
    df_crudo = _df_logistics_crudo()
    df_con_duplicado = pd.concat([df_crudo, df_crudo.iloc[[0]]], ignore_index=True)
    df = transform_logistics(df_con_duplicado)
    assert len(df) == len(df_crudo)
 
 
# ---------------------------------------------------------------------------
# transform_production
# ---------------------------------------------------------------------------
 
def _df_production_crudo():
    return pd.DataFrame({
        'pedido_ref': [' ord001 ', '002'],
        'detalles_taller.maquina_sublimacion': ['M1', 'M2'],
        'detalles_taller.operador': ['Juan', None],
        'detalles_taller.inicio_estampado': [
            '2024-02-01T10:00:00', '2024-02-02T11:00:00'
        ],
        'detalles_taller.fin_confeccion': [
            '2024-02-01T12:00:00', '2024-02-02T13:00:00'
        ],
        'detalles_taller.control_calidad_ok': [True, False],
    })
 
 
def test_transform_production_renombra_columnas():
    df = transform_production(_df_production_crudo())
    for col in ['id_maquina', 'operador', 'inicio_estampado', 'fin_confeccion', 'control_calidad']:
        assert col in df.columns
 
 
def test_transform_production_separa_fecha_y_hora():
    df = transform_production(_df_production_crudo())
    assert 'fecha_inicio_estampado' in df.columns
    assert 'hora_inicio_estampado' in df.columns
    assert 'fecha_fin_confeccion' in df.columns
    assert 'hora_fin_confeccion' in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df['fecha_inicio_estampado'])
 
 
def test_transform_production_completa_operador_nulo():
    df = transform_production(_df_production_crudo())
    assert df['operador'].tolist() == ['Juan', 'Desconocido']
 
 
def test_transform_production_normaliza_pedido_ref():
    df = transform_production(_df_production_crudo())
    assert df['pedido_ref'].tolist() == ['ORD001', 'ORD-002']
 
 
# ---------------------------------------------------------------------------
# transform_sales
# ---------------------------------------------------------------------------
 
def _df_sales_crudo():
    return pd.DataFrame({
        'fecha_compra': [' 01/02/2024 10:00:00 ', '02/02/2024 11:30:00'],
        'ingreso_total': [1000.0, -500.0],
    })
 
 
def test_transform_sales_divide_fecha_y_horario():
    df = transform_sales(_df_sales_crudo())
    assert 'fecha_de_compra' in df.columns
    assert 'horario' in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df['fecha_de_compra'])
 
 
def test_transform_sales_ingreso_total_siempre_positivo():
    df = transform_sales(_df_sales_crudo())
    assert (df['ingreso_total'] >= 0).all()
 
 
def test_transform_sales_horario_convertido_a_time():
    df = transform_sales(_df_sales_crudo())
    assert all(isinstance(valor, dt.time) for valor in df['horario'])