FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --default-timeout=100 --retries 10 -r requirements.txt
COPY . .
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]