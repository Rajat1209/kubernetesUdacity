FROM python:3.10-slim

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1

# Copy source, model, requirements
COPY app.py /app/app.py
COPY model_data /app/model_data
COPY requirements.txt /app/requirements.txt

# Install deps
RUN python -m pip install --no-cache-dir --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["python", "app.py"]
