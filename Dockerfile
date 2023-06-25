FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends\
    ffmpeg \
    build-essential \
    cmake \
    libswscale-dev \
    libjpeg-dev \
    libpng-dev \
    libavformat-dev \
    libpq-dev \
    wget && \
    pip install --upgrade pip setuptools wheel pybind11 --no-cache-dir && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install -r requirements.txt && \
    pip3 install dlib opencv-python --no-cache-dir

COPY . .

CMD ["python3", "main.py"]
