FROM python:3.14-slim

ENV DEBIAN_FRONTEND=noninteractive

COPY ./requirements.txt /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        libpq-dev \
        curl \ 
        tzdata && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/* /tmp && \
    adduser --disabled-password --no-create-home django-user && \
    ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata 

ENV PATH="/py/bin:$PATH"
ENV TZ=America/Sao_Paulo

USER django-user