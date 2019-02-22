import dash_core_components as dcc
import dash_html_components as html

from components.reusable import Card, Column, Comment
from components.sensor_table import create_sensor_table


def get_layout():
    return html.Div(
        html.Div(
            [
                Column(
                    width=3,
                    children=[
                        Comment("**SOIL SENSE v0**"),
                        Card(
                            children=[
                                html.P("Select sensors to plot:"),
                                create_sensor_table(),
                            ]
                        )
                    ],
                ),
                Column(
                    width=9,
                    children=[
                        Card(
                            children=[
                                dcc.Graph(
                                    id="subplots-live",
                                    style=dict(width="100%", height="80vh"),
                                )
                            ]
                        )
                    ],
                ),
                # live update interval
                dcc.Interval(
                    id="interval-component",
                    interval=1 * 1000 * 300,  # in milliseconds
                    n_intervals=0,
                ),
            ]
        )
    )
