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
    
    # Si comienza con 4 dígitos, es probable que sea YYYY-MM-DD
    if len(date_str) >= 4 and date_str[0:4].isdigit():
        return pd.to_datetime(date_str, errors='coerce', format='%Y-%m-%d')
    
    # Si no, asumimos que es DD-MM-YYYY
    else:
        return pd.to_datetime(date_str, errors='coerce', format='%d-%m-%Y')
    
def prediccionGenero(row, detector):
    if pd.isna(row['Género']) or row['Género'] not in ['M', 'F']:
        try:
            # Extraer el primer nombre
            nombre = str(row['Nombre']).split()[0]
            # Convertir a string para manejar valores no string
            nombre = str(nombre).strip()
            
            # Asegurarse de que el nombre tenga al menos un carácter
            if len(nombre) > 0:
                genero_predicho = detector.get_gender(nombre)
                
                # Mapear la respuesta a M o F
                if genero_predicho in ['male', 'mostly_male']:
                    return 'M'
                elif genero_predicho in ['female', 'mostly_female']:
                    return 'F'
            
            return np.nan  # Si no se puede determinar
        except Exception as e:
            print(f"Error procesando el nombre: {row.get('Nombre', 'N/A')}. Error: {e}")
            return np.nan
    else:
        return row['Género']  # Mantener el valor original si es M o F
    
def limpiar_telefono(telefono):
    # Convertir a string y eliminar caracteres no numéricos
    telefono = str(telefono).strip()
    solo_numeros = ''.join(c for c in telefono if c.isdigit())
    
    # Si está vacío, devolver NaN
    if not solo_numeros:
        return np.nan
    
    # Si tiene 10 dígitos, ya está en formato correcto
    if len(solo_numeros) == 10:
        return solo_numeros
    
    # Si comienza con 1 y tiene 11 dígitos (código de país norteamericano)
    elif len(solo_numeros) == 11 and solo_numeros.startswith('1'):
        return solo_numeros[1:]  # Quitar el código de país
    
    # En cualquier otro caso, devolver NaN o el original según prefieras
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