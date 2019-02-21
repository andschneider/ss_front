import pandas as pd

from api_calls import SensorAPI


class DataManager:
    def __init__(self):
        self.sensor_ids = [1]  # TODO shouldn't be hardcoded
        self.sensor_api = SensorAPI()
        self.sensor_data = None

    def update_sensor_data(self, minutes):
        status, data = self.sensor_api.get_sensor_data(minutes, self.sensor_ids)
        if status == 200:
            for s_id in self.sensor_ids:
                # TODO make keys ints?
                df = pd.DataFrame(
                    data["data"][str(s_id)], columns=["date", "temp", "moisture"]
                )
                # TODO clean this up
                df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
                df.drop(columns=["date"], inplace=True)
                self.sensor_data = df
