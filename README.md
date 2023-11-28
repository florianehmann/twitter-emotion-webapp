# Twitter Emotion Analysis - Webapp

![Static Badge](https://img.shields.io/badge/project%20type-personal-blue)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/florianehmann/twitter-emotion-webapp)
![GitHub top language](https://img.shields.io/github/languages/top/florianehmann/twitter-emotion-webapp)
[![Pylint](https://github.com/florianehmann/twitter-emotion-webapp/actions/workflows/pylint.yml/badge.svg)](https://github.com/florianehmann/twitter-emotion-webapp/actions/workflows/pylint.yml)

Webapp Frontend for the [twitter-emotion](https://github.com/florianehmann/twitter-emotion) Project

## About

Flask-based webapp that gives users a convenient way to perform an emotion analysis on tweets.

## Running with Docker

To run this app with docker, you first need to build the image with

```bash
docker-compose build
```

After that, you can use en edited version of the `docker-compose.yml` file with a random secret and your API key to run the app with

```bash
docker-compose up
```

## Development

To get a working development version of the app, you first need to create a virtual environments with the required packages

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You also need to specify your URL and API token for the Huggingface Inference API. Create a file named `.env` in the root directory of the repository and insert the following lines

```
INFERENCE_API_URL=<inference-api-url>
INFERENCE_API_TOKEN=<your-api-token>
```

Beware, this file is ignored by git because it contains sensitive information, so you have to do this everytime you clone this repository.

After that, you can run your local instance with

```bash
flask run
```
