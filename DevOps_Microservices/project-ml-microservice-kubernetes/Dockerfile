FROM python:3.10-slim

WORKDIR /app

# Copy source, model, requirements
COPY app.py /app/app.py
COPY model_data /app/model_data
COPY requirements.txt /app/requirements.txt

# Install deps
RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["python", "app.py"]
