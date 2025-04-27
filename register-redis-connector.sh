#!/bin/bash

# Wait for Kafka Connect to be ready
echo "Waiting for Kafka Connect to be ready..."
sleep 30

# Register the Redis Source connector
echo "Registering Redis Source connector..."
curl -X POST -H "Content-Type: application/json" --data @redis-source-connector.json http://localhost:8083/connectors

echo "Done!"
