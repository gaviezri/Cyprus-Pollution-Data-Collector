import json
import logging
import requests
from constants.config import *


class DataFetcher:
    def __init__(self):
        config = json.load(open(CONFIG_PATH, 'r'))
        self.target = config[TARGET]
        self.stations = config[STATIONS]
        # crucial for successful request
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def fetch(self, from_datetime, to_datetime):
        # year(4)-month(2)-day(2)%20HH:MM
        url = f"{self.target}/{from_datetime}/{to_datetime}"
        logging.info(f"requesting data from {url}")
        response = requests.request(method="GET", url=url, headers=self.headers)
        if 200 <= response.status_code < 300:
            result = self.process_success(response)
        else:
            result = DataFetcher.process_failure(response)
        return result

    def process_success(self, response):
        logging.info(f"response status OK - filtering stations: {self.stations}")
        stations_data = response.json()["data"]
        filtered_response = {}
        for station in self.stations:

            filtered_response[stations_data[station]["name_en"]] = stations_data[station]
        return filtered_response

    @staticmethod
    def process_failure(response):
        logging.fatal(f"RESPONSE STATUS: {response.status_code} ### REASON:{response.content}")
        return dict()
