FROM python:3.7
WORKDIR /usr/src/fusa
COPY ./app ./app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt