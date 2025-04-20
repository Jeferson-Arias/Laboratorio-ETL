# Importación de librerías
from imports import *

# Importar funciones definidas en otro archivo
from funciones import *
from reporte_transformaciones import *

# 2. Extracción de datos
df = pd.read_csv('pacientes_sucio.csv', encoding='latin1') # Lectura del excel, se utiliza latin1 para leer caracteres especiales

pd.set_option('display.max_columns', None)
print("Primeras filas del dataset original:")
print(df.head())

pd.set_option('display.max_rows', None)
print("Se muestran todas los registros del dataset original:")
print(df)

reporte = inicializar_reporte(df)

# 3. Proceso tratamiento de datos
# 3.1 Registros duplicados
df = df.drop_duplicates()

# 3.2 Limpieza columnas
# 3.2.1 Limpieza de edad
edad_antes = df['Edad'].copy()
df['Edad'] = df['Edad'].apply(limpiar_edad)
df['Edad'] = df['Edad'].apply(lambda x: abs(x) if x < 120 else np.nan)
reporte['Edad_transformadas'] = (edad_antes != df['Edad']).sum()
reporte['Edad_invalidas'] = df['Edad'].isna().sum()

# 3.2.2 Estandarizar fechas
fechas_antes = df['Fecha_Consulta'].copy()
df['Fecha_Consulta'] = df['Fecha_Consulta'].astype(str).str.replace(r"[./]", "-", regex=True)
df['Fecha_Consulta'] = df['Fecha_Consulta'].apply(procesarFecha)
reporte['Fechas_invalidas'] = (fechas_antes != df['Fecha_Consulta']).sum()
reporte['Fechas_nulas'] = df['Fecha_Consulta'].isna().sum()

# 3.2.3 Columnas numéricas (Peso - altura)
df['Peso_kg'] = pd.to_numeric(df['Peso_kg'], errors='coerce')
df['Altura_cm'] = pd.to_numeric(df['Altura_cm'], errors='coerce')
reporte['Peso_nulo'] = df['Peso_kg'].isna().sum()
reporte['Altura_nula'] = df['Altura_cm'].isna().sum()

# 3.2.4 Limpieza de Género
detector = gender.Detector(case_sensitive=False)
df['Género'] = df['Género'].str.upper().str.strip()
df['Género'] = df.apply(lambda row: prediccionGenero(row, detector), axis=1)
reporte['Genero_nulo'] = df['Género'].isna().sum()

# 3.2.5 Estandarizar Teléfonos
df['Teléfono'] = df['Teléfono'].apply(limpiar_telefono)
reporte['Telefono_nulo'] = df['Teléfono'].isna().sum()

# 3.2.6 Separar Presión arterial:
df[['Presion_Sistolica', 'Presion_Diastolica']] = df['Presión_Arterial'].apply(separar_presion)
reporte['Presion_nula'] = df['Presion_Sistolica'].isna().sum() + df['Presion_Diastolica'].isna().sum()

# 3.2.7 Manejar nombres faltantes
nombres_antes = df['Nombre'].isna().sum()
df['Nombre'] = df['Nombre'].fillna('Paciente_' + df['ID_Paciente'].astype(str))
reporte['Nombre_autogenerado'] = nombres_antes

# 3.3 Calculamos campos derivados
# 3.3.1 IMC
df['IMC'] = df['Peso_kg'] / (df['Altura_cm'] / 100) ** 2
reporte['IMC_nulo'] = df['IMC'].isna().sum()

# 3.3.2 Clasificación Presión Arterial
df['Clasificacion_Presion'] = df.apply(lambda x: clasificar_presion(x['Presion_Sistolica'], x['Presion_Diastolica']),axis=1)
reporte['Clasificacion_Presion_nulo'] = df['Clasificacion_Presion'].isna().sum()

# mostrar resumen general
mostrar_reporte(reporte)
print(pd)

# Exportar resultados
df.to_csv('pacientes_limpio.csv', index=False, encoding='utf-8-sig')
exportar_reporte_csv(reporte)