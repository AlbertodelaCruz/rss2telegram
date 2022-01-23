FROM python:3.8

WORKDIR /usr/src/app
COPY requeriments.txt /usr/src/app/
COPY requeriments-dev.txt /usr/src/app/
RUN pip3 install -r requeriments.txt
RUN pip3 install -r requeriments-dev.txt