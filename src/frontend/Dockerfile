FROM node:20-alpine

WORKDIR /app

COPY package.json yarn.lock ./

COPY tsconfig*.json ./

RUN yarn install

COPY . .

EXPOSE 3000

ENTRYPOINT ["sh", "-c", "yarn build && yarn start"]