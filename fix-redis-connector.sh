#!/bin/bash

# This script directly modifies the Redis Source Connector JAR file to fix the Jackson serialization issue

# Stop the containers
docker-compose down

# Create a temporary directory
mkdir -p temp_fix

# Copy the Redis Source Connector JAR file from the Docker image
docker run --rm -v $(pwd)/temp_fix:/tmp gcr.io/simulation-images/kafka-connect-redis-source cp /usr/share/java/kafka-connect-redis-source/kafka-connect-redis-1.0-SNAPSHOT.jar /tmp/

# Extract the JAR file
cd temp_fix
mkdir -p extracted
cd extracted
jar xf ../kafka-connect-redis-1.0-SNAPSHOT.jar

# Create a patch for the RedisSourceTask.java file
cat > RedisSourceTask.patch << 'EOF'
--- org/apache/kafka/connect/redis/RedisSourceTask.java.orig
+++ org/apache/kafka/connect/redis/RedisSourceTask.java
@@ -96,7 +96,9 @@
     private SourceRecord getSourceRecord(Event event) {
         try {
             ObjectMapper mapper = new ObjectMapper();
+            mapper.disable(SerializationFeature.FAIL_ON_EMPTY_BEANS);
             String json = mapper.writeValueAsString(event);
+            
             return new SourceRecord(
                     Collections.singletonMap("redis", "server"),
                     Collections.singletonMap("offset", 0),
EOF

# Apply the patch
patch -p0 < RedisSourceTask.patch

# Recompile the class
javac -cp .:../kafka-connect-redis-1.0-SNAPSHOT.jar org/apache/kafka/connect/redis/RedisSourceTask.java

# Update the JAR file
jar uf ../kafka-connect-redis-1.0-SNAPSHOT.jar org/apache/kafka/connect/redis/RedisSourceTask.class

# Copy the modified JAR file back to the host
cd ..
cp kafka-connect-redis-1.0-SNAPSHOT.jar ..

# Clean up
cd ..
rm -rf temp_fix

echo "Redis Source Connector JAR file has been patched."
echo "Now you can start the containers with docker-compose up"
