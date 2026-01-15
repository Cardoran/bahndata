FROM node:18-alpine

WORKDIR /usr/src/app

# Install dependencies required for native modules (if needed)
# RUN apk add --no-cache python3 make g++

COPY package.json .
RUN npm install

COPY . .

# EXPOSE 3000

CMD ["node", "server.js"]
