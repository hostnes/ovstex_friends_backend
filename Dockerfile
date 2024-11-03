FROM python:3.9

RUN mkdir /project
WORKDIR /project

COPY . /project

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt
