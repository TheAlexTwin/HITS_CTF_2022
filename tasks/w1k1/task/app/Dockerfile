FROM node:14-alpine
MAINTAINER "Alexander Zorkin"

WORKDIR /app
COPY . ./

RUN apk add curl

RUN npm install wikit -g
RUN npm install --production

USER node
CMD ["npm", "start"]
