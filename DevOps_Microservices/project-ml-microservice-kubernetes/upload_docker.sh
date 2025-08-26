#!/usr/bin/env bash
# This file tags and uploads an image to Docker Hub
# Assumes that an image is built via `run_docker.sh`

set -euo pipefail

# ---- Config ----
IMAGE_NAME="house-prediction"
TAG="${1:-latest}"

# Set your Docker Hub username here or via env var DOCKERHUB_USERNAME
DOCKERHUB_USER="${DOCKERHUB_USERNAME:-rajat129}"

# Step 1:
# Create dockerpath
dockerpath="${DOCKERHUB_USER}/${IMAGE_NAME}"

# Step 2:
# Authenticate & tag
echo "Docker ID and Image: ${dockerpath}:${TAG}"
docker login -u "${DOCKERHUB_USER}"
docker tag "${IMAGE_NAME}:latest" "${dockerpath}:${TAG}"

# Step 3:
# Push image to a docker repository
docker push "${dockerpath}:${TAG}"

echo "✅ Pushed image: ${dockerpath}:${TAG}"
