from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Step 1: Create Spark Session with MongoDB support
spark = SparkSession.builder \
    .appName("FileToMongoDB") \
    .config("spark.master", "local[*]") \
    .config("spark.hadoop.fs.native.lib", "false") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .config("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .config("spark.hadoop.fs.s3.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .config("spark.hadoop.fs.ftp.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.LocalFileSystem") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
    .config("spark.mongodb.write.connection.uri", "mongodb+srv://ayodeleahmed219:lCYJMzpIytIbyxNB@cluster0.8djhj.mongodb.net/reddit_db") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Step 2: Define the schema for the JSON files
schema = StructType([
    StructField("id", StringType(), True),
    StructField("body", StringType(), True),
    StructField("author", StringType(), True),
    StructField("created_utc", DoubleType(), True),
    StructField("subreddit", StringType(), True)
])

# Step 3: Define the input folder path
input_folder = "/opt/bitnami/spark/dataset"  

# Step 4: Read JSON files from the dataset folder as a stream
json_stream = spark.readStream \
    .schema(schema) \
    .json(input_folder)  

# Step 5: Write the stream to MongoDB
def write_to_mongo(df, epoch_id):
    print(f"Writing batch {epoch_id} to MongoDB...")
    df.write \
        .format("mongodb") \
        .mode("append") \
        .option("database", "reddit_db") \
        .option("collection", "comments") \
        .save()
    print(f"Batch {epoch_id} written successfully!")

# Step 6: Start streaming job to write to MongoDB
query = json_stream.writeStream \
    .foreachBatch(write_to_mongo) \
    .outputMode("append") \
    .start()

# Step 7: Await termination to keep the stream running
query.awaitTermination()
