import dash_table


def create_sensor_table():
    table = dash_table.DataTable(
        id="sensor-table",
        columns=[{"name": i, "id": i} for i in ["sensor_id"]],
        active_cell=[],
        is_focused=True,
        row_selectable="multiple",
        selected_rows=[0],
        sorting="be",
        sorting_type="single",
        sorting_settings=[],
        style_cell_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        editable=True,
    )
    return table
