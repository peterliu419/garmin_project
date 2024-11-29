#!/bin/bash

# Define GitHub username and repository name as variables
GITHUB_USERNAME="peterliu419"
REPO_NAME="garmin_project"

# Define image names using the variables
PRODUCER_IMAGE="ghcr.io/$GITHUB_USERNAME/$REPO_NAME/producer-app:latest"
PRODUCER_CLIENT_IMAGE="ghcr.io/$GITHUB_USERNAME/$REPO_NAME/producer-client:latest"
CONSUMER_IMAGE="ghcr.io/$GITHUB_USERNAME/$REPO_NAME/consumer-app:latest"
CONSUMER_CLIENT_IMAGE="ghcr.io/$GITHUB_USERNAME/$REPO_NAME/consumer-client:latest"

# Define directories where the Dockerfiles are located
PRODUCER_DIR="./producer"
PRODUCER_CLIENT_DIR="./producer-client"
CONSUMER_DIR="./consumer"
CONSUMER_CLIENT_DIR="./consumer-client"

# Function to build and push Docker image
build_and_push() {
  local image_name=$1
  local build_dir=$2

  echo "Building image: $image_name"
  docker build -t "$image_name" "$build_dir"

  # Push the image to GitHub Container Registry
  echo "Pushing image: $image_name"
  docker push "$image_name"
}

# Build and push producer app
build_and_push "$PRODUCER_IMAGE" "$PRODUCER_DIR"

# Build and push producer client
build_and_push "$PRODUCER_CLIENT_IMAGE" "$PRODUCER_CLIENT_DIR"

# Build and push consumer app
build_and_push "$CONSUMER_IMAGE" "$CONSUMER_DIR"

# Build and push consumer client
build_and_push "$CONSUMER_CLIENT_IMAGE" "$CONSUMER_CLIENT_DIR"

echo "All images have been built and pushed successfully!"