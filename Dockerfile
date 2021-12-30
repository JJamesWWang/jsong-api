FROM python:3.9.9-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra
COPY . /code/