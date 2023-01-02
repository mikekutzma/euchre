# syntax=docker/dockerfile:1
FROM node:alpine as build-deps
WORKDIR /usr/src/app
COPY ./euchre-frontend/package.json ./euchre-frontend/package-lock.json ./
RUN npm install
COPY ./euchre-frontend/ ./
COPY ./.env.prod ./.env
RUN npm run build

# Nginx
FROM nginx:stable-alpine
COPY --from=build-deps /usr/src/app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
