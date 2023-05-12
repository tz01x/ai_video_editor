From python:3.10.11-slim-bullseye

WORKDIR app

RUN apt update && apt upgrade -y
RUN apt install ffmpeg -y

COPY requirements.txt .
RUN pip install -r requirements.txt

