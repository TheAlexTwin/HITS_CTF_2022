FROM ubuntu:latest

# ENV ENV PRODUCTION
ENV PYTHONUNBUFFERED 1

WORKDIR /app/src

RUN apt-get update && apt-get install -y firefox python3 curl
RUN apt-get install -y python3-pip

COPY src/requirements.txt ./
RUN pip3 install -r requirements.txt

COPY src /app/src

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "--workers", "3", "--log-level", "DEBUG", "wsgi:app" ]
