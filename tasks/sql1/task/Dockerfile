FROM php:7
RUN docker-php-ext-install mysqli

WORKDIR /app
COPY . /app

CMD [ "php", "-S", "0.0.0.0:8000" ]
EXPOSE 8000

