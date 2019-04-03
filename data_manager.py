import pandas as pd

from api_calls import SensorAPI


class DataManager:
    def __init__(self):
        self.sensor_ids = [1]  # TODO shouldn't be hardcoded
        self.sensor_api = SensorAPI()
        self.sensor_data = None

    def get_sensor_ids(self):
        raise NotImplementedError

    def update_sensor_data(self, minutes, sensor_id):
        status, data = self.sensor_api.get_sensor_data(minutes, self.sensor_ids)
        if status == 200:
            # for s_id in self.sensor_ids:
            # TODO make keys ints?
            self.sensor_data = pd.DataFrame(
                data["data"][str(sensor_id)], columns=["date", "temp", "moisture"]
            )
            # TODO set the time to PCT timezone
            self.sensor_data["date"] = pd.to_datetime(self.sensor_data["date"])
            self.sensor_data.sort_values(by="date", ascending=True, inplace=True)

    def get_plant_names(self):
        """Gets the plant name and its sensor id to populate the table."""
        plants = []
        for s_id in self.sensor_ids:
            status, data = self.sensor_api.get_plant_by_id(s_id)
            if status == 200:
                plants.append(data["data"])
            # TODO catch api errors
        return plants
