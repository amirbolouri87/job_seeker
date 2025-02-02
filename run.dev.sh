#!/bin/bash
##############################################################
# ScriptName:        running job seeker in development       #
# Version:           1.0.0                                   #
##############################################################
read -p "enter image tag: " IMG_TAG
IMAGE_NAME="job_seeker_dev"
IMAGE="${IMAGE_NAME}:${IMG_TAG}"

if docker images | grep -q "${IMAGE_NAME}\s*${IMG_TAG}"; then
    echo "image ${IMAGE_NAME}:${IMG_TAG} already exists"
else
    echo "building image ${IMAGE_NAME}:${IMG_TAG} ..." &&
    docker build --build-arg requirement_file=local.txt --no-cache -t "${IMAGE}" -f Dockerfile .
fi

TAG_NAME="${IMG_TAG}" docker compose --file development-docker-compose.yml up -d