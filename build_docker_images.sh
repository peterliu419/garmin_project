#!/bin/bash

# Define variables for your GitHub username and repository
USERNAME="peterliu419"
REPO_NAME="garmin_project"

# Define image names and corresponding Dockerfiles
declare -A images=(
    ["producer-app"]="docker/Dockerfile.producer-app"
    ["producer-client"]="docker/Dockerfile.producer-client"
    ["consumer-app"]="docker/Dockerfile.consumer-app"
    ["consumer-client"]="docker/Dockerfile.consumer-client"
)

# Build each image
for image in "${!images[@]}"; do
    echo "Building image: $image"
    docker build -t "ghcr.io/$USERNAME/$REPO_NAME/$image:latest" -f "${images[$image]}" .
    if [ $? -ne 0 ]; then
        echo "Failed to build $image. Exiting..."
        exit 1
    fi
done

echo "All images built successfully!"