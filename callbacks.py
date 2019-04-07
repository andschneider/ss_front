import dash
from dash.dependencies import Input, Output, State
import dash.exceptions

from components.plots import create_sub_plots
from data_manager import DataManager


def setup_callbacks(app):
    dm = DataManager()
    print(" +++ callbacks setup")

    @app.callback(Output("slider-value", "children"), [Input("input-rolling", "value")])
    def display_slider_value(slider_input):
        return f"Select number of minutes for the rolling average ({slider_input}):"

    @app.callback(
        Output("subplots-live", "figure"),
        [
            Input("sensor-table", "selected_rows"),
            Input("input-minutes", "value"),
            Input("input-rolling", "value"),
            Input("button-get-data", "n_clicks"),
        ],
    )
    def update_plot(selected, minutes, rolling, button_click):
        # TODO the state is a workaround for the dcc.loading issue in layout.py but is not optimal
        ctx = dash.callback_context
        # print(f"inputs: {ctx.inputs}")
        # print(f"trigger: {ctx.triggered}")

        # TODO allow for multiple selection
        sensor_ids = dm.sensor_ids[selected[0]]

        # on page load default to 10 minutes
        if not minutes:
            dm.update_sensor_data(10, sensor_ids)
            data_rolled = dm.sensor_data.rolling(int(rolling), on="date").mean()
            return create_sub_plots(dm.sensor_data, data_rolled)

        # run when the button is clicked
        if ctx.triggered[0]["prop_id"].split("-")[0] == "button":
            print("updating plot")
            dm.update_sensor_data(int(minutes), sensor_ids)
            # create a rolling average
            # TODO set the time to PCT timezone
            data_rolled = dm.sensor_data.rolling(int(rolling), on="date").mean()
            return create_sub_plots(dm.sensor_data, data_rolled)

        # don't run
        else:
            raise dash.exceptions.PreventUpdate
            # return existing_state
