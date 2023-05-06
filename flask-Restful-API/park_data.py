"""
This module contains a class implementation with to get and return data for every park.
"""
import pandas as pd
from models.park import Park


class Parks:
    def __init__(self, park_info_csv: str):
        self.park_info = pd.read_csv(park_info_csv)
        self.park_list = [row['park_name'] for index, row in self.park_info.iterrows()]
        self._parks: dict = {}

    def load_park(self, park_name: str, park_data_csv: str) -> None:
        """
        Load data for a park.
        :param park_name: the name of the park
        :param park_data_csv: csv file with production data
        """
        for index, row in self.park_info.iterrows():
            if park_name == row['park_name']:
                try:
                    self._parks[row['park_name']] = Park(
                        row['park_name'], row['timezone'], row['energy_type'], park_data_csv
                    )
                except FileNotFoundError:
                    print(f"Error, file {park_data_csv} not found")
                except IOError:
                    print(f"Error, file {park_data_csv} is not of csv type")

    def __getitem__(self, item: str):
        return self._parks[item]

    def __str__(self):
        return "Object representing data for all parks." \
               "Use Parks[park_name] to get data from a particular park."
