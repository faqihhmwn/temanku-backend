FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "===== FIND ROOT =====" && find /app -maxdepth 2 -type d -print | sort
RUN echo "===== FIND PY FILES =====" && find /app -maxdepth 2 -type f -name "*.py" -print | sort
RUN echo "===== CHECK MODELS PATH =====" && test -d /app/models && ls -la /app/models || true
RUN echo "===== CHECK MODELS IMPORT =====" && python -c "import os, sys; print(os.listdir('/app')); print(sys.path); import models; print('models OK')"

CMD ["sh", "-c", "python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]