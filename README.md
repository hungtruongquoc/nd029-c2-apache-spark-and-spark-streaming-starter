# Windows Users
It is HIGHLY recommended to install the 10 October 2020 Update: https://support.microsoft.com/en-us/windows/get-the-windows-10-october-2020-update-7d20e88c-0568-483a-37bc-c3885390d212

You will then want to install the latest version of Docker on Windows: https://docs.docker.com/docker-for-windows/install/



#  Using Docker for your Exercises

You will need to use Docker to run the exercises on your own computer. You can find Docker for your operating system here: https://docs.docker.com/get-docker/

It is recommended that you configure Docker to allow it to use up to 2 cores and 6 GB of your host memory for use by the course workspace. If you are running other processes using Docker simultaneously with the workspace, you should take that into account also.



The docker-compose file at the root of the repository creates 9 separate containers:

- Redis
- Zookeeper (for Kafka)
- Kafka
- Banking Simulation
- Trucking Simulation
- STEDI (Application used in Final Project)
- Kafka Connect with Redis Source Connector
- Spark Master
- Spark Worker

It also mounts your repository folder to the Spark Master and Spark Worker containers as a volume  `/home/workspace`, making your code changes instantly available within to the containers running Spark.

Let's get these containers started!

```
cd [repositoryfolder]
docker-compose up
```

You should see 9 containers when you run this command:
```
docker ps
```

## Spark Logging Fix

* We modified the docker-compose.yaml file to add a new volume mount that maps your local spark/logs/ directory to /opt/bitnami/spark/logs/ inside the Spark containers.
* We created a custom log4j.properties file in the spark/logs/ directory to explicitly configure Spark to write logs to a file.
* We added a new environment variable SPARK_DAEMON_JAVA_OPTS to the Spark containers to use our custom log4j.properties file.
* We restarted the Spark containers to apply these changes.
* Now you can see the Spark logs in your local filesystem, which makes it easier to debug and monitor your Spark applications. The logs will be written to the spark/logs/spark.log file, and you can view them using standard tools like cat, head, tail, etc.

## Connector Container Failing

The fix addresses the Jackson serialization issue by:

Adding the environment variable CONNECT_JACKSON_SERIALIZATION_FEATURE_FAIL_ON_EMPTY_BEANS: "false" to the Kafka Connect container, which disables the Jackson feature that was causing the error.

Creating a custom connector configuration file that explicitly sets the serialization settings.

Mounting the configuration file into the container.

Adding a volume for logs to help with debugging if needed.