#!/usr/bin/python3
from models.base_model import BaseModel
from models import storage
from models.city import City


class State(BaseModel):
    """ State class """
    name = ""

    @property
    def cities(self):
        """ Getter method to return the list of City objects linked to the current State """
        cities_list = []
        all_cities = storage.all(City)
        for city in all_cities.values():
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
