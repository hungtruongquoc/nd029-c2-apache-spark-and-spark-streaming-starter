#!/bin/bash

# Build the custom Docker image
docker build -t custom-kafka-connect-redis-source -f Dockerfile.redis-connect .
