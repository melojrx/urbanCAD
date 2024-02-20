FROM python:3.8.10

WORKDIR /home/ubuntu/maceio-server-cyro/urbanCAD

# Copie os arquivos de requirements.txt
COPY requirements.txt .

#RUN python -m venv venv
#ERUN /bin/bash -c "source venv/bin/activate"

# Instale as dependências dentro da venv
#RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código
COPY . .
#COPY app/static/ /home/ubuntu/maceio-server-cyro/urbanCAD/app/static/


CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8009", "wsgi:app"]
# CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8009", "wsgi:app"]