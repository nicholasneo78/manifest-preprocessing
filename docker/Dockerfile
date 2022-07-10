ARG BASE_CONTAINER=python:3.8.13-slim-buster
FROM $BASE_CONTAINER

USER root

COPY requirements.txt .

ENV TZ=Asia/Singapore
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

#Downloading dependencies 
RUN apt-get update \
&& apt-get upgrade -y \
&& apt-get install -y \
&& apt-get -y install apt-utils gcc libpq-dev libsndfile1 ffmpeg python3-pandas

#Installing dependencies
RUN pip install -r requirements.txt

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
WORKDIR /manifest_preprocessing