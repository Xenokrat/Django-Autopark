import argparse
import json
from datetime import datetime

from confluent_kafka import Producer


def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {msg.value()}: {err.str()}")
    else:
        print(f"Message produced: {msg.value()}")


def kafka_producer(manager: str, vehicle_changes: str):
    conf = {
        'bootstrap.servers': "localhost:34037",
        'client.id': 'VehicleChangeLogger'
    }
    producer = Producer(**conf)
    topic = 'vehicle_changes'

    # Prepare the message
    message = {
        'manager_name': manager,
        'vehicle_changes': vehicle_changes,
        'date_of_change': datetime.now().isoformat()
    }
    message_value = json.dumps(message)

    producer.produce(topic, value=message_value, callback=acked)
    producer.poll(0)
    producer.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send Kafka messages for vehicle updates.")
    parser.add_argument('vehicle_id', type=int, help="The ID of the vehicle.")
    parser.add_argument('status_update', type=str, help="The status update message for the vehicle.")

    args = parser.parse_args()

    # Call the producer function with command-line arguments
    # kafka_producer(args.vehicle_id, args.status_update)
