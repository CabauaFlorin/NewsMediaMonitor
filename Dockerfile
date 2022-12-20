# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN python -m spacy download ro_core_news_md

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
