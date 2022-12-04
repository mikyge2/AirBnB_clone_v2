#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models
from models.amenity import Amenity
from models.review import Review
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 nullable=False,
                                 primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'), nullable=False,
                                 primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    review = relationship('Review', cascade='delete', backref='place')
    amenities = relationship('Amenity', secondary='place_amenity',
                             viewonly=False)
    amenity_ids = []

if getenv('HBNB_TYPE_STORAGE') != 'db':
    @property
    def review(self):
        """ return the list of review """
        rev = models.storage.all(Review).values()
        return [re for re in rev if re.place_id == self.id]

    @property
    def amenities(self):
        """ list of amenities """
        objs = models.storage.all(Amenity).values()
        return [obj for obj in objs if obj.id in self.amenity_ids]

    @amenities.setter
    def amenities(self, value):
        """ add an amenity.id to the attribute amenity_ids """
        if type(value) is Amenity:
            self.amenity_ids.append(value.id)
