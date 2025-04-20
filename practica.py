# Importación de librerías
from imports import *

# Importar funciones definidas en otro archivo
from funciones import *

# 2. Extracción de datos
df = pd.read_csv('pacientes_sucio.csv', encoding='latin1') # Lectura del excel, se utiliza latin1 para leer caracteres especiales

# Configuración y visualización de los 5 primeros datos con todas sus columnas
pd.set_option('display.max_columns', None) # Se configura pandas para que muestre todas las columnas
print("Primeras filas del dataset original:") # Mensaje genérico para avisar lo que se visualizara despues (La tabla)
print(df.head()) # Se visualiza todas las columnas con sus filas, por defecto mostrará 5 columnas mediante el head

# Configuración y visualización de todos los datos con todas sus columnas
pd.set_option('display.max_rows', None) # Se configura Pandas para que muestre todas las filas tambien
print("Se muestran todas los registros del dataset original:") # Mensaje genérico para avisar lo que se visualizara despues (La tabla)
print(df) # Instrucción para mostrar lo leido anteriormente Filas y columnas

# 3. Proceso tratamiento de datos
# 3.1 Registros duplicados
df = df.drop_duplicates() #Elimina únicamente las filas que son identicas

# 3.2 Limpieza columnas
# 3.2.1 Limpieza de edad
df['Edad'] = df['Edad'].apply(limpiar_edad) # La funcion definida limpiar edad (Pasa texto a número)
df['Edad'] = df['Edad'].apply(lambda x: abs(x) if x < 120 else np.nan) # Todo número negativo pasa a positivo, si es mayor a 120 es eliminado

# 3.2.2 Estandarizar fechas
df['Fecha_Consulta'] = df['Fecha_Consulta'].astype(str).str.replace(r"[./]", "-", regex=True) # Todo "." es transformado a -
df['Fecha_Consulta'] = df['Fecha_Consulta'].apply(procesarFecha) # Se define el uso de una función

# 3.2.3 Columnas numéricas (Peso - altura)
df['Peso_kg'] = pd.to_numeric(df['Peso_kg'], errors='coerce')
df['Altura_cm'] = pd.to_numeric(df['Altura_cm'], errors='coerce')

# 3.2.4 Limpieza de Género
detector = gender.Detector(case_sensitive=False)
df['Género'] = df['Género'].str.upper().str.strip()
df['Género'] = df.apply(lambda row: prediccionGenero(row, detector), axis=1)

# 3.2.5 Estandarizar Teléfonos
df['Teléfono'] = df['Teléfono'].apply(limpiar_telefono)

# 3.2.6 Separar Presión arterial:
df[['Presion_Sistolica', 'Presion_Diastolica']] = df['Presión_Arterial'].apply(separar_presion)

# 3.2.7 Manejar nombres faltantes
df['Nombre'] = df['Nombre'].fillna('Paciente_' + df['ID_Paciente'].astype(str))

# 3.3 Calculamos campos derivados
# 3.3.1 IMC
df['IMC'] = df['Peso_kg'] / (df['Altura_cm'] / 100) ** 2

# 3.3.2 Clasificación Presión Arterial
df['Clasificacion_Presion'] = df.apply(lambda x: clasificar_presion(x['Presion_Sistolica'], x['Presion_Diastolica']),axis=1)