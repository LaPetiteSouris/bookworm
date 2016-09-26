FROM python:3.5
MAINTAINER Tung Hoang

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD [python]