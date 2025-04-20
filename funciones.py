# Importación de librerías
from imports import *

def limpiar_edad(valor):
    valor = str(valor).strip().lower()
    try:
        return pd.to_numeric(valor, errors='raise')
    except:
        try:
            return txt(valor, "es")
        except:
            return np.nan
        
def procesarFecha(date_str):
    date_str = str(date_str).strip()
    
    if len(date_str) >= 4 and date_str[0:4].isdigit():
        return pd.to_datetime(date_str, errors='coerce', format='%Y-%m-%d')

    else:
        return pd.to_datetime(date_str, errors='coerce', format='%d-%m-%Y')
    
def prediccionGenero(row, detector):
    if pd.isna(row['Género']) or row['Género'] not in ['M', 'F']:
        try:
            nombre = str(row['Nombre']).split()[0]
            nombre = str(nombre).strip()

            if len(nombre) > 0:
                genero_predicho = detector.get_gender(nombre)

                if genero_predicho in ['male', 'mostly_male']:
                    return 'M'
                elif genero_predicho in ['female', 'mostly_female']:
                    return 'F'
            
            return np.nan
        except Exception as e:
            print(f"Error procesando el nombre: {row.get('Nombre', 'N/A')}. Error: {e}")
            return np.nan
    else:
        return row['Género']
    
def limpiar_telefono(telefono):
    telefono = str(telefono).strip()
    solo_numeros = ''.join(c for c in telefono if c.isdigit())
    
    if not solo_numeros:
        return np.nan
    
    if len(solo_numeros) == 10:
        return solo_numeros
    
    elif len(solo_numeros) == 11 and solo_numeros.startswith('1'):
        return solo_numeros[1:]  # Quitar el código de país
    
    else:
        return np.nan

def separar_presion(presion):
    if isinstance(presion, str) and '/' in presion:
        try:
            sistolica, diastolica = presion.split('/')
            return pd.Series([int(sistolica), int(diastolica)])
        except:
            return pd.Series([np.nan, np.nan])
    return pd.Series([np.nan, np.nan])

def clasificar_presion(sis, dia):
    if pd.isna(sis) or pd.isna(dia):
        return np.nan
    if sis < 120 and dia < 80:
        return 'Normal'
    elif 120 <= sis < 130 and dia < 80:
        return 'Elevada'
    elif 130 <= sis < 140 or 80 <= dia < 90:
        return 'Hipertensión Grado 1'
    elif sis >= 140 or dia >= 90:
        return 'Hipertensión Grado 2'
    else:
        return 'Desconocida'