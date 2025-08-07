#!/bin/bash
set -o

IMAGE_NAME="call518/mcpo-server"

# CUSTOM_TAG="${1:-latest}"
CUSTOM_TAG="1.0.3"

for TAG in ${CUSTOM_TAG} latest
do
    docker build -t ${IMAGE_NAME}:${TAG} .
done
