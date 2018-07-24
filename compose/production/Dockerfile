FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libcups2-dev python3-dev \
        python3-cups libmariadbclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# RUN mkdir /app
WORKDIR /app
# ADD . /app/

EXPOSE 80
EXPOSE 443