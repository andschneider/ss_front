import datetime

import pandas as pd

from api_calls import SensorAPI


class DataManager:
    def __init__(self):
        self.sensor_ids = [1]  # TODO shouldn't be hardcoded
        self.sensor_api = SensorAPI()
        self.sensor_data = None
        self.cache_data = None

    def get_sensor_ids(self):
        raise NotImplementedError

    def update_sensor_data(self, minutes, sensor_id):
        """Pulls data from the database and prepares it for plotting.

        There is a shady caching implementation that stores all the data that has been downloaded and will determine
        whether to download new data or just display cached data.

        Parameters
        ----------
        minutes : int
            The desired number of minutes of data to pull down and display.
        sensor_id : int
            The sensor id to get data for.
        """

        # get new data the first time the app is loaded
        if self.sensor_data is None:
            self._get_new_data(minutes, sensor_id)
        # compare desired minutes to the already present data and
        # determine the smallest amount of minutes to be pulled from db
        else:
            current_time_diff, dataframe_time_diff = self.compare_time()
            # case 1 - pull all new data
            if minutes > dataframe_time_diff:
                self._get_new_data(minutes, sensor_id)
            # case 2 - add new data or display already downloaded data
            elif 0 < current_time_diff < dataframe_time_diff:
                # pull new data from db
                print(f"pulling new data: {current_time_diff} | {dataframe_time_diff}")
                data = self.sensor_api.get_sensor_data(
                    current_time_diff, self.sensor_ids
                )
                # TODO clean this up
                new_data = pd.DataFrame(
                    data["data"][str(sensor_id)], columns=["date", "temp", "moisture"]
                )
                new_data["date"] = pd.to_datetime(new_data["date"])
                self.cache_data = self.cache_data.append(new_data, ignore_index=True)
                self.cache_data.sort_values(by="date", ascending=True, inplace=True)
                self.cache_data.drop_duplicates(["date"], keep="last", inplace=True)
                # change the data that is plotted
                self.sensor_data = self.cache_data.iloc[-minutes:]

    def compare_time(self):
        """Compares the times in the cached data as well as the current time.

        For example - if the minutes requested was 10, but the current time compared to latest entry is just 5 minutes
        then only 5 minutes of data would be pulled.

        Another example - if the minutes requested was 20, and the current cached dataframe contains only 10
        minutes of data, then the data that will be pulled is the full 20 minutes. This is because the API doesn't
        accept date ranges, it only pulls X amount of minutes from the current time.
        """

        # get min and max minutes in dataframe
        latest = max(self.cache_data["date"])
        earliest = min(self.cache_data["date"])
        # change timedelta to minutes
        df_time_dff = (latest - earliest).seconds // 60
        # compare minutes requested to current time
        current_time_diff = (datetime.datetime.utcnow() - latest).seconds // 60
        # print(f"Current:{current_time_diff}, DF: {df_time_dff}")
        return current_time_diff, df_time_dff

    def _get_new_data(self, minutes, sensor_id):
        data = self.sensor_api.get_sensor_data(minutes, self.sensor_ids)
        # for s_id in self.sensor_ids:
        # TODO make keys ints?
        self.sensor_data = pd.DataFrame(
            data["data"][str(sensor_id)], columns=["date", "temp", "moisture"]
        )
        self.sensor_data["date"] = pd.to_datetime(self.sensor_data["date"])
        self.sensor_data.sort_values(by="date", ascending=True, inplace=True)
        # shady caching
        self.cache_data = self.sensor_data.copy(deep=True)

    def get_plant_names(self):
        """Gets the plant name and its sensor id to populate the table."""
        plants = []
        for s_id in self.sensor_ids:
            status, data = self.sensor_api.get_plant_by_id(s_id)
            if status == 200:
                plants.append(data["data"])
            # TODO catch api errors
        return plants
