FROM python:3.11-slim

# install dependencies
RUN apt-get update && apt-get install -y \
    adb \
    libgl1-mesa-dev \
    # other dependencies (scrcpy if needed) \
    && apt-get clean

WORKDIR /app

COPY ./src /app/src
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "/app/src/main.py", "--todo", "/app/todo.md"]
