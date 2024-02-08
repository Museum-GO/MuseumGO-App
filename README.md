# MuseumGo app

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

This is a simple app to find museums near you.

## Development guide

First, clone the repo:

```bash
git clone https://github.com/Museum-GO/MuseumGO-App.git
cd MuseumGO-App
```

### ArangoDB database

MuseumGo uses ArangoDB v3.11.5 as a database, you can install it locally or use a docker image.

### Backend

The backend is made with Python and requests / flask, it is based on a OpenAPI specification, check the [OpenAPI specification](./back/api.yaml) for more information.

#### Requirements

- Python v3.8
- pip v23.1.2
- A running ArangoDB instance

#### How to setup

```bash
cd back
pip install -r requirements.txt
```

#### Configuration

Fill the [config file](./back/config/config.ini) with your ArangoDB credentials.

#### Run the backend

```bash
python app.py
```

Check the SwaggerUI at [http://localhost:3000/api/ui](http://localhost:3000/api/ui)

[Testing guide](./back/tests/README.md)

#### Good practices

Check that your code is compliant with our linter Black:

```bash
black .
```

### Frontend

The frontend is made with VueJS.

#### Requirements

- NodeJS v19.0.0c
- npm v8.19.2

#### How to setup

```bash
cd front
npm install
```

#### Run the frontend

```bash
npm run serve
```

The frontend is now available by connecting to the backend URL at [http://localhost:3000](http://localhost:3000)

#### Good practices

Check that your code is compliant with our linter Prettier:

```bash
npm run prettier
```

Check that your code has no spelling mistakes:

```bash
npm run spellcheck
```

### Recommended development environment

- VSCode with extensions:
  - [Vetur](https://marketplace.visualstudio.com/items?itemName=octref.vetur)
  - [Black](https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext)
  - [Cspell](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
  - [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
  - [i18n Ally](https://marketplace.visualstudio.com/items?itemName=lokalise.i18n-ally)

## Deployment guide

### Requirements:

- Docker v24.0.5

### Local Docker deployment

Build the docker image:

```bash
docker build -t museumgo .
```

Run the docker image:

```bash
docker run -p 3000:3000 museumgo
```

The app is now available at [http://localhost:3000](http://localhost:3000)

Instead of using the `back/config/config.ini` file, you can use environment variables to configure the app:

```bash
docker run -p 3000:3000 \
  -e MUSEUMGO_ARANGODB_HOST=... \
  -e MUSEUMGO_ARANGODB_PORT=... \
  -e MUSEUMGO_ARANGODB_DATABASE=... \
  -e MUSEUMGO_ARANGODB_USER=...  \
  -e MUSEUMGO_ARANGODB_PASSWORD=... \
  museumgo
```

### Local Docker Compose deployment

You can use the `docker-compose.yml` file to deploy the app with a local ArangoDB instance. Edit the `docker-compose.yml` file to set your ArangoDB credentials and then run:

```bash
docker-compose up
```

The app is now available at [http://localhost:3000](http://localhost:3000)

To run the app in headless mode, use:

```bash
docker-compose up -d
```

To stop the app, use:

```bash
docker-compose down
```

### Continuous deployment

This app is deployed on [http://museumgo.tomansion.fr/](http://museumgo.tomansion.fr/) using a GitHub Actions workflow. The workflow is triggered when a new tag is pushed to the repository on the `main` branch.