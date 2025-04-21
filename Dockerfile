FROM python:3.11.3-slim

WORKDIR /app

# Instalar dependencias
RUN pip install --no-cache-dir text2num pandas numpy gender-guesser

# Copiar los archivos del proyecto
COPY . /app/

# Definir un volumen para los archivos de salida
VOLUME /app/output

# Comando por defecto para ejecutar la aplicación
CMD ["python", "practica.py"]