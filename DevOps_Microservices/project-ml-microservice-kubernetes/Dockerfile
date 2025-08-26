FROM python:3.10-slim
WORKDIR /app

# keep builds small and quiet
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1

# deps first for better caching
COPY requirements.txt /app/requirements.txt

# Pin pip, use --no-cache-dir, and keep the hadolint ignore (as required)
# hadolint ignore=DL3013
RUN python -m pip install --no-cache-dir --upgrade "pip==24.2" \
 && python -m pip install --no-cache-dir --requirement requirements.txt

# app files
COPY app.py /app/app.py
COPY model_data /app/model_data

EXPOSE 80
CMD ["python", "app.py"]
