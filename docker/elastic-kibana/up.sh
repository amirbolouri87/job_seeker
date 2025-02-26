#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  source .env
else
  echo ".env file not found. Please create it and define ELASTIC_PASSWORD and KIBANA_PASSWORD."
  exit 1
fi

# set DNS
read -p "Do you want to configure custom DNS? (y/n): " use_dns
if [ "$use_dns" == "y" ]; then
  read -p "Enter primary DNS: " dns1
  read -p "Enter secondary DNS (optional, press Enter to skip): " dns2

  echo "nameserver $dns1" > /etc/resolv.conf
  if [ -n "$dns2" ]; then
    echo "nameserver $dns2" >> /etc/resolv.conf
  fi
  echo "DNS has been configured."
fi

# mirror registry
read -p "Do you want to use a mirror registry? (y/n): " use_mirror
if [ "$use_mirror" == "y" ]; then
  read -p "Enter the mirror registry URL (e.g., docker.arvancloud.ir): " mirror_registry
else
  mirror_registry=""
fi

# Pull Elasticsearch image
if [ -z "$(docker images -q elasticsearch:8.16.3)" ]; then
  echo "Pulling Elasticsearch image..."
  if [ -n "$mirror_registry" ]; then
    docker pull "$mirror_registry/elasticsearch:8.16.3" &&
    docker tag "$mirror_registry/elasticsearch:8.16.3" elasticsearch:8.16.3 || {
      echo "Failed to pull Elasticsearch image. Exiting..."
      exit 1
    }
  else
    docker pull elasticsearch:8.16.4 || {
      echo "Failed to pull Elasticsearch image. Exiting..."
      exit 1
    }
  fi
fi

# Pull Kibana image
if [ -z "$(docker images -q kibana:8.16.3)" ]; then
  echo "Pulling Kibana image..."
  if [ -n "$mirror_registry" ]; then
    docker pull "$mirror_registry/kibana:8.16.3" &&
    docker tag "$mirror_registry/kibana:8.16.3" kibana:8.16.3 || {
      echo "Failed to pull Kibana image. Exiting..."
      exit 1
    }
  else
    docker pull kibana:8.16.3 || {
      echo "Failed to pull Kibana image. Exiting..."
      exit 1
    }
  fi
fi

# Start Elasticsearch and Kibana
echo "Starting Elasticsearch and Kibana..."
docker compose up -d

# Test connection to Elasticsearch
echo "Testing connection to Elasticsearch..."
curl -u "elastic:${ELASTIC_PASSWORD}" http://localhost:9200

echo "Setup completed"
