ARG PYTHON_VERSION=3.7

FROM python:${PYTHON_VERSION}-slim-buster

ENV PYTHONDONTWRITEBYTECODE=True

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY . /usr/src/app

CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 manage:app
