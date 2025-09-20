FROM python:3.9-slim

# Install ADB
RUN apt-get update && apt-get install -y --no-install-recommends android-tools-adb && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
