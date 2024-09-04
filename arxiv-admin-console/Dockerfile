FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine AS production
COPY --from=build /app/build /usr/share/nginx/html
ARG AAA_URL
ARG ADMIN_API_BACKEND_URL
ARG ADMIN_APP_ROOT
ENV AAA_URL=$AAA_URL
ENV ADMIN_API_BACKEND_URL=$ADMIN_API_BACKEND_URL
ENV ADMIN_APP_ROOT=$ADMIN_APP_ROOT
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
