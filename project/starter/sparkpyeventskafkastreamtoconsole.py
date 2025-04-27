from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, unbase64, base64, split
from pyspark.sql.types import StructField, StructType, StringType, BooleanType, ArrayType, DateType, FloatType

# TO-DO: using the spark application object, read a streaming dataframe from the Kafka topic stedi-events as the source
# Be sure to specify the option that reads all the events from the topic including those that were published before you started the spark stream
                                   
# TO-DO: cast the value column in the streaming dataframe as a STRING 

# TO-DO: parse the JSON from the single column "value" with a json object in it, like this:
# +------------+
# | value      |
# +------------+
# |{"custom"...|
# +------------+
#
# and create separated fields like this:
# +------------+-----+-----------+
# |    customer|score| riskDate  |
# +------------+-----+-----------+
# |"sam@tes"...| -1.4| 2020-09...|
# +------------+-----+-----------+
#
# storing them in a temporary view called CustomerRisk
# TO-DO: execute a sql statement against a temporary view, selecting the customer and the score from the temporary view, creating a dataframe called customerRiskStreamingDF
# TO-DO: sink the customerRiskStreamingDF dataframe to the console in append mode
# 
# It should output like this:
#
# +--------------------+-----
# |customer           |score|
# +--------------------+-----+
# |Spencer.Davis@tes...| 8.0|
# +--------------------+-----
# Run the python script by running the command from the terminal:
# /home/workspace/submit-event-kafka-streaming.sh
# Verify the data looks correct

# Create a StructType for the Kafka stedi-events topic which has the Customer Risk JSON
customerRiskSchema = StructType(
    [
        StructField("customer", StringType()),
        StructField("score", FloatType()),
        StructField("riskDate", StringType())
    ]
)

# Create a spark application object
spark = SparkSession.builder.appName("STEDI-Risk-Stream-Console").getOrCreate()

# Set the spark log level to WARN
spark.sparkContext.setLogLevel("WARN")

# Using the spark application object, read a streaming dataframe from the Kafka topic stedi-events as the source
stediEventsRawStreamingDF = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:19092") \
    .option("subscribe", "stedi-events") \
    .option("startingOffsets", "earliest") \
    .load()

# Cast the value column in the streaming dataframe as a STRING
stediEventsStreamingDF = stediEventsRawStreamingDF.selectExpr("cast(key as string) key", "cast(value as string) value")

# Parse the JSON from the single column "value"
parsedStediEventsStreamingDF = stediEventsStreamingDF \
    .withColumn("value", from_json("value", customerRiskSchema)) \
    .select(col("value.*"))

# Create a temporary view called CustomerRisk
parsedStediEventsStreamingDF.createOrReplaceTempView("CustomerRisk")

# Execute a sql statement against a temporary view, selecting the customer and the score from the temporary view
customerRiskStreamingDF = spark.sql("SELECT customer, score FROM CustomerRisk")

# Sink the customerRiskStreamingDF dataframe to the console in append mode
customerRiskStreamingDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start() \
    .awaitTermination()