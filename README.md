# Content creator API

A platform to create blog content and market research

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_PORT` : api listen port

`DB_PORT` : mongodb port

`DB_DATABASE`: mongodb database

`DB_USER` : mongodb user

`DB_PASSWORD` : mongodb password

`API_GATEWAY_IP` : XXX.XXX.X.X

## Tech Stack

FastApi, MongoDB

## Installation

### Requirements

Python 3.11.5 or highest

Pip 23.2.1 or highest

MongoDB server

### Development

1. Clone the project

2. (Optional) Create a python environment

```bash
  cd your_project_folder
  python -m venv /env
```

3. Start virtual environment

```bash
    cd your_project_folder/env/Scripts
    ./activate
    cd ../..
```

4. Install packages

```bash
  python -m pip install -r  requirements.txt
```

5. Run locally

```bash
    uvicorn main:app --reload
```

## TODOs

- [ ] Refactor: separate platforms from social sources
- [ ] Add "Posts"
- [ ] Implements authorization with API Gateway
- [ ] Create a queue of scrapes
- [ ] Create another instance to scrapes for no block api
- [ ] Add linkedin scraper
- [ ] Add tiktok scraper
- [ ] Add instagram scraper
- [ ] Add facebook scraper
- [ ] Add twitter scraper
- [ ] Add web scraper
- [ ] Add blog scraper
- [ ] Add rss reader
- [ ] Add SEO tools