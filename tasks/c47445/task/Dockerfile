FROM golang:alpine

# store flag here
RUN mkdir /secret
RUN chmod 777 /secret

WORKDIR /app
ADD . /app/

RUN go build -o main .
CMD ["/app/main"]