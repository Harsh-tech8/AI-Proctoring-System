FROM python:3.11-slim
WORKDIR /app
COPY services/scoring_engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/scoring_engine/app ./app
CMD ["python", "-m", "app.worker"]
