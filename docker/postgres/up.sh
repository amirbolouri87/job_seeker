#!/bin/bash

if [ -n "$(docker image -q postgres:17)" ]; then
  echo "postgres:17 already exists"
else
  docker pull docker.arvancloud.ir/postgres:17 &&
  echo "downloaded postgres:17 from arvancloud mirror registry"
  docker tag docker.arvancloud.ir/postgres:17 postgres:17
fi

docker compose up -d
