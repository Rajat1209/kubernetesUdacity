#!/usr/bin/env bash
# Run the containerized app on a Kubernetes cluster and forward ports
set -euo pipefail

# Guard: kubectl installed
command -v kubectl >/dev/null || { echo "kubectl not found. Install it and ensure a cluster is running."; exit 1; }

# If no cluster is reachable, try to create a local kind cluster
if ! kubectl cluster-info >/dev/null 2>&1; then
  if command -v kind >/dev/null 2>&1; then
    echo "No Kubernetes context reachable. Creating kind cluster 'hp'..."
    kind get clusters | grep -q '^hp$' || kind create cluster --name hp --wait 180s
  else
    echo "No Kubernetes context reachable, and 'kind' not installed. Configure KUBECONFIG or install kind."; exit 1
  fi
fi

# Step 1: Docker path (must match your Docker Hub repo)
DOCKERHUB_USER="${DOCKERHUB_USERNAME:-rajat129}"
dockerpath="${DOCKERHUB_USER}/house-prediction"
echo "Docker ID and Image: ${dockerpath}"

app="house-prediction"

# Step 2: Run the Docker Hub container with kubernetes
kubectl delete pod "${app}" --ignore-not-found
kubectl run "${app}" \
  --image="${dockerpath}:latest" \
  --port=80 \
  --labels="app=${app}" \
  --restart=Never \
  --image-pull-policy=Always

# Step 3: List pods & wait for Ready
echo "Listing pods..."
kubectl get pods -o wide

echo "Waiting for pod to become Ready..."
kubectl wait --for=condition=Ready "pod/${app}" --timeout=180s || true
kubectl get pod "${app}" -o wide

# Step 4: Forward port 8000 -> 80
echo "Forwarding host 8000 -> pod 80 (Ctrl+C to stop)..."
kubectl port-forward "pod/${app}" 8000:80