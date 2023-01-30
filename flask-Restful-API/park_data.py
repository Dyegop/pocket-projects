"""
This module contains a class with the data from all the parks.
"""
import pandas as pd
from models.park import Park


class Parks:
    """ Class representation of all the parks. """
    def __init__(self, park_info_csv: str):
        self.park_info = pd.read_csv(park_info_csv)
        self.park_list: list = []
        self._parks: dict = {}

    def load_parks(self, park_data_csv: str):
        """ """
        for index, row in self.park_info.iterrows():
            self.park_list.append(row['park_name'])
            self._parks[row['park_name']] = Park(row['park_name'], row['timezone'], row['energy_type'], park_data_csv)

    def __getitem__(self, item):
        return self._parks[item]

    def __str__(self):
        return "Object representing data for all parks." \
               "Use Parks[park_name] to get data from a particular park."