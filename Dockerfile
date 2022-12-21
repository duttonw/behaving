FROM python:3.10-bullseye
# ARG VERSION=99.0.0

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8

RUN \
    echo "deb https://deb.nodesource.com/node_18.x bullseye main" > /etc/apt/sources.list.d/nodesource.list && \
    wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - && \
    apt-get update && \
    apt-get upgrade -yqq && \
    apt-get install -yqq nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install gherkin-lint
RUN npm install -g gherkin-lint

# Do not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Do not ever buffer console output
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
RUN pip install supervisor

COPY poetry.lock pyproject.toml README.md .flake8 config/supervisord.conf .gherkin-lintrc /app/
COPY src /app/src/
RUN mkdir /app/var && mkdir /app/var/log && mkdir /app/var/mail && mkdir /app/var/sms && mkdir /app/var/gcm && mkdir /app/var/downloads

WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install
RUN useradd -ms /bin/bash behaving
RUN chown -R behaving /app
USER behaving


ENTRYPOINT [ "supervisord" ]
