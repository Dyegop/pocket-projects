"""
This module contains the model implementation of a Park.
"""
import pandas as pd


class Park:
    def __init__(self, name: str, timezone: str, energy_type: str, park_data_csv: str):
        self.name: str = name
        self.timezone: str = timezone
        self.energy_type: str = energy_type
        self.production = pd.read_csv(park_data_csv)
