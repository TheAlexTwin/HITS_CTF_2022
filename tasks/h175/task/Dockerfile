FROM python:2-alpine
LABEL maintainer="Alexander Zorkin"

COPY ./app /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x run.sh main.py

ENTRYPOINT [ "sh", "run.sh" ]
