FROM python:3.10-slim

RUN apt update && apt install -y --no-install-recommends \
    build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["make", "run-server"]
