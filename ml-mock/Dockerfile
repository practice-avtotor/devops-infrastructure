FROM python:3.12-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY ml_mock.py .

CMD ["uvicorn", "ml_mock:app", "--host", "0.0.0.0", "--port", "5000"]
