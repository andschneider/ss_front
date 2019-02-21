import dash_core_components as dcc
import dash_html_components as html


def get_layout():
    return html.Div(
        html.Div(
            [
                html.H4("soil sense"),
                dcc.Graph(id="subplots-live", style=dict(width="100%", height="80vh")),
                dcc.Interval(
                    id="interval-component",
                    interval=1 * 1000 * 300,  # in milliseconds
                    n_intervals=0,
                ),
            ]
        )
    )
