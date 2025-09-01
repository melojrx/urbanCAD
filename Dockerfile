FROM python:3.8-slim-bullseye

WORKDIR /app

# Instalar dependências do sistema necessárias para PostgreSQL e geoespacial
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    libgeos-dev \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 8009

# Comando para executar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8009", "--workers", "1", "--worker-class", "gevent", "wsgi:app"]