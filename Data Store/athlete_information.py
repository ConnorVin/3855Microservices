from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class AthleteInformation(Base):
    """ Athlete Information """

    __tablename__ = "athlete_information"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, first_name, last_name, age, height, weight):
        """ Initializes an athlete """
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.height = height
        self.weight = weight
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of an athlete's information """
        dict = {}
        dict['id'] = self.id
        dict['first_name'] = self.first_name
        dict['last_name'] = self.last_name
        dict['age'] = self.age
        dict['height'] = self.height
        dict['weight'] = self.weight

        return dict