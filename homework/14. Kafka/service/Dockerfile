FROM node:18

WORKDIR /app
COPY package.json service.js ./
RUN npm install

CMD ["node", "service.js"]