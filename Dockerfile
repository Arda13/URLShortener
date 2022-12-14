FROM python:3.8

# Environment variables
ENV HOST default_env
ENV ENV_PORT default_env

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT uvicorn api.main:app --host ${HOST} --port ${ENV_PORT}