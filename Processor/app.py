import connexion
import yaml
import logging
import logging.config
import os
import json
from apscheduler.schedulers.background import BackgroundScheduler
from connexion import NoContent
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def populate_stats():
    """ Periodically update stats """
    logger.info('Periodic processing has started.')

    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            json_data = json.loads(f.read())
    
    else:
        json_data = {
            "num_athlete_stats": 0,
            "num_swim_stats": 0,
            "updated_timestamp": str(datetime.datetime.now())
        }

    parameters = {'startDate': json_data['updated_timestamp'], 'endDate':str(datetime.datetime.now())}
    athlete_data = requests.get(app_config['eventstore']['uri']+'/report/athlete', params=parameters)
    swim_data = requests.get(app_config['eventstore']['uri']+'/report/race', params=parameters)

    athlete_data_json = athlete_data.json()
    swim_data_json = swim_data.json()

    # Check if requests returned 200
    
    if swim_data.status_code == 200:
        logger.info(f'{len(swim_data_json)} new swim stats.')
    else:
        logger.error('Error: Did not receive 200 response from swim stats.')
    
    if athlete_data.status_code == 200:
        logger.info(f'{len(athlete_data_json)} new athlete stats.')
    else:
        logger.error('Error: Did not receive 200 response from swim stats.')



    if json_data.get('num_athlete_stats'):
        json_data['num_athlete_stats'] = json_data['num_athlete_stats'] + len(athlete_data_json)
    else: 
        json_data['num_athlete_stats'] = len(athlete_data_json)

    if json_data.get('num_swim_stats'):
        json_data['num_swim_stats'] = json_data['num_swim_stats'] + len(swim_data_json)
    else: 
        json_data['num_swim_stats'] = len(swim_data_json)

    json_data['updated_timestamp'] = str(datetime.datetime.now())

    with open(app_config['datastore']['filename'], "w") as f:
        f.write(json.dumps(json_data))

    logger.debug(f"Total swim stats: {json_data['num_swim_stats']}. Total athlete stats: {json_data['num_athlete_stats']}")

    logger.info('Periodic processing has ended.')

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()

def get_statistics():
    """ Get statistics from the data store """
    logger.info("Started request")
    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename']) as f:
            data = json.loads(f.read())

        logging.debug("Request data: {}".format(data))
        logging.info("Request completed")

        return data, 200
    else:
        logger.error("File not found")
        return 404

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)