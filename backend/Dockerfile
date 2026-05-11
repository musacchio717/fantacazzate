FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "echo 'Starting migrations...' && alembic upgrade head && echo 'Migrations done, starting server...' && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]