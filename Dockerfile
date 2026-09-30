FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create runtime directories
RUN mkdir -p blockchain_ledger

# src/ on PYTHONPATH so all absolute imports work
ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["python", "-m", "main", "api"]
