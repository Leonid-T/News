FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt-get update && apt install -y netcat

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./news ./news

WORKDIR ./news
ENTRYPOINT ["/usr/src/app/news/entrypoint.sh"]