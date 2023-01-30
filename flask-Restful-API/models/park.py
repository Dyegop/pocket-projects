"""
This module contains the model implementation of a Park.
"""
import pandas as pd


class Park:
    """ Class representation of the data of a single park """
    def __init__(self, name: str, timezone: str, energy_type: str, park_data_csv: str):
        self.name: str = name
        self.timezone: str = timezone
        self.energy_type: str = energy_type
        try:
            self.datetimes = pd.read_csv(park_data_csv)['datetime']
            self.generation = pd.read_csv(park_data_csv)['MW']
        except IOError:
            print(f"Error, file {park_data_csv} is not of csv type")
