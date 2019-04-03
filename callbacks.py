import dash
from dash.dependencies import Input, Output, State
import dash.exceptions

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
            return dm.get_plant_names()

    @app.callback(
        Output("subplots-live", "figure"),
        [
            Input("interval-component", "n_intervals"),
            Input("sensor-table", "selected_rows"),
            Input("input-minutes", "value"),
            Input("input-rolling", "value"),
            Input("button-get-data", "n_clicks"),
        ],
        [State("subplots-live", "figure")],
    )
    def update_plot(n, selected, minutes, rolling, button_click, existing_state):
        # TODO the state is a workaround for the dcc.loading issue in layout.py but is not optimal
        ctx = dash.callback_context
        # print(f"inputs: {ctx.inputs}")
        # print(f"trigger: {ctx.triggered}")

        # TODO allow for multiple selection
        sensor_ids = dm.sensor_ids[selected[0]]

        # on page load default to 10 minutes
        if not minutes:
            minutes = 10

        # run when the time interval set in layout.py is up
        trigger = ctx.triggered[0]["prop_id"].split("-")[0]
        if trigger == "interval" or trigger == "button":
            print("updating plot")
            dm.update_sensor_data(minutes, sensor_ids)
            # create a rolling average
            data_rolled = dm.sensor_data.rolling(int(rolling), on="date").mean()
            return create_sub_plots(dm.sensor_data, data_rolled)

        # don't run
        else:
            raise dash.exceptions.PreventUpdate
            # return existing_state
