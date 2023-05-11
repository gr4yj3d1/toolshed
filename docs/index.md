# Toolshed Documentation

## Introduction

This is the documentation for the Toolshed project. It is a work in progress.
`#social` `#network` `#federation` `#decentralized` `#federated` `#socialnetwork` `#fediverse` `#community` `#hashtags`

## Getting Started

## Installation

``` bash
 # TODO add installation instructions
 # similar to development instructions just with more docker
 # TODO add docker-compose.yml
```

## Development

``` bash
git clone https://github.com/gr4yj3d1/toolshed.git
```
or
``` bash
git clone https://git.neulandlabor.de/j3d1/toolshed.git
```

### Frontend

``` bash
cd toolshed/frontend
npm install
npm run dev
```

### Backend

``` bash
cd toolshed/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Docs

``` bash
cd toolshed/docs
mkdocs serve -a 0.0.0.0:8080
```
