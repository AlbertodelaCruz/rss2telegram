FROM python:3.8

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
COPY requirements-dev.txt /usr/src/app/
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt
