#!/usr/bin/env python3
# consumer.py

from kafka import KafkaConsumer
import json
import os
from datetime import datetime
import pprint

# Kafka broker and topic (can be overridden by environment variables)
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "covid_data")

# Maximum number of records to display per batch to avoid log spam
MAX_DISPLAY = 2  

# PrettyPrinter for nice JSON formatting
pp = pprint.PrettyPrinter(indent=2)

def consume_messages():
    """
    Continuously consume messages from Kafka and pretty-print them.

    Parameters explained:
    - auto_offset_reset='earliest': if no committed offsets exist, start from the beginning of the topic.
      Use 'latest' if you want to consume only new messages produced after starting the consumer.
    - enable_auto_commit=True: automatically commit offsets periodically so consumer remembers 
      where it left off when restarted.
    """
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),  # deserialize JSON bytes
        auto_offset_reset='earliest',  # start from beginning if first run
        enable_auto_commit=True         # automatically commit offsets
    )

    for message in consumer:
        timestamp = datetime.now().strftime('%H:%M:%S')
        data = message.value  # data is a list of country records sent by producer

        print(f"[{timestamp}] [INFO] Received batch with {len(data)} records from topic '{KAFKA_TOPIC}'")

        # Display only the first MAX_DISPLAY records to prevent huge logs
        for i, record in enumerate(data):
            if i >= MAX_DISPLAY:
                remaining = len(data) - MAX_DISPLAY
                print(f"  ... {remaining} more records not shown")
                break
            pp.pprint(record)

        print()  # blank line to separate batches for readability

if __name__ == "__main__":
    consume_messages()
