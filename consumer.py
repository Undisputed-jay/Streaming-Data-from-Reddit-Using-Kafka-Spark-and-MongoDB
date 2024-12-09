from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import os

# Kafka Topics
topic = "REDDIT_TOPIC"
kafka_bootstrap_servers = 'kafka:9092'

# Consumer Configuration
consumer_config = {
    'bootstrap.servers': kafka_bootstrap_servers,
    'group.id': 'reddit-consumer-group',
    'auto.offset.reset': 'earliest'  
}

# Instantiate the Consumer
consumer = Consumer(consumer_config)

# Subscribe to the input topic
consumer.subscribe([topic])

# Create the dataset folder if it doesn't exist
dataset_folder = "dataset"
os.makedirs(dataset_folder, exist_ok = True)

# Initialize variables
message_count = 0
max_messages = 10000
output_file_path = os.path.join(dataset_folder, "output.jsonl")  # Save in JSONL format (one JSON per line)

try:
    with open(output_file_path, "w") as output_file:
        while message_count < max_messages:
            # Poll for new messages
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue  # No new messages, continue polling
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition reached {msg.partition()} at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                # Deserialize the Kafka message
                comment_data = json.loads(msg.value().decode('utf-8'))
                print(f"Received comment: {comment_data}")

                # Write the comment to the output file
                output_file.write(json.dumps(comment_data) + "\n")

                # Increment the message count
                message_count += 1

                # Print progress every 1000 messages
                if message_count % 1000 == 0:
                    print(f"Processed {message_count} messages...")

        print(f"Reached the limit of {max_messages} messages. Stopping consumer.")

except KeyboardInterrupt:
    print("Consumer interrupted")
finally:
    # Close the consumer
    consumer.close()
