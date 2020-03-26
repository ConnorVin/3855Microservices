import connexion
import requests
import yaml
import json
from connexion import NoContent
from pykafka import KafkaClient
import datetime
from flask_cors import CORS, cross_origin
with open('kafka_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

def add_race_information(report):
    client = KafkaClient(hosts=f'{app_config["kafka-server"]}:{app_config["kafka-port"]}')
    topic = client.topics[f'{app_config["topic"]}']
    producer = topic.get_sync_producer()
    msg = { "type": "ri",
            "datetime" : datetime.datetime.now().strftime("%Y-%m-$dT%H: %M: %S"),
            "payload": report
        }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent,201

def add_athlete_information(report):
    client = KafkaClient(hosts=f'{app_config["kafka-server"]}:{app_config["kafka-port"]}')
    topic = client.topics[f'{app_config["topic"]}']
    producer = topic.get_sync_producer()
    msg = { "type": "ai",
        "datetime" :
            datetime.datetime.now().strftime(
                "%Y-%m-$dT%H: %M: %S"),
        "payload": report }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)