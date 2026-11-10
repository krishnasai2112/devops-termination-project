FROM python:3.11-slim

WORKDIR /app

# Install available Debian security updates
RUN apt-get update \
    && apt-get install --only-upgrade -y zlib1g \
    && rm -rf /var/lib/apt/lists/*

# Update Python packaging tools
RUN python -m pip install --no-cache-dir --upgrade setuptools wheel

COPY app/requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
