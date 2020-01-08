ARG PYTHON_VERSION=3.8.1

FROM python:${PYTHON_VERSION}-slim-buster

ENV PYTHONDONTWRITEBYTECODE=True

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && \
 apt-get install -y g++ libc-dev unixodbc-dev curl gnupg2 apt-transport-https

# adding custom MS repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers and tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

RUN apt-get update && \
    apt-get install -y gcc g++ make --no-install-recommends && \
    pip install -r requirements.txt && \
    apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app

CMD gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:8000 manage:app
