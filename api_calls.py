from configparser import ConfigParser
import os

import requests

from locations import SETTINGS_FOLDER


class SensorAPI:
    def __init__(self):
        self.base_url = self._load_api_settings()

    @staticmethod
    def _load_api_settings():
        parser = ConfigParser()
        settings_file = os.path.join(SETTINGS_FOLDER, "api_settings.ini")
        if os.path.exists(settings_file):
            parser.read(settings_file)
            url = parser["web"]["base_url"]
            return url
        else:
            url = "http://localhost:3030"
            print(f"No API settings file found. Defaulting to {url}")
            return url

    def get_sensor_ids(self):
        url = self.base_url + "/get_sensor_ids"
        r = requests.get(url)
        return r.status_code, r.json()

    def get_sensor_data(self, minutes, sensor_ids):
        url = self.base_url + "/get_sensor_data"

        id_string = ",".join([str(s_id) for s_id in sensor_ids])
        args = f"sensor_ids={id_string}&minutes={minutes}"

        full_url = url + "?" + args
        r = requests.get(full_url)
        if r.status_code == 200:
            return r.json()
        # TODO catch api errors
        # return r.status_code, r.json()

    def get_plant_by_id(self, sensor_id):
        url = self.base_url + "/sensor_info"
        r = requests.get(url, params={"sensor_id": sensor_id})
        return r.status_code, r.json()
