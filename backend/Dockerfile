FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "echo 'STEP 1' && alembic upgrade head && echo 'STEP 2' && python3 -c 'from app.main import app; print(\"STEP 3\")' && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]