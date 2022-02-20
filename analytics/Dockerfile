#Deriving the latest base image
FROM node:latest

WORKDIR /analytics

COPY . .

RUN npm install mysql2 \
    && npm install mongodb 

CMD [ "node", "./analytics.js"]
