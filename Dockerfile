FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  python3 python3-pip wget gnupg ca-certificates && \
  rm -rf /var/lib/apt/lists/*


RUN wget -O - http://download.sgjp.pl/apt/sgjp.gpg.key | apt-key add - && \
  echo "deb http://download.sgjp.pl/apt/ubuntu jammy main" > /etc/apt/sources.list.d/sgjp.list && \
  apt-get update && \
  apt-get install -y --no-install-recommends morfeusz2 python3-morfeusz2 && \
  rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt


COPY . .

ENV PYTHONPATH=/app

ENTRYPOINT ["python3", "src/main.py"]
