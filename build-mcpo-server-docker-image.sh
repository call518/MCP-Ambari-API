#!/bin/bash
set -o

Dockerfile_PATH="./Dockerfile.for-OpenWebUI"
IMAGE_NAME="call518/mcpo-proxy"

# CUSTOM_TAG="${1:-latest}"
TAGs="
1.0.2
latest
"

for TAG in ${TAGs}
do
    docker build -t ${IMAGE_NAME}:${TAG} -f ${Dockerfile_PATH} .
done

echo

read -p "Do you want to push the images to Docker Hub? (y/N): " answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    for TAG in ${TAGs}
    do
        docker push ${IMAGE_NAME}:${TAG}
    done
fi