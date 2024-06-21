# Thumbnail Generation API

## Overview

The Thumbnail Generation API provides the service for generating thumbnails of morphologies/electrophysiologies and the soma of morphologies. The API is designed to receive a `content_url` from a BBP Nexus resource (morphology or electrophysiology) and produce a corresponding thumbnail image.

## Install

To get started with the Thumbnail Generation API, follow these simple steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/BlueBrain/thumbnail-generation-api.git
    cd thumbnail-generation-api
    ```

2. **Install [Poetry](https://python-poetry.org/docs/)**
    
3. **Install the dependencies:**
    ```sh
    poetry install
    ```

4. **Run the application:**
    ```sh
    poetry run uvicorn main:app --reload
    ```

Your Thumbnail Generation API should now be running at `http://127.0.0.1:8000`.

## Examples

Here are some simple examples to get you started with using the Thumbnail Generation API:

1. **Generate a thumbnail for electrophysiologies:**
    ```sh
    curl -X GET "http://127.0.0.1:8000/generate/trace-image?content_url=https://bbp.epfl.ch/nexus/v1/files/public/hippocampus/https%3A%2F%2Fbbp.epfl.ch%2Fneurosciencegraph%2Fdata%2Fb67a2aa6-d132-409b-8de5-49bb306bb251" -H "accept: application/json" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
    ```

2. **Generate a thumbnail for morphologies:**
    ```sh
    curl -X GET "http://127.0.0.1:8000/generate/morphology-image?content_url=https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118" -H "accept: application/json" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
    ```

For more detailed usage and examples, please refer to the visit `http://127.0.0.1:8000/docs`.


## Testing

Tests can be run using the following command:

```
pytest
```


## Acknowledgements

The development of this software was supported by funding to the Blue Brain Project, a research center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board of the Swiss Federal Institutes of Technology.

For license and authors, see LICENSE.txt and AUTHORS.txt respectively.

Copyright &copy; 2024 Blue Brain Project/EPFL