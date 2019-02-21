from dash.dependencies import Input, Output

from data_manager import DataManager
from plots import create_sub_plots


def setup_callbacks(app):
    print(" +++ callbacks setup")

    @app.callback(
        Output("subplots-live", "figure"), [Input("interval-component", "n_intervals")]
    )
    def update_plot(n):
        # get data
        dm = DataManager()
        dm.update_sensor_data(60 * 48)  # TODO update data more intelligently

        # create a rolling average
        data_rolled = dm.sensor_data.rolling(60).mean()

        return create_sub_plots(dm.sensor_data, data_rolled)
