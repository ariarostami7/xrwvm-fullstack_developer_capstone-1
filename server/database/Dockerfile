FROM node:18.12.1-bullseye-slim

RUN npm install -g npm@9.1.3


# Install necessary dependencies including Netcat
RUN apt-get update && apt-get install -y netcat

ADD package.json .
ADD app.js .
ADD review.js .
ADD dealership.js .
ADD data/dealerships.json .
ADD data/reviews.json .
COPY . .
RUN npm install

EXPOSE 3030

#CMD [ "node", "app.js" ]


# Start the server
CMD ["sh", "-c", "until nc -z mongo_db 27017; do echo 'Waiting for MongoDB...'; sleep 5; done && node app.js"]


# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./