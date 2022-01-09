FROM python:3.9.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUBUFFERED=1

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt-get update && apt-get install -y ffmpeg libavcodec-extra
RUN apt install aria2 -y