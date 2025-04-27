#!/bin/bash

# Set Java system property to disable FAIL_ON_EMPTY_BEANS
export KAFKA_OPTS="$KAFKA_OPTS -Dcom.fasterxml.jackson.databind.SerializationFeature.FAIL_ON_EMPTY_BEANS=false"

# Print the Java options for debugging
echo "KAFKA_OPTS: $KAFKA_OPTS"

# Run the original entrypoint
exec /etc/confluent/docker/run
