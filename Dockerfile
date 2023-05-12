FROM python:3.8-slim-buster

WORKDIR /app

RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y

RUN pip install torch>=1.8.1

COPY requirements.txt .
RUN pip install -r requirements.txt