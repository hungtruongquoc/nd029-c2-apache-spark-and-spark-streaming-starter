from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, to_json, col, unbase64, base64, split, expr
from pyspark.sql.types import StructField, StructType, StringType, BooleanType, ArrayType, DateType, FloatType

# TO-DO: create a StructType for the Kafka redis-server topic which has all changes made to Redis - before Spark 3.0.0, schema inference is not automatic

# TO-DO: create a StructType for the Customer JSON that comes from Redis- before Spark 3.0.0, schema inference is not automatic

# TO-DO: create a StructType for the Kafka stedi-events topic which has the Customer Risk JSON that comes from Redis- before Spark 3.0.0, schema inference is not automatic

#TO-DO: create a spark application object

#TO-DO: set the spark log level to WARN

# TO-DO: using the spark application object, read a streaming dataframe from the Kafka topic redis-server as the source
# Be sure to specify the option that reads all the events from the topic including those that were published before you started the spark stream

# TO-DO: cast the value column in the streaming dataframe as a STRING 

# TO-DO:; parse the single column "value" with a json object in it, like this:
# +------------+
# | value      |
# +------------+
# |{"key":"Q3..|
# +------------+
#
# with this JSON format: {"key":"Q3VzdG9tZXI=",
# "existType":"NONE",
# "Ch":false,
# "Incr":false,
# "zSetEntries":[{
# "element":"eyJjdXN0b21lck5hbWUiOiJTYW0gVGVzdCIsImVtYWlsIjoic2FtLnRlc3RAdGVzdC5jb20iLCJwaG9uZSI6IjgwMTU1NTEyMTIiLCJiaXJ0aERheSI6IjIwMDEtMDEtMDMifQ==",
# "Score":0.0
# }],
# "zsetEntries":[{
# "element":"eyJjdXN0b21lck5hbWUiOiJTYW0gVGVzdCIsImVtYWlsIjoic2FtLnRlc3RAdGVzdC5jb20iLCJwaG9uZSI6IjgwMTU1NTEyMTIiLCJiaXJ0aERheSI6IjIwMDEtMDEtMDMifQ==",
# "score":0.0
# }]
# }
# 
# (Note: The Redis Source for Kafka has redundant fields zSetEntries and zsetentries, only one should be parsed)
#
# and create separated fields like this:
# +------------+-----+-----------+------------+---------+-----+-----+-----------------+
# |         key|value|expiredType|expiredValue|existType|   ch| incr|      zSetEntries|
# +------------+-----+-----------+------------+---------+-----+-----+-----------------+
# |U29ydGVkU2V0| null|       null|        null|     NONE|false|false|[[dGVzdDI=, 0.0]]|
# +------------+-----+-----------+------------+---------+-----+-----+-----------------+
#
# storing them in a temporary view called RedisSortedSet

# TO-DO: execute a sql statement against a temporary view, which statement takes the element field from the 0th element in the array of structs and create a column called encodedCustomer
# the reason we do it this way is that the syntax available select against a view is different than a dataframe, and it makes it easy to select the nth element of an array in a sql column

# TO-DO: take the encodedCustomer column which is base64 encoded at first like this:
# +--------------------+
# |            customer|
# +--------------------+
# |[7B 22 73 74 61 7...|
# +--------------------+

# and convert it to clear json like this:
# +--------------------+
# |            customer|
# +--------------------+
# |{"customerName":"...|
#+--------------------+
#
# with this JSON format: {"customerName":"Sam Test","email":"sam.test@test.com","phone":"8015551212","birthDay":"2001-01-03"}

# TO-DO: parse the JSON in the Customer record and store in a temporary view called CustomerRecords

# TO-DO: JSON parsing will set non-existent fields to null, so let's select just the fields we want, where they are not null as a new dataframe called emailAndBirthDayStreamingDF

# TO-DO: Split the birth year as a separate field from the birthday
# TO-DO: Select only the birth year and email fields as a new streaming data frame called emailAndBirthYearStreamingDF

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

# TO-DO: join the streaming dataframes on the email address to get the risk score and the birth year in the same dataframe

# TO-DO: sink the joined dataframes to a new kafka topic to send the data to the STEDI graph application 
# +--------------------+-----+--------------------+---------+
# |            customer|score|               email|birthYear|
# +--------------------+-----+--------------------+---------+
# |Santosh.Phillips@...| -0.5|Santosh.Phillips@...|     1960|
# |Sean.Howard@test.com| -3.0|Sean.Howard@test.com|     1958|
# |Suresh.Clark@test...| -5.0|Suresh.Clark@test...|     1956|
# |  Lyn.Davis@test.com| -4.0|  Lyn.Davis@test.com|     1955|
# |Sarah.Lincoln@tes...| -2.0|Sarah.Lincoln@tes...|     1959|
# |Sarah.Clark@test.com| -4.0|Sarah.Clark@test.com|     1957|
# +--------------------+-----+--------------------+---------+
#
# In this JSON Format {"customer":"Santosh.Fibonnaci@test.com","score":"28.5","email":"Santosh.Fibonnaci@test.com","birthYear":"1963"}

# Create StructType for the Kafka redis-server topic which has all changes made to Redis
redisMessageSchema = StructType(
    [
        StructField("key", StringType()),
        StructField("existType", StringType()),
        StructField("ch", BooleanType()),
        StructField("incr", BooleanType()),
        StructField("zSetEntries", ArrayType(
            StructType([
                StructField("element", StringType()),
                StructField("score", FloatType())
            ])
        ))
    ]
)

# Create StructType for the Customer JSON that comes from Redis
customerJSONSchema = StructType(
    [
        StructField("customerName", StringType()),
        StructField("email", StringType()),
        StructField("phone", StringType()),
        StructField("birthDay", StringType())
    ]
)

# Create StructType for the Kafka stedi-events topic which has the Customer Risk JSON
customerRiskSchema = StructType(
    [
        StructField("customer", StringType()),
        StructField("score", FloatType()),
        StructField("riskDate", StringType())
    ]
)

# Create a spark application object
spark = SparkSession.builder.appName("STEDI-Risk-Score-Join").getOrCreate()

# Set the spark log level to WARN
spark.sparkContext.setLogLevel("WARN")

#################################################
# Read the Redis Server Kafka Topic
#################################################

# Read a streaming dataframe from kafka redis-server topic
redisServerRawStreamingDF = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:19092") \
    .option("subscribe", "redis-server") \
    .option("startingOffsets", "earliest") \
    .load()

# Cast the value column in the streaming dataframe as a STRING
redisServerStreamingDF = redisServerRawStreamingDF.selectExpr("cast(key as string) key", "cast(value as string) value")

# Parse the single column "value" with a json object in it
redisServerStreamingDF.withColumn("value", from_json("value", redisMessageSchema)) \
    .select(col("value.*")) \
    .createOrReplaceTempView("RedisSortedSet")

# Execute a sql statement to get the customer data from Redis
encodedCustomerDF = spark.sql("SELECT key, zSetEntries[0].element as encodedCustomer FROM RedisSortedSet")

# Take the encodedCustomer column which is base64 encoded and convert to a string
decodedCustomerDF = encodedCustomerDF \
    .withColumn("customer", unbase64(encodedCustomerDF.encodedCustomer).cast("string"))

# Parse the JSON in the Customer record and store in a temporary view called CustomerRecords
decodedCustomerDF \
    .withColumn("customer", from_json("customer", customerJSONSchema)) \
    .select(col("customer.*")) \
    .createOrReplaceTempView("CustomerRecords")

# JSON parsing will set non-existent fields to null, so let's select just the fields we want
emailAndBirthDayStreamingDF = spark.sql("""
    SELECT email, birthDay 
    FROM CustomerRecords
    WHERE email IS NOT NULL AND birthDay IS NOT NULL
""")

# Split the birth year as a separate field from the birthday
emailAndBirthYearStreamingDF = emailAndBirthDayStreamingDF \
    .withColumn("birthYear", split(col("birthDay"), "-").getItem(0)) \
    .select("email", "birthYear")

#################################################
# Read the STEDI Events Kafka Topic
#################################################

# Read a streaming dataframe from Kafka stedi-events topic
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
stediEventsStreamingDF \
    .withColumn("value", from_json("value", customerRiskSchema)) \
    .select(col("value.*")) \
    .createOrReplaceTempView("CustomerRisk")

# Create a dataframe with customer and score from CustomerRisk
customerRiskStreamingDF = spark.sql("SELECT customer, score FROM CustomerRisk")

#################################################
# Join Dataframes
#################################################

# Join the streaming dataframes on the email address to get the risk score and birth year in the same dataframe
riskScoreByBirthYearStreamingDF = customerRiskStreamingDF \
    .join(emailAndBirthYearStreamingDF, expr("""
        customer = email
    """))

# Select the fields required in the final JSON
riskScoreByBirthYearStreamingDF = riskScoreByBirthYearStreamingDF \
    .select("customer", "score", "email", "birthYear")

# Create JSON from the joined dataframe
riskScoreByBirthYearJSON = riskScoreByBirthYearStreamingDF \
    .selectExpr("to_json(struct(*)) AS value") \
    .select("value")

# Write the joined dataframe to a new kafka topic
kafkaRiskScoreByBirthYearStreamingDF = riskScoreByBirthYearJSON \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:19092") \
    .option("topic", "customer-risk-topic") \
    .option("checkpointLocation", "/tmp/kafkacheckpoint") \
    .start()

# Keep the process running until terminated
kafkaRiskScoreByBirthYearStreamingDF.awaitTermination()