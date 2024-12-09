<h1>Reddit Data Pipeline with Kafka, Spark, and MongoDB</h1>
    <p>This project implements a data pipeline that streams Reddit comments from the 'Politics' subreddit, processes the data using Kafka and Apache Spark, and stores the results in MongoDB. The architecture is designed for real-time data collection and processing.</p>
    
  <h2>Architecture Overview</h2>
    <ol>
        <li><strong>Reddit Stream:</strong> Streams comments from the 'Politics' subreddit using the PRAW (Python Reddit API Wrapper).</li>
        <li><strong>Kafka:</strong> Acts as the message broker for decoupling the Reddit data producer and consumer.</li>
        <li><strong>Spark:</strong> Reads messages from Kafka, processes them, and writes them to MongoDB.</li>
        <li><strong>MongoDB:</strong> Stores the processed data in the `reddit_db` database and `comments` collection.</li>
    </ol>
    
   <h2>Prerequisites</h2>
    <h3>System Requirements</h3>
    <ul>
        <li><strong>Python 3.x</strong></li>
        <li><strong>Apache Kafka</strong> (Local or remote setup)</li>
        <li><strong>Apache Spark 3.x</strong> with MongoDB Spark Connector</li>
        <li><strong>MongoDB</strong> (MongoDB Atlas or local instance)</li>
    </ul>
    
  <h3>Libraries/Dependencies</h3>
    <p>The following Python libraries are required:</p>
    <ul>
        <li><code>praw</code>: Python Reddit API Wrapper</li>
        <li><code>confluent_kafka</code>: Kafka producer and consumer client</li>
        <li><code>pyspark</code>: Apache Spark for streaming and data processing</li>
        <li><code>pymongo</code>: MongoDB driver for Python</li>
        <li><code>json</code>: For working with JSON data</li>
    </ul>
    <p>To install the dependencies, run:</p>
    <pre><code>pip install praw confluent_kafka pyspark pymongo</code></pre>
    
  <h3>Kafka Setup</h3>
    <ol>
        <li>Set up a Kafka cluster locally or use a managed Kafka service.</li>
        <li>Make sure Kafka is running and accessible. The default broker address in the code is <code>kafka:9092</code>.</li>
    </ol>
    
   <h3>MongoDB Setup</h3>
    <ol>
        <li>Use MongoDB Atlas or a local MongoDB instance.</li>
        <li>Set up a database (<code>reddit_db</code>) and a collection (<code>comments</code>).</li>
        <li>Update the MongoDB URI in the Spark configuration to connect to your MongoDB instance.</li>
    </ol>
    
  <h2>Configuration</h2>
    <h3>Constants File (<code>constant.py</code>)</h3>
    <p>Create a file named <code>constant.py</code> in the project directory and define the following constants:</p>
    <pre><code>
# constant.py
client_id = 'your_reddit_client_id'
client_secret = 'your_reddit_client_secret'
user_agent = 'your_user_agent'
    </code></pre>
    
  <h3>Kafka Configuration</h3>
    <p>The Kafka producer configuration is set in the code to connect to <code>kafka:9092</code> by default. Update the configuration if using a different Kafka broker:</p>
    <pre><code>
# Producer configuration
producer_config = {
    'bootstrap.servers': 'kafka:9092',
}
    </code></pre>
    
  <h3>MongoDB Configuration in Spark</h3>
    <p>Update the MongoDB URI in the Spark session configuration:</p>
    <pre><code>
spark = SparkSession.builder \
    .appName("FileToMongoDB") \
    .config("spark.mongodb.write.connection.uri", "mongodb+srv://<username>:<password>@cluster0.mongodb.net/reddit_db") \
    .getOrCreate()
    </code></pre>
    
  <h2>How the Pipeline Works</h2>
    <h3>Step 1: Reddit Stream (Producer)</h3>
    <p>The producer script uses PRAW to stream comments from the <code>Politics</code> subreddit:</p>
    <ul>
        <li>Continuously fetches new comments from the subreddit.</li>
        <li>Each comment is serialized to JSON format and sent to the Kafka <code>REDDIT_TOPIC</code> topic.</li>
    </ul>
  
  <h3>Step 2: Kafka Consumer</h3>
    <p>The consumer reads the comments from the Kafka topic:</p>
    <ul>
        <li>Polls messages from the <code>REDDIT_TOPIC</code> topic.</li>
        <li>Each message is deserialized, and the comment data is stored in a file (<code>output.jsonl</code>).</li>
    </ul>
    
  <h3>Step 3: Spark Streaming</h3>
    <p>Spark reads the <code>output.jsonl</code> file in real-time:</p>
    <ul>
        <li>Processes the data according to the schema defined in the code.</li>
        <li>Writes the processed data to MongoDB using the MongoDB Spark Connector.</li>
    </ul>
    
  <h3>Step 4: MongoDB Storage</h3>
    <p>The comments are stored in the <code>comments</code> collection in the <code>reddit_db</code> database.</p>
    
  <h2>Running the Project</h2>
    <h3>1. Run the Reddit Stream Producer</h3>
    <p>Run the script that streams comments from Reddit and sends them to Kafka:</p>
    <pre><code>python reddit_producer.py</code></pre>
    
  <h3>2. Run the Kafka Consumer</h3>
    <p>Run the consumer to read from Kafka and save the comments to a local file:</p>
    <pre><code>python kafka_consumer.py</code></pre>
    
  <h3>3. Run Spark Streaming</h3>
    <p>Run the Spark streaming job to process the data and store it in MongoDB:</p>
    <pre><code>python spark_streaming.py</code></pre>
    
  <h2>Directory Structure</h2>
    <pre><code>
.
├── constant.py               # Configuration for Reddit API
├── kafka_consumer.py         # Kafka consumer to read messages
├── reddit_producer.py        # Reddit producer to fetch comments
├── spark_streaming.py        # Spark streaming job to process and save data
└── dataset/                  # Folder where consumer saves data (output.jsonl)
    </code></pre>
    
  <h2>Expected Output</h2>
    <p>Once the pipeline is running, comments from the 'Politics' subreddit will be continuously streamed, processed, and stored in MongoDB. You can verify the data by querying the <code>reddit_db</code> database, <code>comments</code> collection in MongoDB.</p>
    <pre><code>db.comments.find().pretty()</code></pre>
    
  <h2>Troubleshooting</h2>
    <ul>
        <li><strong>Kafka Issues:</strong> Make sure Kafka is running and accessible. Ensure that the topic <code>REDDIT_TOPIC</code> exists or is created automatically.</li>
        <li><strong>MongoDB Issues:</strong> Verify your MongoDB URI and ensure MongoDB is up and running.</li>
        <li><strong>Spark Issues:</strong> Check the Spark configuration and ensure the MongoDB Spark Connector is correctly installed.</li>
    </ul>
