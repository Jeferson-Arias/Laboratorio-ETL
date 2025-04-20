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