FROM node:8.1.4-slim

RUN npm install -g create-react-app && \
    create-react-app app && \
    cd app

WORKDIR "/app"

EXPOSE 3000

CMD ["yarn", "start"]
