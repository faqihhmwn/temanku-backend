FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "===== LIST /app =====" && ls -la /app
RUN echo "===== LIST /app/models =====" && ls -la /app/models
RUN echo "===== PYTHONPATH =====" && python -c "import sys; print(sys.path)"
RUN echo "===== IMPORT TEST =====" && python -c "import models; print('models import OK')"

CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]