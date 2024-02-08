# Vuejs Frontend
FROM node:lts-alpine as build-stage
WORKDIR /front
COPY front/ .
RUN npm install
RUN npm run build

# Python Backend
FROM python:3.8-slim-buster
WORKDIR /back
COPY back/ .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY --from=build-stage /front/dist dist
ENV FLASK_ENV production
CMD ["python", "app.py"]