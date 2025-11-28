# Dockerfile
FROM python:3.13-slim

# Configura variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Configura diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Instala dependências do sistema
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o projeto
COPY . /app/

# Exponha a porta
EXPOSE 8001

# Copia o script entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Define o entrypoint
ENTRYPOINT ["entrypoint.sh"]

# Executa o gunicorn (ou manage.py runserver para dev)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]