#!/bin/bash

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

# Pull Postgres image
if [ -z "$(docker images -q postgres:17)" ]; then
  echo "Pulling Elasticsearch image..."
  if [ -n "$mirror_registry" ]; then
    docker pull "$mirror_registry/postgres:17" &&
    docker tag "$mirror_registry/postgres:17" postgres:17 || {
      echo "Failed to pull Elasticsearch image. Exiting..."
      exit 1
    }
  else
    docker pull postgres:17 || {
      echo "Failed to pull Elasticsearch image. Exiting..."
      exit 1
    }
  fi
fi

docker compose up -d
