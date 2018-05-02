FROM python:3.6.5-alpine3.7

WORKDIR /src

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
