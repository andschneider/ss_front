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
            df = pd.DataFrame(
                data["data"][str(sensor_id)], columns=["date", "temp", "moisture"]
            )
            # TODO clean this up
            df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
            df.drop(columns=["date"], inplace=True)
            self.sensor_data = df

    def get_plant_names(self):
        """Gets the plant name and its sensor id to populate the table."""
        plants = []
        for s_id in self.sensor_ids:
            status, data = self.sensor_api.get_plant_by_id(s_id)
            if status == 200:
                plants.append(data["data"])
            # TODO catch api errors
        return plants
