
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm install -g vite

CMD ["npm", "run", "dev"]
