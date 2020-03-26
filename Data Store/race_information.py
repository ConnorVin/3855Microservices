from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class RaceInformation(Base):
    """ Race Information """

    __tablename__ = "race_information"

    id = Column(Integer, primary_key=True)
    race_id = Column(String(250), nullable=False)
    swim = Column(String(250), nullable=False)
    distance = Column(Integer, nullable=False)
    distance_measurement = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, race_id, swim, distance, distance_measurement):
        """ Initializes race information """
        self.race_id = race_id
        self.swim = swim
        self.distance = distance
        self.distance_measurement = distance_measurement
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a race's information """
        dict = {}
        dict['id'] = self.id
        dict['race_id'] = self.race_id
        dict['swim'] = self.swim
        dict['distance'] = self.distance
        dict['distance_measurement'] = self.distance_measurement

        return dict