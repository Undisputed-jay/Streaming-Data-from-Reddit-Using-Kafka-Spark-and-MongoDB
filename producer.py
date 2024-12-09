import praw
from confluent_kafka import Producer
import constant
import json

# Kafka Topic
topic = "REDDIT_TOPIC"

# Broker
producer_config = {
    'bootstrap.servers': 'kafka:9092',
}

# Delivery report callback function
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


# Instantiating the Producer
producer = Producer(producer_config)

# Instantiating Reddit
reddit = praw.Reddit(
    client_id = constant.client_id,
    client_secret = constant.client_secret,
    user_agent = constant.user_agent
)

# Stream comment from politics subreddit
subreddit = reddit.subreddit('Politics')

for comment in subreddit.stream.comments():
    try:
        # Extract and serialize the comment data
        comment_data = {
            "id": comment.id,
            "body": comment.body,
            "author": str(comment.author),
            "created_utc": comment.created_utc,
            "subreddit": str(comment.subreddit)
        }
        # Send comment data to Kafka
        producer.produce(
            topic = topic,
            value = json.dumps(comment_data).encode('utf-8'),
            callback = delivery_report
        )
        producer.poll(0)  # Trigger delivery report callback for any delivered messages

    except Exception as e:
        print(f"Error processing comment: {e}")

producer.flush()