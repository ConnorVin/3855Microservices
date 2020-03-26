import connexion
from connexion import NoContent
import requests
import datetime
import json
import yaml
from pykafka import KafkaClient
import logging
from flask_cors import CORS, cross_origin

with open('kafka_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

def race_stat_offset(offset):
    client = KafkaClient(hosts=f'{app_config["kafka-server"]}:{app_config["kafka-port"]}')
    topic = client.topics[f'{app_config["topic"]}']
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)

    message_list = []
    for message in consumer:
        message_string = message.value.decode('utf-8')
        message = json.loads(message_string)
        if message['type'] == 'ri':
            message_list.append(message)

    return message_list[offset], 200

def get_earliest_athlete_stat():
    client = KafkaClient(hosts=f'{app_config["kafka-server"]}:{app_config["kafka-port"]}')
    topic = client.topics[f'{app_config["topic"]}']
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=500)

    message_list = []
    for message in consumer:
        message_string = message.value.decode('utf-8')
        message = json.loads(message_string)
        if message['type'] == 'ai':
            message_list.append(message)
    if len(message_list) == 0:
            return NoContent, 404

    return message_list[-1], 200

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8120)