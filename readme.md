# Jina.ai Alternative Search Result Scraper with Markdown Output Using FastAPI, SearXNG, Browserless, and AI Integration

English | [中文版](README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Description

This project provides a powerful web scraping tool that fetches search results and converts them into Markdown format using FastAPI, SearXNG, and Browserless. It includes the capability to use proxies for web scraping and handles HTML content conversion to Markdown efficiently. Now featuring AI Integration for filtering search results. Alternatives include Jina.ai, FireCrawl AI, Exa AI, and 2markdown, offering various web scraping and search engine solutions for developers.

## Table of Contents
- [Jina.ai Alternative Search Result Scraper with Markdown Output Using FastAPI, SearXNG, Browserless, and AI Integration](#jinaai-alternative-search-result-scraper-with-markdown-output-using-fastapi-searxng-browserless-and-ai-integration)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Alternatives:](#alternatives)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Docker Setup](#docker-setup)
  - [Manual Setup](#manual-setup)
  - [Usage](#usage)
    - [Search Endpoint](#search-endpoint)
    - [Fetch URL Content](#fetch-url-content)
    - [Fetching Images](#fetching-images)
    - [Fetching Videos](#fetching-videos)
  - [Using Proxies](#using-proxies)
  - [Roadmap](#roadmap)
  - [Code Explanation](#code-explanation)
  - [License](#license)
  - [Author](#author)
  - [Contributing](#contributing)
  - [Acknowledgements](#acknowledgements)
  - [Star History](#star-history)

## Alternatives:

- [Jina.ai](https://jina.ai/): A powerful search engine for developers.
- [FireCrawl AI](https://firecrawl.dev/): A web scraping API for developers.
- [Exa AI](https://exa.ai/): A web scraping API for developers.
- [2markdown](https://2markdown.com/): A web scraping tool that converts HTML to Markdown.

## Features

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **SearXNG**: An open-source internet metasearch engine.
- **Browserless**: A web browser automation service.
- **Markdown Output**: Converts HTML content to Markdown format.
- **Proxy Support**: Utilizes proxies for secure and anonymous scraping.
- **AI Integration (Reranker AI)**: Filters search results using AI to provide the most relevant content.
- **YouTube Transcriptions**: Fetches YouTube video transcriptions.
- **Image and Video Search**: Fetches images and video results using SearXNG.

## Prerequisites

Ensure you have the following installed:

- Python 3.11
- Virtualenv
- Docker

## Docker Setup

You can use Docker to simplify the setup process. Follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/essamamdani/search-result-scraper-markdown.git
    cd search-result-scraper-markdown
    ```

2. **Run Docker Compose**:
    ```sh
    docker compose up --build
    ```

With this setup, if you change the `.env` or `main.py` file, you no longer need to restart Docker. Changes will be reloaded automatically.

## Manual Setup

Follow these steps for manual setup:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/essamamdani/search-result-scraper-markdown.git
    cd search-result-scraper-markdown
    ```

2. **Create and activate virtual environment**:
    ```sh
    virtualenv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a .env file** in the root directory with the following content:
    ```bash
    SEARXNG_URL=http://searxng:8080
    BROWSERLESS_URL=http://browserless:3000
    TOKEN=your_browserless_token_here  # Replace with your actual token
    # PROXY_PROTOCOL=http
    # PROXY_URL=your_proxy_url
    # PROXY_USERNAME=your_proxy_username
    # PROXY_PASSWORD=your_proxy_password
    # PROXY_PORT=your_proxy_port
    REQUEST_TIMEOUT=30

    # AI Integration for search result filter
    FILTER_SEARCH_RESULT_BY_AI=true
    AI_ENGINE=groq
    # GROQ
    GROQ_API_KEY=yours_groq_api_key_here
    GROQ_MODEL=llama3-8b-8192
    # OPENAI
    # OPENAI_API_KEY=your_openai_api_key_here
    # OPENAI_MODEL=gpt-3.5-turbo-0125
    ```

5. **Run Docker containers for SearXNG and Browserless**:
    ```sh
    ./run-services.sh
    ```

6. **Start the FastAPI application**:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

## Usage

### Search Endpoint

To perform a search query, send a GET request to the root endpoint `/` with the query parameters `q` (search query), `num_results` (number of results), and `format` (get response in JSON or by default in Markdown).

Example:
```sh
curl "http://localhost:8000/?q=python&num_results=5&format=json" # for JSON format
curl "http://localhost:8000/?q=python&num_results=5" # by default Markdown
```

### Fetch URL Content

To fetch and convert the content of a specific URL to Markdown, send a GET request to the `/r/{url:path}` endpoint.

Example:
```sh
curl "http://localhost:8000/r/https://example.com&format=json" # for JSON format
curl "http://localhost:8000/r/https://example.com" # by default Markdown
```

### Fetching Images

To fetch image search results, send a GET request to the `/images` endpoint with the query parameters `q` (search query) and `num_results` (number of results).

Example:
```sh
curl "http://localhost:8000/images?q=puppies&num_results=5"
```

### Fetching Videos

To fetch video search results, send a GET request to the `/videos` endpoint with the query parameters `q` (search query) and `num_results` (number of results).

Example:
```sh
curl "http://localhost:8000/videos?q=cooking+recipes&num_results=5"
```

## Using Proxies

This project uses Geonode proxies for web scraping. You can use [my Geonode affiliate link](https://geonode.com/invite/47389) to get started with their proxy services.

## Roadmap

- [x] **FastAPI**: A modern, fast web framework for building APIs with Python.
- [x] **SearXNG**: An open-source internet metasearch engine.
- [x] **Browserless**: A web browser automation service.
- [x] **Markdown Output**: Converts HTML content to Markdown format.
- [x] **Proxy Support**: Utilizes proxies for secure and anonymous scraping.
- [x] **AI Integration (Reranker AI)**: Filters search results using AI to provide the most relevant content.
- [x] **YouTube Transcriptions**: Fetches YouTube video transcriptions.
- [x] **Image and Video Search**: Fetches images and video results using SearXNG.

## Code Explanation

For a detailed explanation of the code, visit the article [here](https://www.essamamdani.com/articles/search-result-scraper-markdown).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Essa Mamdani - [essamamdani.com](https://essamamdani.com)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SearXNG](https://github.com/searxng/searxng)
- [Browserless](https://www.browserless.io/)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=essamamdani/search-result-scraper-markdown&type=Date)](https://star-history.com/#essamamdani/search-result-scraper-markdown&Date)