#!/bin/bash

if [ -n "$(docker image -q elasticsearch:8.16.3)" ]; then
  echo "elasticsearch:8.16.3 already exists"
else
  docker pull docker.arvancloud.ir/elasticsearch:8.16.3 &&
  echo "downloaded elasticsearch:8.16.3 from arvancloud mirror registry"
  docker tag docker.arvancloud.ir/elasticsearch:8.16.3 elasticsearch:8.16.3
fi

if [ -n "$(docker images -q kibana:8.16.3)" ]; then
    echo "kibana:8.16.3 already exists"
else
    docker pull docker.arvancloud.ir/kibana:8.16.3 &&
    echo "downloaded kibana:8.16.3 from arvancloud mirror registry" &&
    docker tag docker.arvancloud.ir/kibana:8.16.3 kibana:8.16.3
fi

docker compose up -d
