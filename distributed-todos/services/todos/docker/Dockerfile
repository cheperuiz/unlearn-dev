FROM python:3.8-slim-buster

ARG TZ=America/Los_Angeles
ARG USERNAME=python_user

RUN useradd --create-home $USERNAME
RUN echo Timezone: $TZ
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

RUN apt-get update \
    && apt-get install -y \
    ipython \
    && rm -rf /var/lib/apt/lists/*

COPY assets/ /
RUN pip install --upgrade --no-cache pip
RUN pip install -r requirements.txt --no-cache
