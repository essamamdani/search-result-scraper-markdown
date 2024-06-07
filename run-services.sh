#!/bin/bash

# Run SearXNG
docker run -d --name searxng -p 8888:8888 -v ./searxng:/etc/searxng:rw searxng/searxng

# Run Browserless
docker run -d --name browserless -p 3000:3000 browserless/chrome

echo "SearXNG is running at http://localhost:8888"
echo "Browserless is running at http://localhost:3000"
