# syntax=docker/dockerfile:1

# FROM python:3.8-slim-buster

# FROM osgeo/gdal:latest
FROM osgeo/gdal:ubuntu-small-3.6.2

RUN apt-get update -y && apt-get install python3-pip -y

WORKDIR /app

COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "-u", "app.py"]