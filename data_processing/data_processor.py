from collections import defaultdict
from constants.config import POLLUTANTS as POLLUTANTS_ID, CONFIG_PATH
from constants.processing import *
import json
import logging


class DataProcessor:
    # Transform to state machine later
    def __init__(self, station_data: dict):
        self.station_data = station_data
        self.days = 0
        with open(CONFIG_PATH, 'r') as cfgfile:
            self.target_pollutants = json.load(cfgfile)[POLLUTANTS_ID]
        self.monthly_averages = {station: defaultdict(float) for station in self.station_data}
        self.daily_data = None
        self.hourly_data = None
        self.current_station = None

    def process(self):
        """
        calculate daily averages for each pollutant based on code in config
        calculate monthly averages for those pollutants
        return dictionary where key is (pollutant code, notation) and value is the monthly average
        """
        try:
            self.process_stations_values_per_station()
            self.transform_values_to_averages()
        except Exception as e:
            logging.exception(e)
        return self.monthly_averages, self.days >= 28

    def process_stations_values_per_station(self):
        for station in self.station_data:
            self.current_station = station
            for hourly_timestamp in self.station_data[self.current_station][VALUES]:
                self.prepare_for_new_day(hourly_timestamp)
                self.calculate_hourly_values(hourly_timestamp)
                self.finish_daily_calculations(hourly_timestamp)

    def transform_values_to_averages(self):
        for station in self.station_data:
            for key in self.monthly_averages[station]:
                self.monthly_averages[station][key] /= (self.days * HOURS_IN_DAY)

    def finish_daily_calculations(self, hourly_timestamp):
        if hourly_timestamp.endswith('23'):
            for key in self.daily_data:
                self.monthly_averages[self.current_station][key] += self.daily_data[key]

    def prepare_for_new_day(self, hourly_timestamp):
        if hourly_timestamp.endswith('00'):
            self.days += 1
            self.daily_data = defaultdict(float)

    def calculate_hourly_values(self, hourly_timestamp):
        self.hourly_data = self.station_data[self.current_station][VALUES][hourly_timestamp][POLLUTANTS]
        for element in self.hourly_data:
            if (element.startswith('pollutant') and
                    self.hourly_data[element][CODE] in self.target_pollutants):
                key = f"notation: {self.hourly_data[element][NOTATION]} | code: {self.hourly_data[element][CODE]}"
                value = self.hourly_data[element][VALUE]
                self.daily_data[key] += float(value)
