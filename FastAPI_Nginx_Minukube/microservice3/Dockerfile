FROM python:3.9-slim
WORKDIR /app
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
