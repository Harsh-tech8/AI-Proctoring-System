FROM python:3.11-slim
WORKDIR /app
COPY services/vision_worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/vision_worker/app ./app
CMD ["python", "-m", "app.worker"]
