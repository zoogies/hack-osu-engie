FROM node:lts-alpine

WORKDIR /src/frontend

COPY . .
RUN cd engie && yarn install
RUN cd engie && yarn build

CMD ["node","engie/build/index.js"]