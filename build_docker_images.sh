#!/bin/bash

# Variables for your GitHub username and repository
USERNAME="peterliu419"
REPO_NAME="garmin_project"

# Parallel arrays for image names and their corresponding Dockerfiles
IMAGES=("producer-app" "producer-client" "consumer-app" "consumer-client")
DOCKERFILES=("docker/Dockerfile.producer-app" "docker/Dockerfile.producer-client" "docker/Dockerfile.consumer-app" "docker/Dockerfile.consumer-client")

# Iterate through the arrays
for ((i=0; i<${#IMAGES[@]}; i++)); do
    IMAGE="${IMAGES[$i]}"
    DOCKERFILE="${DOCKERFILES[$i]}"
    echo "Building image: $IMAGE"
    docker build -t "ghcr.io/$USERNAME/$REPO_NAME/$IMAGE:latest" -f "$DOCKERFILE" .
    if [ $? -ne 0 ]; then
        echo "Failed to build $IMAGE. Exiting..."
        exit 1
    fi
done

echo "All images built successfully!"
