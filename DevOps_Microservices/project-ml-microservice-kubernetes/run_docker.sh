#!/usr/bin/env bash

## Complete the following steps to get Docker running locally

docker build --tag=house-prediction .
docker images
docker run -p 8000:80 house-prediction