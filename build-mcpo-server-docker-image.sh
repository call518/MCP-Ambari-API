#!/bin/bash
set -o

IMAGE_NAME="call518/mcpo-proxy"

# CUSTOM_TAG="${1:-latest}"
CUSTOM_TAG="1.0.1"

for TAG in ${CUSTOM_TAG} latest
do
    docker build -t ${IMAGE_NAME}:${TAG} .
done
