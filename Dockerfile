ARG PYTHON_VERSION=3.8.1

FROM python:${PYTHON_VERSION}-slim-buster

ENV PYTHONDONTWRITEBYTECODE=True

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && \
    apt-get install -y unixodbc-dev gcc g++ make --no-install-recommends && \
    SLUGIFY_USES_TEXT_UNIDECODE=yes pip install -r requirements.txt && \
    apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app

CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 manage:app
