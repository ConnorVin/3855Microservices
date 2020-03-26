import connexion
import yaml
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from athlete_information import AthleteInformation
from race_information import RaceInformation
import datetime
from threading import Thread
import json
from pykafka import KafkaClient
import logging
import logging.config
from flask_cors import CORS, cross_origin


with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

with open('kafka_conf.yml', 'r') as f:
    kafka_config = yaml.safe_load(f.read())

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


# def add_race_information(report):
#     """ Receives information on a race """

#     session = DB_SESSION()

#     ri = RaceInformation(report['race_id'],
#                          report['swim'],
#                          report['distance'],
#                          report['distance_measurement']
#                          )

#     session.add(ri)
#     session.commit()
#     session.close()

#     return NoContent, 201


def get_race_information(startDate, endDate):
    """ Get race information from the data store """

    results_list = []
    
    session = DB_SESSION()

    results = session.query(RaceInformation).all()

    results = session.query(RaceInformation).filter(RaceInformation.date_created.between(startDate, endDate))

    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 200


# def add_athlete_information(report):
#     """ Add an athlete's information """

#     session = DB_SESSION()

#     ai = AthleteInformation(report['first_name'],
#                             report['last_name'],
#                             report['age'],
#                             report['height'],
#                             report['weight']
#                             )
    
#     session.add(ai)

#     session.commit()
#     session.close()

#     return NoContent, 201


def get_athlete_information(startDate, endDate):
    """ Get an athlete's information from the data store """
    
    results_list = []
    
    session = DB_SESSION()

    results = session.query(AthleteInformation).all()

    results = session.query(AthleteInformation).filter(AthleteInformation.date_created.between(startDate, endDate))

    for result in results:
        results_list.append(result.to_dict())

    session.close()

    return results_list, 200

def process_messages():
    client = KafkaClient(hosts=f'{kafka_config["kafka-server"]}:{kafka_config["kafka-port"]}')
    topic = client.topics[f'{kafka_config["topic"]}']
    consumer = topic.get_simple_consumer(auto_commit_interval_ms=1000, auto_commit_enable=True, consumer_group="events")

    message_list = []
    for message in consumer:
        message_string = message.value.decode('utf-8')
        message = json.loads(message_string)
        logger.info(f'New Message: {message_string}')
        print(message['type'])
        if message['type'] == 'ri':
            session=DB_SESSION()
            ri = RaceInformation(message['payload']['race_id'],
                         message['payload']['swim'],
                         message['payload']['distance'],
                         message['payload']['distance_measurement'])

            session.add(ri)
            session.commit()
            session.close()

        if message['type'] == 'ai':
            session=DB_SESSION()
            ai = AthleteInformation(message['payload']['first_name'],
                            message['payload']['last_name'],
                            message['payload']['age'],
                            message['payload']['height'],
                            message['payload']['weight'])
    
            session.add(ai)
            session.commit()
            session.close()




app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS']='Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)