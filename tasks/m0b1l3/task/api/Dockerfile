FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "server.py" ]