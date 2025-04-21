import gender_guesser.detector as gender
from text_to_num import text2num as txt
import pandas as pd
import numpy as np

def inicializar_reporte(df):
    return {
        'Edad_invalidas': df['Edad'].isna().sum(),  # Antes de limpiar
        'Edad_transformadas': 0,
        'Fechas_invalidas': 0,
        'Fechas_nulas': 0,
        'Genero_nulo': 0,
        'Peso_nulo': 0,
        'Altura_nula': 0,
        'Telefono_nulo': 0,
        'Presion_nula': 0,
        'Nombre_autogenerado': 0,
        'IMC_nulo': 0,
        'Clasificacion_Presion_nulo': 0
    }

def mostrar_reporte(reporte_dict):
    reporte_df = pd.DataFrame.from_dict(reporte_dict, orient='index', columns=['Cantidad'])
    print("\n📋 Reporte de Transformaciones de Datos:")
    print(reporte_df)
    return reporte_df

def exportar_reporte_csv(reporte_dict,     ruta = '/app/output/nombre_del_reporte.csv'):
    reporte_df = pd.DataFrame.from_dict(reporte_dict, orient='index', columns=['Cantidad'])
    reporte_df.to_csv(ruta)
    print(f"\n📁 Reporte exportado a {ruta}")
