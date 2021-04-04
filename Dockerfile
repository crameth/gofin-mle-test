# pull official base image
FROM python:3.6.10-slim

# set environment variables
ENV TZ Asia/Singapore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src

# copy scripts
COPY ./api/requirements.txt /usr/src/requirements.txt

# install dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

# copy source
COPY ./api /usr/src

ENTRYPOINT ["bash", "entrypoint.sh"]
