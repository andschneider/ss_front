import plotly
import plotly.graph_objs as go


def create_moisture_plot(data):
    """Creates a single plot of moisture data.

    Parameters
    ----------
    data : DataFrame
        A dataframe of the sensor data, with the index as the date and a column labeled 'moisture.'

    Returns
    -------
    figure : Plotly figure
        A Plotly figure object to be passed to a Dash Graph object.
    """
    moisture_data = go.Scatter(
        name="moisture",
        x=data.index,
        y=data["moisture"],
        line=dict(width=2, color="rgb(58, 118, 175)"),
    )

    traces = [moisture_data]
    layout = go.Layout(
        showlegend=False,
        margin=dict(l=60, r=60, b=60, t=60),
        hovermode="closest",
        title="moisture",
        xaxis=dict(title="date"),
        yaxis=dict(title="moisture"),
    )
    return go.Figure(data=traces, layout=layout)


def create_sub_plots(data, rolled_data):
    """Creates two plots, one of temperature and one of moisture sensor data. Also plots the rolling average data.

    Parameters
    ----------
    data : DataFrame
        A DataFrame of the sensor data, with the index as the date and columns labeled 'moisture' and 'temp.'
    rolled_data : DataFrame
        A DataFrame that has had a rolling average applied to it.

    Returns
    -------
    figure : Plotly figure
        A Plotly figure object to be passed to a Dash Graph object.
    """
    fig = plotly.tools.make_subplots(
        rows=2, cols=1, vertical_spacing=0.2, print_grid=False
    )
    fig["layout"]["margin"] = {"l": 30, "r": 10, "b": 30, "t": 10}
    fig["layout"]["legend"] = {
        "x": 0.9,
        "y": 0.47,
        "xanchor": "left",
        "bgcolor": "rgba(0,0,0,0)",
        "bordercolor": "grey",
        "borderwidth": 1,
    }

    # moisture traces
    fig.append_trace(
        {
            "x": data.index,
            "y": data["moisture"],
            "name": "moist raw",
            "mode": "lines",
            "type": "scatter",
        },
        1,
        1,
    )
    fig.append_trace(
        {
            "x": rolled_data.index,
            "y": rolled_data["moisture"],
            "name": "moist rolled",
            "mode": "lines",
            "type": "scatter",
        },
        1,
        1,
    )

    # temperature traces
    fig.append_trace(
        {
            "x": data.index,
            "y": data["temp"],
            "name": "temp raw",
            "mode": "lines",
            "type": "scatter",
        },
        2,
        1,
    )
    fig.append_trace(
        {
            "x": rolled_data.index,
            "y": rolled_data["temp"],
            "name": "temp rolled",
            "mode": "lines",
            "type": "scatter",
        },
        2,
        1,
    )

    return fig
