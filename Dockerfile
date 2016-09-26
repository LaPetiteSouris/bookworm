FROM python:3.5
MAINTAINER Tung Hoang


ENV INSTALL_PATH /bookworm
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH


COPY requirements.txt /tmp/requirements.txt
COPY . .

WORKDIR  "/bookworm"

RUN pip install -r /tmp/requirements.txt

CMD gunicorn -b 0.0.0.0:3000 --access-logfile - "api.wsgi:app"
