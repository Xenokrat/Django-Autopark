import json

from confluent_kafka import Consumer, KafkaError

def kafka_consumer():
    conf = {
        'bootstrap.servers': "localhost:34037",
        'group.id': 'vehicle_change_logging',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(**conf)
    consumer.subscribe(['vehicle_changes'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            data = json.loads(msg.value().decode('utf-8'))
            log_to_file(data)
    finally:
        consumer.close()

def log_to_file(data):
    with open('vehicle_change_log.txt', 'a') as file:
        log_message = f"{data['date_of_change']} - Manager: {data['manager_name']} changed {data['vehicle_changes']}\n"
        file.write(log_message)


if __name__ == '__main__':
    kafka_consumer()
