from dash.dependencies import Input, Output

from components.plots import create_sub_plots
from data_manager import DataManager


def setup_callbacks(app):
    dm = DataManager()
    print(" +++ callbacks setup")

    @app.callback(
        Output("sensor-table", "data"), [Input("interval-component", "n_intervals")]
    )
    def update_table(n):
        if n == 0:
            # get data
            table_data = []
            for s_id in dm.sensor_ids:
                table_data.append({"sensor_id": s_id})
            return table_data

    @app.callback(
        Output("subplots-live", "figure"),
        [
            Input("interval-component", "n_intervals"),
            Input("sensor-table", "selected_rows"),
        ],
    )
    def update_plot(n, selected):
        # selected rows
        # TODO allow for multiple selection
        sensor_ids = dm.sensor_ids[selected[0]]

        # get data
        dm.update_sensor_data(60 * 48, sensor_ids)  # TODO update data more intelligently

        # create a rolling average
        data_rolled = dm.sensor_data.rolling(60).mean()

        return create_sub_plots(dm.sensor_data, data_rolled)
