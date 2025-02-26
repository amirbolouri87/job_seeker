#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  source .env
else
  echo ".env file not found. Please create it and define ELASTIC_PASSWORD and KIBANA_PASSWORD."
  exit 1
fi

# Pull Elasticsearch and Kibana images if not already present
if [ -z "$(docker images -q elasticsearch:8.16.3)" ]; then
  echo "Pulling Elasticsearch image..."
  docker pull docker.arvancloud.ir/elasticsearch:8.16.3 &&
  docker tag docker.arvancloud.ir/elasticsearch:8.16.3 elasticsearch:8.16.3
fi

if [ -z "$(docker images -q kibana:8.16.3)" ]; then
  echo "Pulling Kibana image..."
  docker pull docker.arvancloud.ir/kibana:8.16.3 &&
  docker tag docker.arvancloud.ir/kibana:8.16.3 kibana:8.16.3
fi

# Start Elasticsearch and Kibana
echo "Starting Elasticsearch and Kibana..."
docker compose up -d

# Test connection to Elasticsearch
echo "Testing connection to Elasticsearch..."
curl -u "elastic:${ELASTIC_PASSWORD}" http://localhost:9200

echo "Setup completed"
