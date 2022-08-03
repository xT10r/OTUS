FROM python:buster

ENV PATH /home/trufflehog/.local/bin:$PATH

LABEL authors="HW-09" \
   description="Docker python image"

RUN apt-get update; \
    update-ca-certificates; \
    apt-get install -qq -y nano git \
    && apt-get install -qq -f \
    && apt-get clean; \
    rm -f /var/lib/apt/lists/* 2> /dev/null; \
    pip install --upgrade pip

RUN groupadd -g 2000 trufflehog; \
    useradd -rm -d /home/trufflehog -s /bin/bash -g trufflehog -u 2001 trufflehog

USER trufflehog

RUN pip install truffleHog -q --exists-action i

EXPOSE 8080