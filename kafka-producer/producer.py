#!/usr/bin/env python3
# producer.py 

import requests
import time
from kafka import KafkaProducer
import json 
import os
import sys
from datetime import datetime

# Kafka broker address and topic (can be overridden by environment variables)
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "covid_data")

# Fetch data from the COVID API
def fetch_data(url):
    """Fetch JSON data from the provided URL."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] Failed to fetch data: {e}", file=sys.stderr)
        return None

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER], 
    value_serializer=lambda v: json.dumps(v).encode("utf-8")  # serialize Python dict to JSON bytes
)

def send_loop(url, interval=60):
    """Continuously fetch data and send it to Kafka."""
    while True:
        data = fetch_data(url)
        if data:
            try:
                # Send data to Kafka asynchronously and get a Future object
                future = producer.send(KAFKA_TOPIC, data)

                # Wait for Kafka to confirm the message is sent
                result = future.get(timeout=15)  # blocking call to ensure delivery
                producer.flush()  # optional: flush ensures all queued messages are sent

                # Log successful send with timestamp and batch size
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [INFO] Sent {len(data)} records to {KAFKA_TOPIC}")
                print()  # blank line between batches for readability

            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] [ERROR] Failed to send data: {e}", file=sys.stderr)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [WARN] No data fetched this cycle")

        time.sleep(interval)  # wait before fetching the next batch

if __name__ == "__main__":
    url = "https://disease.sh/v3/covid-19/countries"
    send_loop(url, interval=60)
