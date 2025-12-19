# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Instalamos las dependencias del sistema para WeasyPrint
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar archivos e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto que usa Flask
EXPOSE 5000

# Comando para ejecutar con Gunicorn (más seguro que flask run)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
