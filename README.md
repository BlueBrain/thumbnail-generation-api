# Thumbnail Generation API

## Installation

Navigate under `/api` and run `pip install -r requirements.txt`.

## Environment Variables

- `DEBUG_MODE` Sets whether FastAPI will run with debug mode ON (default: `False`)
- `WHITELISTED_CORS_URLS` Sets the list of whitelisted CORS URLs in a comma-separated string eg. `http://localhost:3000,https://my-website.com`

## Start

```
python -m uvicorn api.main:app
```

## Test

Test Content URLs

- Trace: `"https://bbp.epfl.ch/nexus/v1/files/public/hippocampus/https%3A%2F%2Fbbp.epfl.ch%2Fneurosciencegraph%2Fdata%2Fb67a2aa6-d132-409b-8de5-49bb306bb251"`
- Morphology: `"https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118"`
